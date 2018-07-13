from classRequest import Requester
from classLogger import Logger
from classConfiger import Configer
import pandas as pd
import json
from datetime import datetime
import itertools


class EarningsService(Requester, Logger, Configer):
    def __init__(self, conf_path, log_path):
        Configer.__init__(self, conf_path)
        Requester.__init__(self, self.config.get('hosts'), self.config.get('ports'))
        Logger.__init__(self, self.config.get('service'), log_path)
        self.curr_date = datetime.now().strftime('%Y-%m-%d')
        self.map = ""
        self.data_from_redis = {}
        self.map_url = self.config.get('map_url')
        self.categories = self.config.get('categories')
        self.base_url = self.config.get('base_url')

    def get(self):
        print(self.categories)
        for category_base, category_name in self.categories.items():
            curr_data = self.data_from_redis.get(category_base)
            new_idi = []
            new_erns = []
            new_dls = []
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
                        list_id, list_ernings, list_downloads = self.get_new_data(df, category_name)
                        new_idi = list(itertools.chain(new_idi, list_id))
                        new_erns = list(itertools.chain(new_erns, list_ernings))
                        new_dls = list(itertools.chain(new_dls, list_downloads))
                    except ValueError:
                        # self.to_logger(ValueError)
                        print(ValueError)
                        break
                except():
                    print("error in request")
            self.processing_dataframe(new_idi, new_erns, new_dls, curr_data, category_name)
            # self.to_logger("error in request")

    @staticmethod
    def get_new_data(df, category):
        print(category)
        df = df[0]
        list_id = df[df.columns[1]].tolist()  # ID
        list_ernings = df[df.columns[2]].tolist()  # Earnings
        list_downloads = df[df.columns[3]].tolist()  # Downloads
        return list_id, list_ernings, list_downloads

    def processing_dataframe(self, list_idi, list_erns, list_dls, curr_data, category):
        data_to_redis = {}
        for idi, erns, dls in zip(list_idi, list_erns, list_dls):
            if idi not in curr_data:
                self.map = json.loads(self.get_response(self.map_url).content)
                country, city = self.get_location(idi)
                self.post_to_api(idi, dls, erns, country, city, category)
            else:
                curr_dls = curr_data.get(idi).get('downloads')
                if dls != curr_dls:
                    curr_erns = curr_data.get(idi).get('earnings')
                    new_dls = dls - curr_dls
                    new_erns = erns - curr_erns
                    self.map = json.loads(self.get_response(self.map_url).content)
                    country, city = self.get_location(idi)
                    self.post_to_api(idi, new_dls, new_erns, country, city, category)
            data_to_redis[idi] = {"downloads": dls, "earnings": erns}
        self.post_to_redis(data_to_redis)

    def get_location(self, idi):
        for location in self.map:
            media_id = location.get('media_id')
            if str(media_id) == idi:
                country = location.get('country')
                city = location.get('city')
                if country is None and city is not None:
                    country = city
                return country, city
        return None, None
