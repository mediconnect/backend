# Generated by Django 2.0.2 on 2018-08-10 05:19

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('disease', '0001_initial'),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('area', models.CharField(blank=True, max_length=50)),
                ('overall_rank', models.IntegerField(default=0)),
                ('website', models.URLField(blank=True)),
                ('introduction', models.TextField(default='intro')),
                ('specialty', models.TextField(default='specialty')),
                ('feedback_time', models.IntegerField(default=1)),
                ('average_score', models.DecimalField(decimal_places=3, max_digits=4, null=True)),
                ('review_number', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'db_hospital',
            },
        ),
        migrations.CreateModel(
            name='HospitalReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=200, null=True)),
                ('score', models.IntegerField(null=True)),
                ('customer_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.Customer')),
                ('hospital_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital.Hospital')),
            ],
            options={
                'db_table': 'db_hospital_review',
            },
        ),
        migrations.CreateModel(
            name='LikeHospital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.Customer')),
                ('disease', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='disease.Disease')),
                ('hospital', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital.Hospital')),
            ],
            options={
                'db_table': 'db_like_hospital',
            },
        ),
    ]
