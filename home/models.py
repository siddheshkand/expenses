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

    def __str__(self):
        return str(self.date) + ":-" + str(self.amount) + " " + str(self.tags)


class Scheduler(models.Model):
    event_name = models.TextField()
    date = models.DateField()
    from_time = models.TimeField()
    to_time = models.TimeField()
    location = models.TextField()

    def __str__(self):
        return str(self.date) + ":-" + str(self.event_name) + " " + str(self.location)


PeriodicExpensesOption = (
    ('1', "Monthly"),
    ('3', "Quarterly"),
    ('12', "Yearly"),
)


class PeriodicExpense(models.Model):
    name = models.TextField(max_length=255)
    amount = models.PositiveIntegerField()
    type = models.TextField(max_length=255, choices=PeriodicExpensesOption)
    description = models.TextField()


class TodoList(models.Model):
    item_name = models.TextField()
    # Todo Complete todo list module
