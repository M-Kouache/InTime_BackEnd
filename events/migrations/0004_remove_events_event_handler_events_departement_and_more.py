# Generated by Django 4.0.4 on 2022-05-21 22:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_department_options_alter_service_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='event_handler',
        ),
        migrations.AddField(
            model_name='events',
            name='departement',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='events.department'),
        ),
        migrations.AddField(
            model_name='events',
            name='private_events',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='events',
            name='public_events',
            field=models.BooleanField(default=True),
        ),
    ]
