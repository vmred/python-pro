from datetime import datetime
from typing import Any
from urllib import parse

import dateutil.parser
import requests


def check_if_bank_supported(value: str) -> str:
    """
    Checks if bank is supported and returns abbreviation or raises exception otherwise
    :param value: bank value
    :return: bank abbreviation
    """
    value = str(value)
    allowed_values = {
        'pb, privatbank, PrivatBank, PB': 'PB',
        'nbu, nationalbank, NB, NationalBank': 'NBU',
    }
    for k, v in allowed_values.items():
        if value in k:
            return v

    raise ValueError(f'"{value}" bank is unknown or not supported.')


def reformat_date(value: str) -> Any:
    """
    Reformat date to d.m.y format or raises an exception
    :param value: string date
    :return: formatted date
    """
    try:
        return dateutil.parser.parse(value).strftime("%d.%m.%Y")
    except Exception as ex:
        raise ValueError('Invalid date format') from ex


def get_currency_iso_code(currency: str) -> int:
    '''
    Функція повертає ISO код валюти
    :param currency: назва валюти
    :return: код валюти
    '''
    currency_dict = {
        'UAH': 980,
        'USD': 840,
        'EUR': 978,
        'GBP': 826,
        'AZN': 944,
        'CAD': 124,
        'PLN': 985,
    }
    try:
        return currency_dict[currency]
    except Exception as ex:
        raise KeyError('Currency not found! Update currencies information') from ex


def get_currency_exchange_rate(currency_a: str, currency_b: str) -> str:
    currency_code_a = get_currency_iso_code(currency_a)
    currency_code_b = get_currency_iso_code(currency_b)

    response = requests.get('https://api.monobank.ua/bank/currency')  # pylint: disable=missing-timeout
    json = response.json()

    if response.status_code == 200:
        for _, v in enumerate(json):
            if v.get('currencyCodeA') == currency_code_a and v.get('currencyCodeB') == currency_code_b:
                date = datetime.fromtimestamp(int(v.get('date'))).strftime('%Y-%m-%d %H:%M:%S')
                rate_buy = v.get('rateBuy')
                rate_sell = v.get('rateSell')
                return f'exchange rate {currency_a} to {currency_b} for {date}: \n rate buy - {rate_buy} \n rate sell - {rate_sell}'
            return f'Not found: exchange rate {currency_a} to {currency_b}'
    else:
        return f"Api error {response.status_code}: {json.get('errorDescription')}"


# pylint: disable=too-many-return-statements
def get_pb_exchange_rate(convert_currency: str, bank: str, rate_date: str) -> str:
    bank = check_if_bank_supported(bank)
    rate_date = reformat_date(rate_date)
    params = {
        'json': '',
        'date': rate_date,
    }
    query = parse.urlencode(params)
    api_url = 'https://api.privatbank.ua/p24api/exchange_rates?'
    response = requests.get(api_url + query)  # pylint: disable=missing-timeout
    json = response.json()

    if response.status_code == 200:
        rates = json['exchangeRate']
        for rate in rates:
            if rate['currency'] == convert_currency:
                if bank == 'NBU':
                    try:
                        sale_rate = rate['saleRateNB']
                        purchase_rate = rate['purchaseRateNB']
                        return f'Exchange rate UAH to {convert_currency} for {rate_date} at {bank}: sale={sale_rate}, purchase={purchase_rate}'
                    except KeyError:
                        return f'There is no exchange rate NBU for {convert_currency}'
                if bank == 'PB':
                    try:
                        sale_rate = rate['saleRate']
                        purchase_rate = rate['purchaseRate']
                        return f'Exchange rate UAH to {convert_currency} for {rate_date} at {bank}: sale={sale_rate}, purchase={purchase_rate}'
                    except KeyError:
                        return f'There is no exchange rate PrivatBank for {convert_currency}'

                return f'Unknown bank: {bank}'

            return 'Currencies does not match'
    else:
        return f'error {response.status_code}'
