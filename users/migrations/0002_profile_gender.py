# Generated by Django 3.2.7 on 2021-09-18 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
