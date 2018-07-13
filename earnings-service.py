from flask import Flask, render_template, request, flash
from flask_cors import CORS
from classEarningsService import EarningsService
import itertools

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


def test():
    print(earnings.config)
    earnings.data_from_redis = {"25_a_day": {"11111": 1, "22222": 1, "33333": 1},
                               "on_demand": {"44444": 1, "55555": 1, "66666": 1},
                               "enhanced": {"77777": 1, "88888": 1, "99999": 1},
                               "single_image_and_other": {"12345": 1, "5678": 1, "90123": 1}}
    # earnings.get()

    ls = []

    lst1 = ["999", "222", "333"]

    ls = list(itertools.chain(ls, lst1))
    print(ls)

    lst2 = ["444", "555", "666"]

    ls = list(itertools.chain(ls, lst2))

    print(ls)


@app.route("/history/earnings", methods=['GET'])
def get_data():
    return ""


if __name__ == '__main__':
    conf_path = "./config.yaml"
    log_path = "./app_logs"
    earnings = EarningsService(conf_path, log_path)
    test()
    # get_data()
    # app.run(host='127.0.0.1', port=8003)
