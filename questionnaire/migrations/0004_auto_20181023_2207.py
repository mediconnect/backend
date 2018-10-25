# Generated by Django 2.0.2 on 2018-10-24 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0003_auto_20181022_2116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='selected',
        ),
        migrations.RemoveField(
            model_name='question',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='questionnaire',
            name='questions',
        ),
        migrations.AlterField(
            model_name='question',
            name='format',
            field=models.IntegerField(choices=[(1, 'Multiple Choice'), (2, 'All that Matched'), (3, 'Short Answer')]),
        ),
    ]
