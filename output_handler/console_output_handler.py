import textwrap

from colorama import Fore
from colorama import init as colorama_init

from output_handler.base_output_handler import BaseOutputHandler


class ConsoleOutputHandler(BaseOutputHandler):
    @staticmethod
    def out(data: list, limit: int = 0):
        colorama_init()
        if limit:
            data = data[:limit]

        for article in data:
            feed_str = Fore.GREEN + 'Feed' + Fore.RESET + ':' + Fore.LIGHTCYAN_EX + f' {article["source"]}'
            title_str = Fore.GREEN + 'Title' + Fore.RESET + ':' + Fore.RED + f' {article["title"]}'
            date_str = Fore.GREEN + 'Date' + Fore.RESET + ':' + Fore.LIGHTYELLOW_EX + f' {article["published"]}'
            link_str = Fore.GREEN + 'Link' + Fore.RESET + ':' + Fore.LIGHTBLUE_EX + f' {article["link"]}'
            details_str = textwrap.fill(Fore.RESET + f'{article["details"]}', 100)

            links = ''
            for index, link in enumerate(article["media"]):
                links += Fore.MAGENTA + f'[{index + 1}]' + Fore.RESET + ':' + Fore.LIGHTBLUE_EX + f' {link}'

            output = ''
            output += f'''
{feed_str}

{title_str}
{date_str}
{link_str}

{details_str}

{Fore.GREEN + 'Links' + Fore.RESET + ':'}
{links}
                    '''
            print(textwrap.dedent(output))
