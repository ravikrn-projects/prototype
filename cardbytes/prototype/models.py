from __future__ import unicode_literals

from django.db import models


class Merchant(models.Model):
    name = models.CharField(max_length=200, unique=True)

class Offers(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    cashback = models.IntegerField(default=0)
    cashback_status = models.CharField(max_length=50, default='Unused')

class User(models.Model):
    name = models.CharField(max_length=200)
    acc_balance = models.FloatField(default=0)
    cashback_realized = models.FloatField(default=0)

class Vendor(models.Model):
	revenue = models.FloatField(default=0)

class Bank(models.Model):
	revenue = models.FloatField(default=0)
	revenue_clm = models.FloatField(default=0) 


