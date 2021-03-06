# Generated by Django 2.1.2 on 2018-11-09 01:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hospital', '0001_initial'),
        ('disease', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50)),
                ('description', models.TextField(max_length=200)),
                ('obsolete', models.BooleanField(default=False)),
                ('extensions', models.TextField(blank=True, max_length=100, null=True)),
                ('limit', models.IntegerField(default=16384)),
            ],
            options={
                'db_table': 'db_requirement_file_type',
            },
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('require_list', models.BinaryField()),
                ('disease_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='disease.Disease')),
                ('hospital_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital.Hospital')),
            ],
            options={
                'db_table': 'db_requirement',
            },
        ),
    ]
