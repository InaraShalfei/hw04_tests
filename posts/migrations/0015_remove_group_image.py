# Generated by Django 2.2.6 on 2021-02-10 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_auto_20210210_1519'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='image',
        ),
    ]