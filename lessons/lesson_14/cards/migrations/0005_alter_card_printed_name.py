# Generated by Django 4.2.2 on 2023-07-14 17:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('cards', '0004_alter_card_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='printed_name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
