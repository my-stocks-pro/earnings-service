from classRequest import Requester
from classLogger import Logger
from classConfiger import Configer
import pandas as pd
import json
from datetime import datetime


class EarningsService(Requester, Logger, Configer):
    def __init__(self, conf_path, log_path):
        Configer.__init__(self, conf_path)
        Requester.__init__(self)
        Logger.__init__(self, self.config.get('service'), log_path)
        self.curr_date = datetime.now().strftime('%Y-%m-%d')
        self.map = ""
        self.ids_from_redis = ""
        self.map_url = self.config.get('map_url')
        self.categories = self.config.get('categories')
        self.base_url = self.config.get('base_url')

    def get(self):
        print(self.categories)
        for category_base, category_name in self.categories.items():
            page = 1
            while True:
                tmp_url = self.base_url.format(str(page), self.curr_date, category_base)
                try:
                    r = self.get_response(tmp_url)
                    if int(r.url[r.url.index("=") + 1:r.url.index("&")]) < page:
                        print("empty url ->" + tmp_url)
                        # self.to_logger("empty url ->" + tmp_url)
                        break
                    # self.to_logger(tmp_url)
                    r_map = self.get_response(self.map_url)
                    self.map = json.loads(r_map.content)
                    print(tmp_url)
                    page += 1
                    try:
                        df = pd.read_html(r.content)
                        self.processing_dataframe(df, category_name)
                    except ValueError:
                        # self.to_logger(ValueError)
                        print(ValueError)
                        break
                except():
                    print("error in request")
                    # self.to_logger("error in request")

    def processing_dataframe(self, df, category):
        print(category)
        df = df[0]
        list_id = df[df.columns[1]].tolist()  # ID
        list_downloads = df[df.columns[3]].tolist()  # Downloads
        for idi, download in zip(list_id, list_downloads):
            print(idi, download)
            # country, city = self.get_location(idi)
            # self.post(idi, download,  country, city, category)
