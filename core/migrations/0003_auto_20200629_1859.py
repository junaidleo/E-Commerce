# Generated by Django 2.2.10 on 2020-06-29 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200629_0001'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-ordered_date']},
        ),
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.CharField(default='', max_length=100),
        ),
    ]