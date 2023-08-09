'''
Model classes
'''
# pylint:disable=no-member
from datetime import datetime
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


def get_total_amount(user) -> Decimal:
    return Payment.objects.filter(user=user).aggregate(
        models.Sum('amount', default=0)
    )['amount__sum']


class BaseModel(models.Model):
    '''
    Abstract base model
    Has the user that own the entity, and a name and description
    '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    class Meta:
        '''Meta class for BaseModel'''
        abstract = True


class PaymentRelatedModel(BaseModel):
    '''
    Abstract model for Models that have a many-to-one relationship to Payment
    '''
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.name)

    @property
    def total(self) -> Decimal:
        '''
        The total amount of the payments of this object
        '''
        return self.payment_set.filter(pending=False).aggregate(
            models.Sum('amount', default=0)
        )['amount__sum']

    class Meta:
        '''Meta class for PaymentRelatedModel'''
        abstract = True


class Budget(PaymentRelatedModel):
    '''
    Model for a budget
    '''
    active = models.BooleanField(default=True)

    def add_from_csv(self, text: str):
        '''
        Add payees and payments to this budget from a CSV formatted string
        '''
        rows = text.strip().split('\n')
        for line in rows:
            record = line.split(',')
            payee = Payee.objects.get_or_create(
                name=record[0], user=self.user)[0]
            payment = Payment(
                user=self.user,
                payee=payee,
                budget=self,
                amount=record[1],
                date=datetime.strptime(record[2], '%d/%m/%Y'),
            )
            if len(record) >= 4:
                payment.notes = record[3]
            if len(record) >= 5:
                payment.pending = record[4] != ''
            payment.save()


class Payee(PaymentRelatedModel):
    '''
    Model for a payee
    '''


class Payment(BaseModel):
    '''
    Model for a payment
    Requires a payee and a budget
    Has an amount and date
    '''
    payee = models.ForeignKey(
        Payee,
        on_delete=models.CASCADE,
    )
    budget = models.ForeignKey(
        Budget,
        on_delete=models.CASCADE,
        limit_choices_to={'active': True}
    )
    amount = models.DecimalField(decimal_places=2, max_digits=7)
    date = models.DateField()
    pending = models.BooleanField(
        default=False, verbose_name='Exclude from total')
    notes = models.TextField(null=True, blank=True)

    def clean(self):
        errors = []
        if self.user != self.budget.user:
            errors.append('You can only access your own budgets')
        if self.user != self.payee.user:
            errors.append('You can only access your own payees')
        if len(errors) != 0:
            raise ValidationError(errors)
