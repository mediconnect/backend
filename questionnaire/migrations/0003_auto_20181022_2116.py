# Generated by Django 2.0.2 on 2018-10-23 01:16

from django.db import migrations, models
import questionnaire.models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0002_auto_20180925_2040'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questionnaire',
            old_name='origin_pdf',
            new_name='origin',
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='translated',
            field=models.FileField(null=True, upload_to=questionnaire.models.questions_path),
        ),
    ]
