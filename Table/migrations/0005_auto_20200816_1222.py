# Generated by Django 3.0.3 on 2020-08-16 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Table', '0004_auto_20200816_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='deletetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
