# Generated by Django 2.1.15 on 2020-03-03 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20200303_1406'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='region',
        ),
    ]
