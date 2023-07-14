from faker import Faker
from faker.providers import credit_card

faker = Faker()
faker.add_provider(credit_card)


def get_card_number():
    card_number = faker.credit_card_number()
    return card_number


def get_card_cvv():
    cvv = faker.credit_card_security_code()
    return cvv


def get_name():
    name = faker.name()
    return name
