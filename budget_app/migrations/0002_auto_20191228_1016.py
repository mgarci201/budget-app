# Generated by Django 3.0.1 on 2019-12-28 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expenseinfo',
            old_name='expenses',
            new_name='expense_name',
        ),
    ]
