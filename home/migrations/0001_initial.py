# Generated by Django 2.1.3 on 2019-09-15 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IncomeAndExpense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount', models.PositiveIntegerField()),
                ('tags', models.TextField()),
                ('mode', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('income', 'income'), ('expense', 'expense')], max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Income and Expense',
                'ordering': ('date',),
            },
        ),
        migrations.CreateModel(
            name='PeriodicExpenses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=255)),
                ('amount', models.PositiveIntegerField()),
                ('type', models.TextField(choices=[('1', 'Monthly'), ('3', 'Quarterly'), ('12', 'Yearly')], max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Scheduler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.TextField()),
                ('date', models.DateField()),
                ('from_time', models.TimeField()),
                ('to_time', models.TimeField()),
                ('location', models.TextField()),
            ],
        ),
    ]
