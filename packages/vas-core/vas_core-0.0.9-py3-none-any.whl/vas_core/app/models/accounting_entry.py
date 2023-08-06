from django.db import models

from vas_core.app.models import BaseModelAbstract


class AccountConfig(BaseModelAbstract, models.Model):
    account = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=100, null=False, blank=False)
    is_dynamic = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.description} - {self.account}"

    def __unicode__(self):
        return self.__str__()

    def to_dict(self) -> dict:
        return {
            "account": self.account,
            "desc": self.description,
            "is_dynamic": self.is_dynamic,
        }


class FeeAccountConfig(BaseModelAbstract, models.Model):
    accounting_entry = models.ForeignKey('AccountingEntry', on_delete=models.CASCADE, related_name='fees')
    description = models.CharField(max_length=100)
    account = models.ForeignKey("AccountConfig", on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=5, max_digits=50, null=False,
                                 blank=False)
    max_amount = models.DecimalField(decimal_places=5, max_digits=50, default=0)
    is_percentage = models.BooleanField(default=False)
    deduct_from_amount = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.account} - {self.amount}{ '%' if self.is_percentage else ''}"

    def __unicode__(self):
        return self.__str__()

    def to_dict(self) -> dict:
        return {
            "account_config": self.account.to_dict(),
            "amount": self.amount,
            "is_percentage": self.is_percentage,
        }


class AccountingEntry(BaseModelAbstract, models.Model):
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    currency = models.CharField(max_length=5)
    transit_account = models.CharField(max_length=30, null=True, blank=True)

    def to_dict(self) -> dict:
        _fees = []
        for fee in self.fees.all():
            _fees.append(fee.to_dict())
        return {
            # "settlement_account": self.settlement_account.to_dict(),
            "fees": _fees
        }


class ChannelAccountingEntry(BaseModelAbstract, models.Model):
    biller_form = models.ForeignKey('BillerForm', on_delete=models.CASCADE)
    channel = models.ForeignKey('Channel', on_delete=models.CASCADE)
    accounting_entry = models.ForeignKey('AccountingEntry', on_delete=models.CASCADE)
