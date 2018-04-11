# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-05 19:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0017_require_video_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtubevideo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]