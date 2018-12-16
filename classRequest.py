from __future__ import print_function
import requests
# import browser_cookie3
import time
import json
import os


class NetworkError(RuntimeError):
    pass


class Requester:
    def __init__(self, gateway):
        self.prod = os.getenv("PROD")
        self.gateway = gateway
        self.redisDB = "earnings"
        self.cookies = {
            "session": "s%3ACH2H5DdpB6MzmSsDieZE7UvVMQPehBCt.1z%2B36%2FhnbFqxO7XKSXFCg1VuMhuFT%2B47W4%2B05gVV67k"}
        print("LOGIN to Shutterstock...")

    def retryer(max_retries=10, timeout=5):
        def wraps(func):
            request_exceptions = (
                requests.exceptions.Timeout,
                requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError)

            def inner(*args, **kwargs):
                for i in range(max_retries):
                    try:
                        result = func(*args, **kwargs)
                    except request_exceptions:
                        time.sleep(timeout)
                        continue
                    else:
                        return result
                else:
                    raise NetworkError

            return inner

        return wraps

    @retryer(max_retries=10, timeout=2)
    def get_response(self, url):
        return requests.get(url, cookies=self.cookies)

    def get_data_frame(self, url):
        return self.get_response(self, url).text.split("\n")

    def post_slack(self, idi, download, earnings, country, city, category):
        data = {"idi": idi,
                "download": download,
                "earnings": earnings,
                "category": category,
                "country": country,
                "city": city}
        body = json.dumps(data)
        requests.post(f"{self.gateway}/slack", data=body)

    def redis_get(self, key):
        data = json.dumps({"db": self.redisDB, "key": key, "val": None})
        r = requests.get(f"{self.gateway}/redis", data=data)
        res = r.json()
        return res

    def redis_set(self, key, val):
        msg = {"key": key, "db": "earnings", "val": val}
        requests.post(f"{self.gateway}/redis", data=json.dumps(msg))

    def redis_del(self):
        msg = {"db": self.redisDB, "key": None, "val": None}
        requests.delete(f"{self.gateway}/redis", data=json.dumps(msg))

    def postgres_save(self):
        pass