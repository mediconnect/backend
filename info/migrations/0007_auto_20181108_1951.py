# Generated by Django 2.1.3 on 2018-11-09 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0006_auto_20181108_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='deposit',
            field=models.IntegerField(default=10000),
        ),
        migrations.AlterField(
            model_name='info',
            name='full_price',
            field=models.IntegerField(default=100000),
        ),
    ]
