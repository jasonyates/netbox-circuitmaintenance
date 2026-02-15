from django.db import migrations, models

import netbox_circuitmaintenance.models


class Migration(migrations.Migration):

    dependencies = [
        (
            "netbox_circuitmaintenance",
            "0009_nullable_notification_fk_and_timezone",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="circuitmaintenance",
            name="status",
            field=models.CharField(
                choices=netbox_circuitmaintenance.models.CircuitMaintenanceTypeChoices.CHOICES,
                db_index=True,
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="circuitmaintenance",
            name="start",
            field=models.DateTimeField(
                db_index=True,
                help_text="Start date and time of the maintenance event e.g. 2022-12-25 14:30",
            ),
        ),
        migrations.AlterField(
            model_name="circuitmaintenance",
            name="end",
            field=models.DateTimeField(
                db_index=True,
                help_text="End date and time of the maintenance event e.g. 2022-12-26 14:30",
            ),
        ),
        migrations.AlterField(
            model_name="circuitmaintenancenotifications",
            name="subject",
            field=models.CharField(max_length=500),
        ),
    ]
