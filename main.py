from argparse import ArgumentParser, Namespace
import feedparser
import psycopg2
from datetime import datetime
from db.sql_handler import SQLHandler
from db.models import NewsModel, MediaModel
from output_handler.console_output_handler import ConsoleOutputHandler
from output_handler.json_output_handler import JSONOutputHandler


def parse_cmd_args() -> Namespace:
    """
    arguments parser from command line
    """
    parser = ArgumentParser(description='Process some integers.')
    parser.add_argument('url', type=str, help='rss news url')
    parser.add_argument('--limit', type=int, help='news amount limit')
    parser.add_argument('--date', type=str, help='reads cached news since this date, --limit affects on news count')
    parser.add_argument('--json', type=bool, default=0, help='set 1 if want json output too')
    return parser.parse_args()


def parse_rss(url: str) -> list:
    feed = feedparser.parse(url)

    source_title = feed['feed']['title']
    news = feed['entries']

    output = []
    for item in news:
        article = {
            'source': source_title,
            'title': item['title'],
            'link': item['link'],
            'published': item['published'],
            'media': [i['url'] for i in item['links'][1:]],
            'details': item['summary']
        }
        output.append(article)

    return output


def insert_news(data: list[dict], insert_old: bool = False):
    connection = SQLHandler()
    db_date_format = '%Y-%m-%d'
    parse_date_format = '%a, %d %b %Y %H:%M:%S %z'

    if insert_old:
        actual_data = data
    else:
        last_date = connection.select_max('published', 'news')[0]
        actual_data = [el for el in data if (datetime.strptime(el['published'], parse_date_format).date() >= last_date)]

    for el in actual_data:
        news_model = NewsModel(source=el['source'],
                               title=el['title'],
                               link=el['link'],
                               published=el['published'],
                               details=el['details'])
        try:
            connection.insert(news_model, 'news')
            id = connection.select_max('id', 'news')[0]
            for link in el['media']:
                media_model = MediaModel(link=link, news_id=id)
                connection.insert(media_model, 'media')
                id += 1

        except psycopg2.errors.UniqueViolation:
            pass
        except psycopg2.errors.StringDataRightTruncation:
            print(news_model)


def convert_date(date: str) -> str:
    return datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y%m%d')


def read_cached_news(date: str, limit: int = 0) -> list:
    connection = SQLHandler()

    limit = str(limit) if limit else '*'

    recieved_data = connection.request(f"select {limit} from news where published >= '{date}';")

    data = []
    for article in recieved_data:
        idx = article[0]
        media = [link[1] for link in connection.request(f"select * from media where news_id = {idx};")]
        data_to_add = NewsModel(*article[1:]).asdict()
        data_to_add['media'] = media
        data.append(data_to_add)

    return data


def main():
    args = parse_cmd_args()

    if args.date:
        data = read_cached_news(args.date)
    else:
        data = parse_rss(args.url)[9:]
        insert_news(data, True)

    ConsoleOutputHandler.out(data, args.limit)

    if args.json:
        JSONOutputHandler.out(data)


if __name__ == "__main__":
    main()
