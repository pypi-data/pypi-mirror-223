# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-08 13:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("api", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="template",
            name="group",
            field=models.CharField(
                blank=True, db_index=True, max_length=255, null=True
            ),
        )
    ]
