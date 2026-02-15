import strawberry_django
from netbox.graphql.filters import NetBoxModelFilter

from ..models import (
    CircuitMaintenance,
    CircuitMaintenanceImpact,
    CircuitMaintenanceNotifications,
)


@strawberry_django.filter_type(CircuitMaintenance, lookups=True)
class CircuitMaintenanceFilter(NetBoxModelFilter):
    pass


@strawberry_django.filter_type(CircuitMaintenanceImpact, lookups=True)
class CircuitMaintenanceImpactFilter(NetBoxModelFilter):
    pass


@strawberry_django.filter_type(CircuitMaintenanceNotifications, lookups=True)
class CircuitMaintenanceNotificationsFilter(NetBoxModelFilter):
    pass
