from flask import Flask, render_template, request, flash
from flask_cors import CORS
from classEarningsService import EarningsService
import itertools
import json

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/health", methods=['GET'])
def health():
    return app.response_class(
        response=json.dumps(earnings.health()),
        status=200,
        mimetype='application/json'
    )


@app.route("/version", methods=['GET'])
def version():
    return app.response_class(
        response=json.dumps(earnings.version()),
        status=200,
        mimetype='application/json'
    )


@app.route("/", methods=['GET'])
def earnings():
    timestamp_new = earnings.date_now()
    data = earnings.redis_get(timestamp_new)

    timestamp = data.get("timestamp")
    if timestamp is None or timestamp != timestamp_new:
        earnings.redis_del()

    for category_base, category_name in earnings.categories.items():

        category_data = data.get(category_base)

        if category_data is None:
            error = f"{category_base} not exist in data_from_redis"
            continue

        category_data = earnings.get(category_data, timestamp_new)
        earnings.redis_set(category_base, category_data)
        earnings.pos

    earnings.redis_set("timestamp", timestamp_new)

    return app.response_class(
        response=json.dumps(error),
        status=200,
        mimetype='application/json'
    )


if __name__ == '__main__':
    conf_path = "./config.yaml"
    log_path = "./app_logs"
    earnings = EarningsService(conf_path, log_path)
    app.run(host='127.0.0.1', port=9002)
