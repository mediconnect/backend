# Generated by Django 2.0.2 on 2018-11-08 02:35

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0002_info_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='id',
            field=models.UUIDField(default=uuid.UUID('46f01ca1-b220-4d64-9aea-ce296612129f'), editable=False, primary_key=True, serialize=False),
        ),
    ]
