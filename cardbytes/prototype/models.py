from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Merchant(models.Model):
	name = models.CharField(max_length=200)

class Offers(models.Model):
	merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
	cashback = models.IntegerField(default=0)
	cashback_status = models.CharField(max_length=50, default='Unused')