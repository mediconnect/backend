# Generated by Django 2.0.2 on 2018-06-12 01:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0002_remove_customer_zipcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('first_name_pinyin', models.CharField(max_length=50)),
                ('last_name_pinyin', models.CharField(max_length=50)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('birthdate', models.DateField()),
                ('relationship', models.CharField(max_length=50)),
                ('passport', models.CharField(max_length=20)),
                ('notes', models.CharField(blank=True, max_length=10000)),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.Customer')),
            ],
            options={
                'db_table': 'db_patient',
            },
        ),
    ]
