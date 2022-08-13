import textwrap

from output_handler.base_output_handler import BaseOutputHandler


class ConsoleOutputHandler(BaseOutputHandler):
    @staticmethod
    def out(data: list, limit: int = 0):
        if limit:
            data = data[:limit]

        for article in data:
            feed_str = f'Feed: {article["source"]}'
            title_str = f'Title: {article["title"]}'
            date_str = f'Date: {article["published"]}'
            details_str = f'{article["details"]}'
            link_str = f'Link: {article["link"]}'
            links = ''
            for index, link in enumerate(article["media"]):
                links += f'[{index + 1}]: {link}'
            output = textwrap.dedent(
                f'''
                    {feed_str}
    
                    {title_str}
                    {date_str}
                    {link_str}
        
                    {details_str}
        
                    Links:
                    {links}
                ''')
            print(output)
