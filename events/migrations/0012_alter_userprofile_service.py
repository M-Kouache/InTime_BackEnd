# Generated by Django 4.0.4 on 2022-06-17 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_alter_service_libelle_alter_userprofile_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='service',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='events.service'),
        ),
    ]
