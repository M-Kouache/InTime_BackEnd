# Generated by Django 4.0.4 on 2022-05-21 23:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_remove_events_event_handler_events_departement_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='private_events',
        ),
    ]
