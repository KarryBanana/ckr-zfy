# Generated by Django 3.0.3 on 2020-08-17 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Table', '0005_auto_20200816_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='groupnum',
            field=models.IntegerField(default=-1),
        ),
    ]
