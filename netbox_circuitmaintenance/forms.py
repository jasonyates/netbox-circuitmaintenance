from django import forms
from django.utils import timezone
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms.widgets import DateTimePicker
from circuits.models import Provider, Circuit
from .models import (
    CircuitMaintenance, CircuitMaintenanceImpact, CircuitMaintenanceNotifications,
    CircuitMaintenanceTypeChoices, CircuitMaintenanceImpactTypeChoices, TimeZoneChoices
)
import zoneinfo

class CircuitMaintenanceForm(NetBoxModelForm):

    provider = DynamicModelChoiceField(
        queryset=Provider.objects.all()
    )

    original_timezone = forms.ChoiceField(
        choices=TimeZoneChoices,
        required=False,
        label='Timezone',
        help_text='Timezone for the start/end times (converted to system timezone on save)'
    )

    class Meta:
        model = CircuitMaintenance
        fields = ('name', 'summary', 'status', 'provider', 'start', 'end', 'original_timezone', 'internal_ticket', 'acknowledged', 'comments', 'tags')
        widgets = {
            'start': DateTimePicker(),
            'end': DateTimePicker()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # On edit, change help text since we don't convert
        if self.instance and self.instance.pk:
            self.fields['original_timezone'].help_text = 'Original timezone from provider notification (reference only)'
            self.fields['original_timezone'].label = 'Original Timezone'

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Only convert timezone on CREATE (not on edit)
        if not instance.pk and instance.original_timezone:
            try:
                # Get the timezone objects
                original_tz = zoneinfo.ZoneInfo(instance.original_timezone)
                system_tz = timezone.get_current_timezone()

                # Convert start time if provided
                if instance.start:
                    # Make the datetime aware in the original timezone if it's naive
                    if timezone.is_naive(instance.start):
                        start_in_original_tz = instance.start.replace(tzinfo=original_tz)
                    else:
                        # If already aware, interpret it as being in the original timezone
                        start_in_original_tz = instance.start.replace(tzinfo=original_tz)
                    # Convert to system timezone
                    instance.start = start_in_original_tz.astimezone(system_tz)

                # Convert end time if provided
                if instance.end:
                    if timezone.is_naive(instance.end):
                        end_in_original_tz = instance.end.replace(tzinfo=original_tz)
                    else:
                        end_in_original_tz = instance.end.replace(tzinfo=original_tz)
                    instance.end = end_in_original_tz.astimezone(system_tz)

            except (zoneinfo.ZoneInfoNotFoundError, ValueError) as e:
                # If timezone is invalid, just save without conversion
                pass

        if commit:
            instance.save()
            self.save_m2m()

        return instance

class CircuitMaintenanceFilterForm(NetBoxModelFilterSetForm):
    model = CircuitMaintenance

    name = forms.CharField(
        required=False
    )

    summary = forms.CharField(
        required=False
    )

    provider = forms.ModelMultipleChoiceField(
        queryset=Provider.objects.all(),
        required=False
    )

    status = forms.MultipleChoiceField(
        choices=CircuitMaintenanceTypeChoices,
        required=False
    )

    start = forms.CharField(
        required=False
    )

    end = forms.CharField(
        required=False
    )

    acknowledged = forms.BooleanField(
        required=False
    )

    internal_ticket = forms.CharField(
        required=False
    )

    impact = forms.ModelMultipleChoiceField(
        queryset=CircuitMaintenanceImpact.objects.all(),
        required=False
    )


class CircuitMaintenanceImpactForm(NetBoxModelForm):

    circuit = DynamicModelChoiceField(
        queryset=Circuit.objects.all()
    )

    class Meta:
        model = CircuitMaintenanceImpact
        fields = ('circuitmaintenance', 'circuit', 'impact')

class CircuitMaintenanceNotificationsForm(NetBoxModelForm):

    class Meta:
        model = CircuitMaintenanceNotifications
        fields = ('circuitmaintenance', 'subject', 'email_from', 'email_body', 'email_recieved')
        widgets = {
            'email_recieved': DateTimePicker()
        }
