# Generated by Django 2.0.5 on 2018-11-03 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reservation', '0001_initial'),
        ('questionnaire', '0001_initial'),
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='reservation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservation.Reservation'),
        ),
        migrations.AddField(
            model_name='answer',
            name='translator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='staff.Translator'),
        ),
    ]