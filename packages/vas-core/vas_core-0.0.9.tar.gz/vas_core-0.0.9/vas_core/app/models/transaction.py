import uuid

from django.db import models

from vas_core import constants
from vas_core.app.models import BaseModelAbstract


class Transaction(BaseModelAbstract, models.Model):
    old_id = None
    created_by = None
    request_id = models.UUIDField(default=uuid.uuid4)
    txn_id = models.CharField(max_length=255)
    customer_acct_no = models.CharField(max_length=30)
    amount = models.DecimalField(decimal_places=2, max_digits=15)
    biller = models.ForeignKey("Biller", on_delete=models.DO_NOTHING, null=True, blank=True)
    provider = models.ForeignKey("Provider", on_delete=models.DO_NOTHING, null=True, blank=True)
    provider_acct_no = models.CharField(max_length=30, null=True, blank=True)
    status = models.CharField(max_length=1, choices=constants.TRANSACTION_STATUSES,
                              default=constants.INITIALIZED_TRANSACTION_STATUS)
    status_reason = models.TextField(default="Transaction Initialized")
    channel = models.ForeignKey("Channel", on_delete=models.DO_NOTHING, null=True, blank=True)
    channel_txn_id = models.CharField(max_length=255)
    customer_id = models.CharField(max_length=30, null=True, blank=True)
    is_debited = models.BooleanField(default=False)
    debit_response_code = models.CharField(max_length=30, null=True, blank=True)
    debited_on = models.DateTimeField(null=True, blank=True)
    is_reversed = models.BooleanField(default=False)
    reversal_response_code = models.CharField(max_length=30, null=True, blank=True)
    reversed_on = models.DateTimeField(null=True, blank=True)
    requery_count = models.IntegerField(default=0)
    provider_resp_status = models.CharField(max_length=100, null=True, blank=True)
    provider_resp_desc = models.TextField(null=True, blank=True)

