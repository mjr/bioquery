# Generated by Django 3.1.4 on 2020-12-13 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_reference_article'),
        ('articles', '0002_auto_20201210_2215'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='references',
            field=models.ManyToManyField(blank=True, to='core.Reference', verbose_name='referências'),
        ),
    ]
