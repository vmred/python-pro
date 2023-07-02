import uuid

from django.db import models


class Card(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pan = models.CharField(max_length=16, unique=True)
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=3)
    issue_date = models.DateField()
    owner_id = models.UUIDField(default=uuid.uuid4)
    status = models.CharField()
