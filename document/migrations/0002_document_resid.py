# Generated by Django 2.0.5 on 2018-11-03 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('document', '0001_initial'),
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='resid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservation.Reservation'),
        ),
    ]
