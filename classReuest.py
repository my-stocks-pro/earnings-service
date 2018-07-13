from __future__ import print_function
import requests
# import browser_cookie3
import time
import json


class NetworkError(RuntimeError):
    pass


class Requester:
    def __init__(self):
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

    def post_request(self, df):
        body = json.dumps(df)
        print(df)
        # TODO need test...
        url = "http://127.0.0.1:8001/data/psql/earnings"
        requests.post(url, data=body)
