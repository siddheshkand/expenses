from django.db import models

IandE = [
    ('income', 'income'),
    ('expense', 'expense'),
]


class IncomeAndExpense(models.Model):
    date = models.DateField()
    amount = models.PositiveIntegerField()
    tags = models.TextField()
    mode = models.CharField(max_length=255)
    type = models.CharField(choices=IandE, max_length=255)

    class Meta:
        verbose_name_plural = 'Income and Expense'
        ordering = ('date',)
