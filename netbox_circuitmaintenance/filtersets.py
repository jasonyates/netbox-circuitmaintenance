from netbox.filtersets import NetBoxModelFilterSet
from .models import CircuitMaintenance, CircuitMaintenanceImpact, CircuitMaintenanceNotifications
from django.db.models import Q

class CircuitMaintenanceFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = CircuitMaintenance
        fields = ('id', 'name', 'summary', 'status', 'provider', 'start', 'end', 'impact', 'internal_ticket', 'acknowledged', 'comments')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
        )

class CircuitMaintenanceImpactFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = CircuitMaintenanceImpact
        fields = ('id', 'circuitmaintenance', 'circuit', 'impact')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(circuit__icontains=value)
        )

class CircuitMaintenanceNotificationsFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = CircuitMaintenanceNotifications
        fields = ('id', 'email_body', 'subject', 'email_from', 'email_recieved')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(subject__icontains=value)
        )
