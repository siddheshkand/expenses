# Generated by Django 2.1.3 on 2019-06-10 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_income'),
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
                ('type', models.CharField(choices=[('income', 'income'), ('expenses', 'expenses')], max_length=255)),
            ],
        ),
    ]