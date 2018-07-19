# Generated by Django 2.0.2 on 2018-07-19 01:50

from django.db import migrations, models
import django.db.models.deletion
import questionnaire.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('disease', '0001_initial'),
        ('hospital', '0001_initial'),
        ('translator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, max_length=200)),
                ('questions', models.FileField(null=True, upload_to=questionnaire.models.questions_path)),
                ('questions_path', models.CharField(max_length=200)),
                ('is_translated', models.BooleanField(default=False)),
                ('origin_pdf', models.FileField(null=True, upload_to=models.CharField(max_length=200))),
                ('origin_pdf_path', models.CharField(max_length=200)),
                ('disease', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='disease.Disease')),
                ('hospital', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital.Hospital')),
                ('translator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='translator.Translator')),
            ],
            options={
                'db_table': 'db_questionnaire',
            },
        ),
    ]
