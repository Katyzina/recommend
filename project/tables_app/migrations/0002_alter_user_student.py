# Generated by Django 4.0 on 2024-03-02 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tables_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tables_app.student', verbose_name='Студент'),
        ),
    ]
