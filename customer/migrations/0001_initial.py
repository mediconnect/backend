# Generated by Django 2.0.2 on 2018-03-21 13:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tel', models.CharField(default='unknown', max_length=50)),
                ('address', models.CharField(default='unknown', max_length=50)),
                ('zipcode', models.CharField(default='unknown', max_length=50)),
                ('wechat', models.CharField(blank=True, max_length=50)),
                ('weibo', models.CharField(blank=True, max_length=50)),
                ('qq', models.CharField(blank=True, max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'db_customer',
            },
        ),
    ]
