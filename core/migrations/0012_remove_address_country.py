# Generated by Django 2.2.10 on 2020-06-30 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20200630_1152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='country',
        ),
    ]