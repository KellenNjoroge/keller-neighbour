# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-24 13:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jirani', '0002_auto_20181124_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=100)),
                ('profilepic', models.ImageField(blank=True, upload_to='picture/')),
                ('contact', models.CharField(blank=True, max_length=15)),
                ('hoodpin', models.BooleanField(default=False)),
                ('hood', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home', to='jirani.Hood')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
