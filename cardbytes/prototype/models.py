from __future__ import unicode_literals

from django.db import models


class Merchant(models.Model):
    name = models.CharField(max_length=200, unique=True)

class User(models.Model):
    name = models.CharField(max_length=200)
    acc_balance = models.FloatField()
    cashback_realized = models.FloatField()

class Offer(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    cashback = models.FloatField(default=0)
    cashback_used = models.BooleanField(default=False)
    goal = models.IntegerField()
    customer_tag = models.IntegerField()
    geography = models.IntegerField()

class Vendor(models.Model):
    revenue = models.FloatField(default=0)

class Bank(models.Model):
    revenue_with_clm = models.FloatField(default=0)
    revenue_without_clm = models.FloatField(default=0) 

class Relevance(models.Model):
    unique_id = models.IntegerField(default=0)
    index = models.FloatField(default=0)
