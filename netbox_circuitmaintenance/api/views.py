from netbox.api.viewsets import NetBoxModelViewSet

from .. import models
from .serializers import CircuitMaintenanceSerializer, CircuitMaintenanceImpactSerializer, CircuitMaintenanceNotificationsSerializer

class CircuitMaintenanceViewSet(NetBoxModelViewSet):
    queryset = models.CircuitMaintenance.objects.prefetch_related('tags')
    serializer_class = CircuitMaintenanceSerializer

class CircuitMaintenanceImpactViewSet(NetBoxModelViewSet):
    queryset = models.CircuitMaintenanceImpact.objects.prefetch_related('tags')
    serializer_class = CircuitMaintenanceImpactSerializer

class CircuitMaintenanceNotificationsViewSet(NetBoxModelViewSet):
    queryset = models.CircuitMaintenanceNotifications.objects.prefetch_related('tags')
    serializer_class = CircuitMaintenanceNotificationsSerializer