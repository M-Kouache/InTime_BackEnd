# Generated by Django 4.0.4 on 2022-06-17 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_alter_service_libelle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='libelle',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='events.service'),
        ),
    ]