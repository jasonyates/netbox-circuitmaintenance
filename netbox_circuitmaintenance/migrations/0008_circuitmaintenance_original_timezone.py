# Generated for timezone support feature

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "netbox_circuitmaintenance",
            "0007_alter_circuitmaintenancenotifications_options_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="circuitmaintenance",
            name="original_timezone",
            field=models.CharField(
                blank=True,
                help_text="Original timezone from provider notification (e.g., America/New_York, UTC, Europe/London)",
                max_length=63,
                verbose_name="Original Timezone",
            ),
        ),
    ]
