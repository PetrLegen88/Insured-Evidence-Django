# Generated by Django 4.1.1 on 2023-06-16 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evidence', '0003_insuranceevent_insured'),
    ]

    operations = [
        migrations.AddField(
            model_name='insured',
            name='role',
            field=models.CharField(choices=[('insurer', 'Insurer'), ('insured', 'Insured')], max_length=10, null=True),
        ),
    ]
