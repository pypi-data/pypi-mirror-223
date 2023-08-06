import json

from django.db import models

from vas_core import constants
from vas_core.app.models import BaseModelAbstract


class BillerForm(BaseModelAbstract, models.Model):
    biller = models.OneToOneField("Biller", on_delete=models.CASCADE)
    validation_field = models.TextField(blank=True)
    api_url = models.URLField(null=True, blank=True, help_text='Defaults to merchant url')
    form_type = models.CharField(max_length=50, choices=constants.BILLER_FORM_TYPES,
                                 default=constants.REGULAR_BILLER_FORM_TYPE)
    settlement_account = models.ForeignKey("AccountConfig",
                                           on_delete=models.CASCADE)
    accounting_entry = models.ForeignKey('AccountingEntry', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.biller}'s Form"

    def __unicode__(self):
        return self.__str__()

    def to_redis(self):
        fields_json = dict()
        fields = self.fields.all()
        if fields.count() == 1:
            fields_json['field'] = fields.first().to_dict()
        else:
            fields_json['field'] = list()
            for field in fields:
                fields_json['field'].append(field.to_dict())
        products = self.products.all()
        if products.count() > 0:
            fields_json['productList'] = {'item': []}
            for product in products:
                fields_json['productList']['item'].append(product.to_dict())
        data = {
            "validation_field": self.validation_field,
            "api_url": self.api_url,
            "fields_json": fields_json,
            "form_type": self.form_type
        }
        return json.dumps(data)
