from django.contrib.postgres.fields import *
from django.contrib.auth.models import User
from django.db import models

# Regions
class Regions(models.Model):
    name  = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ('name',)

# Locations
class Locations(models.Model):
    name   = models.CharField(max_length=100, blank=True, default='')
    region = models.ForeignKey(Regions, related_name='locations', on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)

# Areas 
class Areas(models.Model):
    name     = models.CharField(max_length=100, blank=True, default='')
    location = models.ForeignKey(Locations, related_name='areas', on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)

# Pokémons Species
class Species(models.Model):
    abilities    = ArrayField(models.CharField(max_length=300, blank=True ))
    capture_rate = models.CharField(max_length=300, null=True, blank=True, default='')
    color        = models.CharField(max_length=300, null=True, blank=True, default='')
    flavor_text  = models.CharField(max_length=300, null=True, blank=True, default='')
    height       = models.CharField(max_length=300, null=True, blank=True, default='')
    moves        = ArrayField(models.CharField(max_length=1500, blank=True ), size = 500)
    name         = models.CharField(max_length=300, null=True, blank=True, default='')
    sprites      = JSONField()
    stats        = ArrayField(JSONField())
    types        = ArrayField(models.CharField(max_length=300, blank=True ))
    weight       = models.CharField(max_length=300, null=True, blank=True, default='')
    areas        = models.ManyToManyField(Areas, related_name='species')


    class Meta:
        ordering = ('name',)

# Pokémons of users 
class Storage_Users(models.Model):
    specie          = models.ForeignKey(Species, on_delete=models.CASCADE)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    nick_name       = models.CharField(max_length=100, blank=True, default='')
    is_party_member = models.BooleanField(blank=True)

    class Meta:
        ordering = ('specie',)
