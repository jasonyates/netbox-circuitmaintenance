from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "netbox_circuitmaintenance",
            "0007_alter_circuitmaintenancenotifications_options_and_more",
        ),
    ]

    operations = [
        # Fix verbose_name_plural typo
        migrations.AlterModelOptions(
            name="circuitmaintenanceimpact",
            options={
                "ordering": ("impact",),
                "verbose_name": "Circuit Maintenance Impact",
                "verbose_name_plural": "Circuit Maintenance Impact",
            },
        ),
        # Remove null=True from acknowledged BooleanField
        migrations.AlterField(
            model_name="circuitmaintenance",
            name="acknowledged",
            field=models.BooleanField(
                default=False,
                help_text="Confirm if this maintenance event has been acknowledged",
                verbose_name="Acknowledged?",
            ),
        ),
        # Remove max_length from DateTimeFields
        migrations.AlterField(
            model_name="circuitmaintenance",
            name="start",
            field=models.DateTimeField(
                help_text="Start date and time of the maintenance event e.g. 2022-12-25 14:30",
            ),
        ),
        migrations.AlterField(
            model_name="circuitmaintenance",
            name="end",
            field=models.DateTimeField(
                help_text="End date and time of the maintenance event e.g. 2022-12-26 14:30",
            ),
        ),
        # Add unique constraint for circuit + maintenance
        migrations.AddConstraint(
            model_name="circuitmaintenanceimpact",
            constraint=models.UniqueConstraint(
                fields=["circuitmaintenance", "circuit"],
                name="unique_maintenance_circuit",
            ),
        ),
        # Rename email_recieved to email_received
        migrations.RenameField(
            model_name="circuitmaintenancenotifications",
            old_name="email_recieved",
            new_name="email_received",
        ),
        # Update ordering to use renamed field
        migrations.AlterModelOptions(
            name="circuitmaintenancenotifications",
            options={
                "ordering": ("email_received",),
                "verbose_name": "Circuit Maintenance Notification",
                "verbose_name_plural": "Circuit Maintenance Notification",
            },
        ),
    ]
