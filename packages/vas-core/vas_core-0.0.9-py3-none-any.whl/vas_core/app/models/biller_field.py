from django.db import models

from vas_core.app.models import BaseModelAbstract, LocalizationField


class BillerFormField(BaseModelAbstract, models.Model):
    biller_form = models.ForeignKey("BillerForm", on_delete=models.CASCADE, related_name='fields')
    field_id = models.CharField(max_length=100, null=False, blank=False)
    field_name = LocalizationField()
    required = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.biller_form.biller} Form Field"

    def __unicode__(self):
        return self.__str__()

    def to_dict(self):
        data = {
            "FieldId": self.field_id,
            "FieldName": self.field_name,
            "req": f"{int(self.required)}"
        }
        return data


class BillerFormProduct(models.Model):
    biller_form = models.ForeignKey("BillerForm", on_delete=models.CASCADE, related_name='products')
    product_id = models.CharField(max_length=100)
    name = LocalizationField()
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.biller_form.biller} Form Product"

    def __unicode__(self):
        return self.__str__()

    def to_dict(self):
        data = {
            "id": self.product_id,
            "desc": self.name,
            "amount": str(self.amount)
        }
        return data
