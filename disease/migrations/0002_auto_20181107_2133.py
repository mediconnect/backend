# Generated by Django 2.0.2 on 2018-11-08 02:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('disease', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disease',
            name='id',
            field=models.UUIDField(default=uuid.UUID('64133dfa-b9fc-4c4f-b669-98fcd661e2b6'), editable=False, primary_key=True, serialize=False),
        ),
    ]