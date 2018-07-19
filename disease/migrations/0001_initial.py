# Generated by Django 2.0.2 on 2018-07-19 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='unknown', max_length=50)),
                ('keyword', models.CharField(default='unknown', max_length=150)),
            ],
            options={
                'db_table': 'db_disease',
            },
        ),
    ]
