# Generated by Django 3.1.4 on 2020-12-13 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reference',
            name='article',
        ),
    ]