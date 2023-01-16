from django import forms
from netbox.forms import NetBoxModelForm
from utilities.forms import DateTimePicker
from .models import CircuitMaintenance, CircuitMaintenanceImpact, CircuitMaintenanceNotifications

class CircuitMaintenanceForm(NetBoxModelForm):

    class Meta:
        model = CircuitMaintenance
        fields = ('name', 'summary', 'status', 'provider', 'start', 'end', 'internal_ticket', 'acknowledged', 'comments', 'tags')
        widgets = {
            'start': DateTimePicker(),
            'end': DateTimePicker()
        }

class CircuitMaintenanceImpactForm(NetBoxModelForm):

    CircuitMaintenance.objects.all()

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
