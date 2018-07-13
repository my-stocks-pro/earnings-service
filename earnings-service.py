from flask import Flask, render_template, request, flash
from flask_cors import CORS
from classEarningsService import EarningsService

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


def test():
    print(earnings.config)
    earnings.ids_from_redis = {"25_a_day": ["11111", "22222", "33333"],
                               "on_demand": ["44444", "55555", "66666"],
                               "enhanced": ["77777", "88888", "99999"],
                               "single_image_and_other": ["12345", "5678", "90123"]}
    earnings.get()


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
