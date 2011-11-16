from django.db import models
from django.contrib.auth.models import User
import datetime


class Account(models.Model):
    owner   = models.ForeignKey(User)
    name    = models.CharField(max_length=50)
    agency  = models.CharField(max_length=50, blank=True, null=True)
    number  = models.CharField(max_length=50, blank=True, null=True)
    initial = models.DecimalField(max_digits=12, decimal_places=2)

    def __unicode__(self):
        return self.name

    
class Payee(models.Model):
    owner = models.ForeignKey(User)
    name  = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name   = models.CharField(max_length=200, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True)

    def __unicode__(self):
        return self.name


class PaymentType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class Transaction(models.Model):
    owner        = models.ForeignKey(User)
    category     = models.ForeignKey(Category, blank=True, null=True)
    payee        = models.ForeignKey(Payee, blank=True, null=True)
    account      = models.ForeignKey(Account)
    payment_type = models.ForeignKey(PaymentType, blank=True, null=True)
    description  = models.CharField(max_length=250)
    amount       = models.DecimalField(max_digits=12, decimal_places=2)
    date         = models.DateField(default=datetime.date.today())

    class Meta:
        ordering = ['date', ]

    def __unicode__(self):
        return self.description
