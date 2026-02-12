from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from .models import (
    CircuitMaintenance,
    CircuitMaintenanceImpact,
    CircuitMaintenanceNotifications,
)


class CircuitMaintenanceFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = CircuitMaintenance
        fields = (
            'id', 'name', 'summary', 'status', 'provider', 'start', 'end',
            'internal_ticket', 'acknowledged',
        )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
            | Q(summary__icontains=value)
            | Q(provider__name__icontains=value)
            | Q(internal_ticket__icontains=value)
        )


class CircuitMaintenanceImpactFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = CircuitMaintenanceImpact
        fields = ('id', 'circuitmaintenance', 'circuit', 'impact')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(circuit__cid__icontains=value)
            | Q(circuitmaintenance__name__icontains=value)
        )


class CircuitMaintenanceNotificationsFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = CircuitMaintenanceNotifications
        fields = ('id', 'email_body', 'subject', 'email_from', 'email_received')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(subject__icontains=value)
            | Q(email_from__icontains=value)
        )
