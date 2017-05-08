# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class InvoiceProfile(models.Model):
    client = models.OneToOneField('timesheets.Client')
    payment_id = models.CharField(max_length=255)


class Invoice(models.Model):
    invoice_profile = models.ForeignKey('invoicing.Client')
    entries = models.ManyToManyField('timesheets.Entry')
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    total_billed = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_lenght=255)
