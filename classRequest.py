from __future__ import print_function
import requests
# import browser_cookie3
import time
import json
import os


class NetworkError(RuntimeError):
    pass


class Requester:
    def __init__(self, hosts, ports):
        self.prod = os.getenv("PROD")
        self.hosts = hosts
        self.ports = ports
        self.host = "127.0.0.1"
        self.cookies = {"session": "s%3ACH2H5DdpB6MzmSsDieZE7UvVMQPehBCt.1z%2B36%2FhnbFqxO7XKSXFCg1VuMhuFT%2B47W4%2B05gVV67k"}
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

    def get_request(self):
        pass

    def post_to_api(self, idi, download, earnings, country, city, category):
        data = {"idi": idi,
                "download": download,
                "earnings": earnings,
                "category": category,
                "country": country,
                "city": city}
        body = json.dumps(data)

        if self.prod == 1:
            self.host = self.hosts.get('api-server')
        url = "http://{}:{}/data/psql/earnings".format(self.host, self.ports.get('api-server'))
        requests.post(url, data=body)

        if self.prod == 1:
            self.host = self.hosts.get('slack-service')
        url = "http://{}:{}/data/earnings".format(self.host, self.ports.get('slack-service'))
        requests.post(url, data=body)

    def post_to_redis(self, data):
        body = json.dumps(data)
        if self.prod == 1:
            self.host = self.hosts.get('api')
        url = "http://{}:{}/data/redis/earnings".format(self.host, self.ports.get('api'))
        requests.post(url, data=body)
