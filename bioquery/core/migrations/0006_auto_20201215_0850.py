# Generated by Django 3.1.4 on 2020-12-15 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20201215_0802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dna',
            name='sequence',
            field=models.TextField(verbose_name='sequência'),
        ),
    ]