# Generated by Django 4.0.4 on 2022-06-10 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_logins'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logins',
            name='token',
            field=models.CharField(max_length=36),
        ),
    ]