from django.contrib import admin

# Register your models here.
from .models.cards import Card

admin.site.register(Card)
