# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-31 23:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0002_auto_20170321_0231'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearningModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trained', models.BooleanField(default=False)),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='medida',
            name='std',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]
