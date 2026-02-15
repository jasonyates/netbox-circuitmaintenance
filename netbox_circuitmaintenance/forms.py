from circuits.models import Circuit, Provider
from django import forms
from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelForm,
    NetBoxModelImportForm,
)
from timezone_field import TimeZoneFormField
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES
from utilities.forms.fields import (
    CSVChoiceField,
    CSVModelChoiceField,
    DynamicModelChoiceField,
)
from utilities.forms.widgets import DateTimePicker

from .models import (
    CircuitMaintenance,
    CircuitMaintenanceImpact,
    CircuitMaintenanceNotifications,
    CircuitMaintenanceTypeChoices,
)


class CircuitMaintenanceForm(NetBoxModelForm):

    provider = DynamicModelChoiceField(queryset=Provider.objects.all())

    time_zone = TimeZoneFormField(
        required=False,
    )

    class Meta:
        model = CircuitMaintenance
        fields = (
            "name",
            "summary",
            "status",
            "provider",
            "start",
            "end",
            "time_zone",
            "internal_ticket",
            "acknowledged",
            "comments",
            "tags",
        )
        widgets = {"start": DateTimePicker(), "end": DateTimePicker()}


class CircuitMaintenanceImportForm(NetBoxModelImportForm):
    provider = CSVModelChoiceField(
        queryset=Provider.objects.all(),
        to_field_name="name",
    )
    status = CSVChoiceField(
        choices=CircuitMaintenanceTypeChoices,
    )

    class Meta:
        model = CircuitMaintenance
        fields = (
            "name",
            "summary",
            "status",
            "provider",
            "start",
            "end",
            "internal_ticket",
            "acknowledged",
            "comments",
            "tags",
        )


class CircuitMaintenanceFilterForm(NetBoxModelFilterSetForm):
    model = CircuitMaintenance

    name = forms.CharField(required=False)

    summary = forms.CharField(required=False)

    provider = forms.ModelMultipleChoiceField(
        queryset=Provider.objects.all(), required=False
    )

    status = forms.MultipleChoiceField(
        choices=CircuitMaintenanceTypeChoices, required=False
    )

    start_after = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(),
        label="Start After",
    )

    start_before = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(),
        label="Start Before",
    )

    acknowledged = forms.NullBooleanField(
        required=False,
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )

    internal_ticket = forms.CharField(required=False)

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
            "provider_id": "$circuitmaintenance__provider",
        },
    )

    class Meta:
        model = CircuitMaintenanceImpact
        fields = ("circuitmaintenance", "circuit", "impact")


class CircuitMaintenanceNotificationsForm(NetBoxModelForm):

    circuitmaintenance = DynamicModelChoiceField(
        queryset=CircuitMaintenance.objects.all(),
        required=False,
        label="Circuit Maintenance",
    )

    class Meta:
        model = CircuitMaintenanceNotifications
        fields = (
            "circuitmaintenance",
            "subject",
            "email_from",
            "email_body",
            "email_received",
        )
        widgets = {"email_received": DateTimePicker()}


class CircuitMaintenanceNotificationsFilterForm(NetBoxModelFilterSetForm):
    model = CircuitMaintenanceNotifications

    subject = forms.CharField(required=False)

    email_from = forms.CharField(required=False)

    circuitmaintenance = DynamicModelChoiceField(
        queryset=CircuitMaintenance.objects.all(),
        required=False,
        label="Maintenance",
    )

    has_maintenance = forms.NullBooleanField(
        required=False,
        label="Associated to Maintenance?",
        widget=forms.Select(choices=BOOLEAN_WITH_BLANK_CHOICES),
    )
