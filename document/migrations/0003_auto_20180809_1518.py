# Generated by Django 2.0.2 on 2018-08-09 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0002_document_resid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='data',
            new_name='file',
        ),
    ]
