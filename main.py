from argparse import ArgumentParser, Namespace
import feedparser


def parse_cmd_args() -> Namespace:
    """
    arguments parser from command line
    """
    parser = ArgumentParser(description='Process some integers.')
    parser.add_argument('url', type=str, help='rss news url')
    parser.add_argument('--limit', type=int, help='news amount limit')
    return parser.parse_args()


def main():
    args = parse_cmd_args()

    feed = feedparser.parse(args.url)

    source_title = feed['feed']['title']
    news = feed['entries']

    for article in news:
        title = article['title']
        link = article['link']
        published = article['published']
        media = [i['url'] for i in article['links'][1:]]
        details = article['summary']

        print(f'Feed: {source_title}\n')
        print(f'Title: {title}')
        print(f'Date: {published}')

        print(f'\n{details}')

        print('\n\nLinks:')
        for index, link in enumerate(media):
            print(f'[{index+1}]: {link}')
        print('#'*20)


if __name__ == "__main__":
    main()
