from argparse import ArgumentParser, Namespace
from output_handler.console_output_handler import ConsoleOutputHandler
from output_handler.json_output_handler import JSONOutputHandler
import feedparser
import colorama


def parse_cmd_args() -> Namespace:
    """
    arguments parser from command line
    """
    parser = ArgumentParser(description='Process some integers.')
    parser.add_argument('url', type=str, help='rss news url')
    parser.add_argument('--limit', type=int, help='news amount limit')
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


def main():
    args = parse_cmd_args()

    data = parse_rss(args.url)

    ConsoleOutputHandler.out(data, args.limit)

    #JSONOutputHandler.out(data)


if __name__ == "__main__":
    main()
