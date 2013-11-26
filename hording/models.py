import os.path
import time

from django.db import models as dj_model

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse as url_reverse

class Company(dj_model.Model):
    """
    A company which either develops or publishes game software.
    """
    name = dj_model.TextField()

    class Meta:
        verbose_name_plural = "companies"

    def __str__(self):
        return self.name

class Region(dj_model.Model):
    """
    A game release region.
    """
    code = dj_model.CharField(primary_key=True, max_length=2)
    name = dj_model.TextField(unique=True)

    def __str__(self):
        return "{} - {}".format(self.code, self.name)

class Game(dj_model.Model):
    """
    A game.
    """
    title = dj_model.TextField()
    developer = dj_model.ForeignKey(Company)

    def __str__(self):
        return self.title

class Platform(dj_model.Model):
    """
    A game platform.
    """
    name = dj_model.TextField(unique=True)

    def __str__(self):
        return self.name

class GameRelease(dj_model.Model):
    """
    An original release in a game region.
    """
    game = dj_model.ForeignKey(Game)
    platform = dj_model.ForeignKey(Platform)
    region = dj_model.ForeignKey(Region)
    publisher = dj_model.ForeignKey(Company)
    release_date = dj_model.DateField(blank=True)

    class Meta:
        unique_together = ("region", "platform", "publisher", "game")

