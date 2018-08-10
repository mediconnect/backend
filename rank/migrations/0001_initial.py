# Generated by Django 2.0.2 on 2018-08-10 03:50

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
            name='Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField(default=0)),
                ('disease', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='disease_rank', to='disease.Disease')),
                ('hospital', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hospital_rank', to='hospital.Hospital')),
            ],
            options={
                'db_table': 'db_rank',
            },
        ),
    ]