# Generated by Django 4.1.1 on 2023-07-26 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evidence', '0015_insuranceevent_closed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='insuranceevent',
            name='closed',
        ),
    ]
