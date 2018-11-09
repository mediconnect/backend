# Generated by Django 2.0.2 on 2018-11-08 02:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('disease', '0001_initial'),
        ('hospital', '0002_auto_20181104_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deposit', models.IntegerField(default=10000)),
                ('full_price', models.IntegerField(default=100000)),
                ('description', models.TextField(default='information')),
                ('disease', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='disease_price', to='disease.Disease')),
                ('hospital', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hospital_price', to='hospital.Hospital')),
            ],
            options={
                'db_table': 'db_info',
            },
        ),
    ]