from django.contrib import admin

# Register your models here.
from .models.card import Card

admin.site.register(Card)
