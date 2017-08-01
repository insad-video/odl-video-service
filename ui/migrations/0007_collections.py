# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-09 02:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ui', '0006_video_multiangle'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('title', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('moira_lists', models.ManyToManyField(blank=True, to='ui.MoiraList')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameField(
            model_name='video',
            old_name='s3_subkey',
            new_name='key',
        ),
        migrations.RemoveField(
            model_name='video',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='video',
            name='moira_lists',
        ),
        migrations.AddField(
            model_name='video',
            name='collection',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='ui.Collection'),
            preserve_default=False,
        ),
    ]