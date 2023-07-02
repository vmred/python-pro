# Generated by Django 4.2.2 on 2023-07-02 10:14

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pan', models.CharField(max_length=16)),
                ('expiry_date', models.DateField()),
                ('cvv', models.CharField(max_length=3)),
                ('issue_date', models.DateField()),
                ('owner_id', models.UUIDField(default=uuid.uuid4)),
                ('status', models.CharField()),
            ],
        ),
    ]
