import hashlib
import uuid


class Status:
    new = 'new'
    active = 'active'
    blocked = 'blocked'


class Card:
    def __init__(self, pan: str, expiry_date: str, cvv: str, issue_date: str, owner_id: uuid, status: Status):
        self.pan = pan
        self.expiry_date = expiry_date
        self.cvv = self.hash_data(cvv)
        self.issue_date = issue_date
        self.owner_id = owner_id
        self.status = status

    def activate_card(self):
        if self.status == Status.blocked:
            raise ValueError('Not allowed to activate blocked database')

        self.status = Status.active

    def block_card(self):
        self.status = Status.blocked

    @staticmethod
    def hash_data(data):
        # Використання SHA-256 для хешування даних
        sha256_hash = hashlib.sha256()
        sha256_hash.update(data.encode('utf-8'))
        return sha256_hash.hexdigest()
