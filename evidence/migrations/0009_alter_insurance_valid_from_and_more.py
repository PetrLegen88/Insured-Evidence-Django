# Generated by Django 4.1.1 on 2023-06-20 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evidence', '0008_alter_insured_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insurance',
            name='valid_from',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='valid_until',
            field=models.DateField(),
        ),
    ]