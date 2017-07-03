# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-03 18:50
from __future__ import unicode_literals

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20170628_0007'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Gallery', max_length=30)),
                ('image', models.ImageField(upload_to=blog.models.gallery_upload)),
            ],
        ),
    ]
