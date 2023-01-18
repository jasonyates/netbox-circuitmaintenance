from netbox.api.viewsets import NetBoxModelViewSet

from .. import models, filtersets
from .serializers import CircuitMaintenanceSerializer, CircuitMaintenanceImpactSerializer, CircuitMaintenanceNotificationsSerializer

class CircuitMaintenanceViewSet(NetBoxModelViewSet):
    queryset = models.CircuitMaintenance.objects.prefetch_related('tags')
    serializer_class = CircuitMaintenanceSerializer
    filterset_class = filtersets.CircuitMaintenanceFilterSet

class CircuitMaintenanceImpactViewSet(NetBoxModelViewSet):
    queryset = models.CircuitMaintenanceImpact.objects.prefetch_related('tags')
    serializer_class = CircuitMaintenanceImpactSerializer
    filterset_class = filtersets.CircuitMaintenanceImpactFilterSet

class CircuitMaintenanceNotificationsViewSet(NetBoxModelViewSet):
    queryset = models.CircuitMaintenanceNotifications.objects.prefetch_related('tags')
    serializer_class = CircuitMaintenanceNotificationsSerializer
    filterset_class = filtersets.CircuitMaintenanceNotificationsFilterSet