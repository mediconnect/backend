# Generated by Django 2.0.2 on 2018-07-20 04:23

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hospital', '0001_initial'),
        ('reservation', '0001_initial'),
        ('disease', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SlotBind',
            fields=[
                ('slot_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('reservation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reservation.Reservation')),
            ],
            options={
                'db_table': 'db_slotbind',
            },
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('timeslot_id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('slot_year', models.IntegerField()),
                ('slot_weeknum', models.IntegerField()),
                ('availability', models.IntegerField()),
                ('disease', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='disease.Disease')),
                ('hospital', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital.Hospital')),
            ],
            options={
                'db_table': 'db_timeslot',
            },
        ),
        migrations.AddField(
            model_name='slotbind',
            name='timeslot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='slot.TimeSlot'),
        ),
    ]
