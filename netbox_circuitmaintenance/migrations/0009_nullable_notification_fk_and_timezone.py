import django.db.models.deletion
from django.db import migrations, models

import timezone_field


def set_default_timezone(apps, schema_editor):
    CircuitMaintenance = apps.get_model(
        "netbox_circuitmaintenance", "CircuitMaintenance"
    )
    CircuitMaintenance.objects.filter(time_zone="").update(time_zone="UTC")


class Migration(migrations.Migration):

    dependencies = [
        (
            "netbox_circuitmaintenance",
            "0008_v070_improvements",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="circuitmaintenancenotifications",
            name="circuitmaintenance",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="notification",
                to="netbox_circuitmaintenance.circuitmaintenance",
                verbose_name="Circuit Maintenance ID",
            ),
        ),
        migrations.AddField(
            model_name="circuitmaintenance",
            name="time_zone",
            field=timezone_field.TimeZoneField(
                default="UTC",
                help_text=(
                    "The provider's local timezone for this maintenance"
                    " (informational only; times remain in UTC)"
                ),
                verbose_name="Provider Timezone",
            ),
        ),
        migrations.RunPython(
            set_default_timezone,
            migrations.RunPython.noop,
        ),
    ]
