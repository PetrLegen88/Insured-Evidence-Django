# Generated by Django 4.1.1 on 2023-06-21 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('evidence', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='insuranceevent',
            name='insurance',
        ),
        migrations.AddField(
            model_name='insuranceevent',
            name='insured',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='evidence.insured'),
        ),
        migrations.AddField(
            model_name='insured',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile_photos'),
        ),
        migrations.AddField(
            model_name='insured',
            name='role',
            field=models.CharField(choices=[('insurer', 'Insurer'), ('insured', 'Insured')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='insurance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='insurance', to='evidence.insured'),
        ),
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
        migrations.AlterField(
            model_name='insured',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='insured', to=settings.AUTH_USER_MODEL),
        ),
    ]