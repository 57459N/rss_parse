import os
from output_handler.base_output_handler import BaseOutputHandler
import json
from datetime import datetime


class JSONOutputHandler(BaseOutputHandler):
    @staticmethod
    def out(data: list):
        dirname = 'downloads'
        now = datetime.now().strftime("%m-%d-%Y_%H-%M")

        filename = f'rss_{data[0]["source"]}_{now}.json'
        os.makedirs(dirname, exist_ok=True)

        with open(os.path.join(dirname, filename), 'w', encoding='utf-16') as file:
            json.dump(data, file, ensure_ascii=False)
