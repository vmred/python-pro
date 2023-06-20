import hashlib
import uuid

from lessons.lesson_6.app.utils import hash_data


class Status:
    new = 'new'
    active = 'active'
    blocked = 'blocked'


class Card:
    def __init__(self, pan: str, expiry_date: str, cvv: str, issue_date: str, owner_id: uuid, status: Status):
        self.pan = pan
        self.expiry_date = expiry_date
        self.cvv = hash_data(cvv)
        self.issue_date = issue_date
        self.owner_id = owner_id
        self.status = status

    def activate_card(self):
        if self.status == Status.blocked:
            raise ValueError('Not allowed to activate blocked database')

        self.status = Status.active

    def block_card(self):
        self.status = Status.blocked
