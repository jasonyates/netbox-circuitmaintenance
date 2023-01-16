
from netbox.views import generic
from django.db.models import Count
from . import forms, models, tables

# Circuit Maintenance Views
class CircuitMaintenanceView(generic.ObjectView):
    queryset = models.CircuitMaintenance.objects.prefetch_related('impact').all()

    def get_extra_context(self, request, instance):
        # Load the maintenance event impact
        impact = models.CircuitMaintenanceImpact.objects.filter(circuitmaintenance=instance)

        # Load the maintenance event notifications
        notification = models.CircuitMaintenanceNotifications.objects.filter(circuitmaintenance=instance)

        return {
            "impacts": impact,
            "notifications": notification
        }

class CircuitMaintenanceListView(generic.ObjectListView):
    queryset = models.CircuitMaintenance.objects.annotate(
        impact_count=Count('impact')
    )
    table = tables.CircuitMaintenanceTable

class CircuitMaintenanceEditView(generic.ObjectEditView):
    queryset = models.CircuitMaintenance.objects.all()
    form = forms.CircuitMaintenanceForm

class CircuitMaintenanceDeleteView(generic.ObjectDeleteView):
    queryset = models.CircuitMaintenance.objects.all()


# Circuit Maintenance Impact views
class CircuitMaintenanceImpactEditView(generic.ObjectEditView):
    queryset = models.CircuitMaintenanceImpact.objects.all()
    form = forms.CircuitMaintenanceImpactForm

class CircuitMaintenanceImpactDeleteView(generic.ObjectDeleteView):
    queryset = models.CircuitMaintenanceImpact.objects.all()


# Circuit Maintenance Notification views
class CircuitMaintenanceNotificationsEditView(generic.ObjectEditView):
    queryset = models.CircuitMaintenanceNotifications.objects.all()
    form = forms.CircuitMaintenanceNotificationsForm

class CircuitMaintenanceNotificationsDeleteView(generic.ObjectDeleteView):
    queryset = models.CircuitMaintenanceNotifications.objects.all()

class CircuitMaintenanceNotificationView(generic.ObjectView):
    queryset = models.CircuitMaintenanceNotifications.objects.all()

# CircuitMaintenanceSchedule 
class CircuitMaintenanceScheduleView(generic.ObjectView):
    queryset = models.CircuitMaintenance.objects.all()
