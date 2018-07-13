from flask import Flask, render_template, request, flash
from flask_cors import CORS
from classEarningsService import EarningsService

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


def test():
    data = ["11111", "22222", "33333"]


@app.route("/history/earnings", methods=['GET'])
def get_data():

    return ""


def main():
    print(1)


if __name__ == '__main__':
    earnings = EarningsService()
    test()
    # get_data()
    # app.run(host='127.0.0.1', port=8003)
