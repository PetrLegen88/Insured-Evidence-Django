# Generated by Django 4.1.1 on 2023-07-26 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evidence', '0014_rename_cost_insuranceevent_paid_out'),
    ]

    operations = [
        migrations.AddField(
            model_name='insuranceevent',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]