from django.contrib import admin as dj_admin
from django.core.management.base import BaseCommand

from functools import wraps

def register_for(model):
    def inner(cls):
        dj_admin.site.register(model, cls)

        return cls

    return inner

def command(func):
    class Command(BaseCommand):
        def handle(self, *args, **kwargs):
            func(*args, **kwargs)

    return Command

