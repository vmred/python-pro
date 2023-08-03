import re

REGEX_MATCH_PASSPORT = r'^[A-Z]{2}\d{6}$'
REGEX_MATCH_CAR_NUMBER_KHARKIV = r'^(XX|EX|AX|KX)\d{4}[A-Z]{2}$'
REGEX_MATCH_CAR_NUMBER_DNEPR = r'^(PP|MI|AE|KE)\d{4}[A-Z]{2}$'
REGEX_MATCH_INN = r'^\d{10}$'


def is_passport_valid(passport_number):
    return bool(re.match(REGEX_MATCH_PASSPORT, passport_number))


def is_car_number_valid_kharkiv(car_number):
    return bool(re.match(REGEX_MATCH_CAR_NUMBER_KHARKIV, car_number))


def is_car_number_valid_dnepr(car_number):
    return bool(re.match(REGEX_MATCH_CAR_NUMBER_DNEPR, car_number))


def is_inn_valid(inn):
    return bool(re.match(REGEX_MATCH_INN, inn))
