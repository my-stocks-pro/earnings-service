from classReuest import Requester
from classLogger import Logger
from classConfiger import Configer
import pandas as pd
import json


class EarningsService(Requester, Logger, Configer):
    def __init__(self, conf_path):
        Configer.__init__(self, conf_path)
        Requester.__init__(self)
        Logger.__init__(self, self.config.get('earnings-service'))
        self.map = ""
        self.url_map = self.config.get('url_map')
        self.categories = self.config.get('categories')
        self.base_urls = self.config.get('urls')

    def get_by_date(self, date):
        for url in self.base_urls:
            page = 1
            while True:
                tmp_url = url.format(str(page), str(date.strftime('%Y-%m-%d')))
                try:
                    r = self.get_response(tmp_url)
                    if int(r.url[r.url.index("=") + 1:r.url.index("&")]) < page:
                        print("empty url ->" + tmp_url)
                        # self.to_logger("empty url ->" + tmp_url)
                        break
                    # self.to_logger(tmp_url)
                    r_map = self.get_response(self.url_map)
                    self.map = json.loads(r_map.content)
                    print(tmp_url)
                    page += 1
                    try:
                        df = pd.read_html(r.content)
                        self.processing_dataframe(df, tmp_url)
                    except ValueError:
                        # self.to_logger(ValueError)
                        print(ValueError)
                        break
                except():
                    print("error in request")
                    # self.to_logger("error in request")
