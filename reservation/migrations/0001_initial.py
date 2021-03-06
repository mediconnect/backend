# Generated by Django 2.1.2 on 2018-11-09 01:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patient', '0001_initial'),
        ('hospital', '0001_initial'),
        ('disease', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('res_id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('commit_at', models.DateTimeField(blank=True, null=True)),
                ('status', models.IntegerField(default=0)),
                ('trans_status', models.IntegerField(default=0)),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('first_hospital', models.CharField(blank=True, max_length=300)),
                ('first_doctor_name', models.CharField(blank=True, max_length=100)),
                ('first_doctor_contact', models.CharField(blank=True, max_length=100)),
                ('note', models.CharField(blank=True, max_length=1000)),
                ('disease_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='disease.Disease')),
                ('hospital_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital.Hospital')),
                ('patient_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.Patient')),
            ],
            options={
                'db_table': 'db_reservation',
            },
        ),
    ]
