# Generated by Django 4.0 on 2024-03-31 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables_app', '0008_student_telegram'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='town',
            field=models.CharField(default=1, max_length=50, verbose_name='Город'),
            preserve_default=False,
        ),
    ]
