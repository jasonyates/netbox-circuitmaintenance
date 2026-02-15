from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms.widgets import DateTimePicker
from timezone_field import TimeZoneFormField
from circuits.models import Provider, Circuit
from .models import CircuitMaintenance, CircuitMaintenanceImpact, CircuitMaintenanceNotifications, CircuitMaintenanceTypeChoices, CircuitMaintenanceImpactTypeChoices

class CircuitMaintenanceForm(NetBoxModelForm):

    provider = DynamicModelChoiceField(
        queryset=Provider.objects.all()
    )

    time_zone = TimeZoneFormField(
        required=False,
    )

    class Meta:
        model = CircuitMaintenance
        fields = ('name', 'summary', 'status', 'provider', 'start', 'end', 'time_zone', 'internal_ticket', 'acknowledged', 'comments', 'tags')
        widgets = {
            'start': DateTimePicker(),
            'end': DateTimePicker()
        }

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

    start_after = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(),
        label='Start After',
    )

    start_before = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(),
        label='Start Before',
    )

    acknowledged = forms.BooleanField(
        required=False
    )

    internal_ticket = forms.CharField(
        required=False
    )

    time_zone = TimeZoneFormField(
        required=False,
    )


class CircuitMaintenanceBulkEditForm(NetBoxModelBulkEditForm):
    model = CircuitMaintenance

    status = forms.ChoiceField(
        choices=CircuitMaintenanceTypeChoices,
        required=False,
    )
    acknowledged = forms.NullBooleanField(
        required=False,
    )
    time_zone = TimeZoneFormField(
        required=False,
    )

    nullable_fields = ()


class CircuitMaintenanceImpactForm(NetBoxModelForm):

    circuitmaintenance = DynamicModelChoiceField(
        queryset=CircuitMaintenance.objects.all(),
    )

    circuit = DynamicModelChoiceField(
        queryset=Circuit.objects.all(),
        query_params={
            'provider_id': '$circuitmaintenance__provider',
        }
    )

    class Meta:
        model = CircuitMaintenanceImpact
        fields = ('circuitmaintenance', 'circuit', 'impact')


class CircuitMaintenanceNotificationsForm(NetBoxModelForm):

    circuitmaintenance = DynamicModelChoiceField(
        queryset=CircuitMaintenance.objects.all(),
        required=False,
        label="Circuit Maintenance",
    )

    class Meta:
        model = CircuitMaintenanceNotifications
        fields = ('circuitmaintenance', 'subject', 'email_from', 'email_body', 'email_received')
        widgets = {
            'email_received': DateTimePicker()
        }


class CircuitMaintenanceNotificationsFilterForm(NetBoxModelFilterSetForm):
    model = CircuitMaintenanceNotifications

    subject = forms.CharField(
        required=False
    )

    email_from = forms.CharField(
        required=False
    )

    circuitmaintenance = DynamicModelChoiceField(
        queryset=CircuitMaintenance.objects.all(),
        required=False,
        label="Maintenance",
    )

    has_maintenance = forms.NullBooleanField(
        required=False,
        label="Associated to Maintenance?",
    )
