from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
   price = models.FloatField(null=True)
   ticker = models.CharField(max_length = 8)
   pe_ratio = models.FloatField(null=True)
   eps = models.FloatField(null=True)
   last_updated = models.DateTimeField(auto_now=False,null=True)
   def __str__(self):
      return self.ticker
   class Meta:
      ordering = ['ticker']
   class Admin:
      pass

class Asset(models.Model):
   name = models.CharField(max_length = 8, null=True)
   quantity = models.FloatField(null = True)
   last_updated = models.DateTimeField(auto_now=False,null=True)
   def __str__(self):
      return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    assets = models.ManyToManyField(Asset, blank=True)
    total = models.FloatField(null=True)
    def __str__(self):
        return self.user.username