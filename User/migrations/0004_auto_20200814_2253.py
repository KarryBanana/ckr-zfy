# Generated by Django 3.0.3 on 2020-08-14 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_auto_20200812_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='hobby',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='introduction',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
