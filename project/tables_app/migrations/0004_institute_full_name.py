# Generated by Django 4.0 on 2024-03-16 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables_app', '0003_alter_user_employer'),
    ]

    operations = [
        migrations.AddField(
            model_name='institute',
            name='full_name',
            field=models.CharField(default=1, max_length=255, verbose_name='Полное название'),
            preserve_default=False,
        ),
    ]
