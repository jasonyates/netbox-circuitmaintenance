from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms.widgets import DateTimePicker
from circuits.models import Provider, Circuit
from .models import CircuitMaintenance, CircuitMaintenanceImpact, CircuitMaintenanceNotifications, CircuitMaintenanceTypeChoices, CircuitMaintenanceImpactTypeChoices

class CircuitMaintenanceForm(NetBoxModelForm):

    provider = DynamicModelChoiceField(
        queryset=Provider.objects.all()
    )

    class Meta:
        model = CircuitMaintenance
        fields = ('name', 'summary', 'status', 'provider', 'start', 'end', 'internal_ticket', 'acknowledged', 'comments', 'tags')
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

    start = forms.DateTimeField(
        required=False,
        widget=DateTimePicker()
    )

    end = forms.DateTimeField(
        required=False,
        widget=DateTimePicker()
    )

    acknowledged = forms.BooleanField(
        required=False
    )

    internal_ticket = forms.CharField(
        required=False
    )


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

    class Meta:
        model = CircuitMaintenanceNotifications
        fields = ('circuitmaintenance', 'subject', 'email_from', 'email_body', 'email_received')
        widgets = {
            'email_received': DateTimePicker()
        }
