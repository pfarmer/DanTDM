# -*- coding: utf-8 -*-
# Generated by Django 2.0.1 on 2018-01-19 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deployment', '0004_auto_20180118_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='created',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='events',
            name='message',
            field=models.TextField(),
        ),
    ]
