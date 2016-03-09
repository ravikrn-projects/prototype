from __future__ import unicode_literals

from django.db import models


class Merchant(models.Model):
    name = models.CharField(max_length=200)
    merchant_id = models.IntegerField(primary_key=True, default=0)
    category = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)

class User(models.Model):
    name = models.CharField(max_length=200, default='****')
    user_id = models.IntegerField(primary_key=True, default=0)
    acc_balance = models.FloatField(default=10000)
    cashback_realized = models.FloatField(default=0)
    age = models.IntegerField(default=18)
    # customer_tag = models.IntegerField(default=0)
    frequent_buyer = models.CharField(max_length=200, default="Frequent")
    # income_tag = models.IntegerField(default=0, blank=True)
    city = models.CharField(max_length=200, blank=True)
    locality = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)

class Offer(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    cashback = models.FloatField(default=0)
    goal = models.IntegerField()

class Vendor(models.Model):
    revenue = models.FloatField(default=0)

class Bank(models.Model):
    revenue_with_clm = models.FloatField(default=0)
    revenue_without_clm = models.FloatField(default=0) 

class Transaction(models.Model):
    transaction_id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()
    bank_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    amount = models.FloatField()
    cashback = models.FloatField(default=0)

class Relevance(models.Model):
    user_id = models.IntegerField(default=0, unique=True)
    index = models.FloatField(default=0)
