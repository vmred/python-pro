from flask import Flask, request

from lessons.lesson_3.app.db_practice import get_customers
from lessons.lesson_3.app.utils import get_currency_exchange_rate, get_pb_exchange_rate

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p><b>Hello, World!</b></p>"


@app.route("/rates", methods=['GET'])
def get_rates():
    currency_a = request.args.get('currency_a', default='USD')
    currency_b = request.args.get('currency_b', default='UAH')
    result = get_currency_exchange_rate(currency_a, currency_b)
    return result


@app.route("/rates_pb", methods=['GET'])
def get_pb_rates():
    convert_currency = request.args.get('convert_currency', default='USD')
    bank = request.args.get('bank', default='NBU')
    rate_date = request.args.get('rate_date', default='01.11.2022')
    return get_pb_exchange_rate(convert_currency, bank, rate_date)


@app.route('/customers', methods=['GET'])
def customers():
    state = request.args.get('state', default=None)
    city = request.args.get('city', default=None)

    return get_customers(state_name=state, city_name=city)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
