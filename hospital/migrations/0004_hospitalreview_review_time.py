# Generated by Django 2.1.3 on 2018-11-09 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0003_auto_20181107_2253'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospitalreview',
            name='review_time',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
