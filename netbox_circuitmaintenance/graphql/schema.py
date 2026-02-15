from typing import List

import strawberry
import strawberry_django

from .types import (
    CircuitMaintenanceImpactType,
    CircuitMaintenanceNotificationsType,
    CircuitMaintenanceType,
)


@strawberry.type(name="Query")
class CircuitMaintenanceQuery:
    circuit_maintenance: CircuitMaintenanceType = strawberry_django.field()
    circuit_maintenance_list: List[CircuitMaintenanceType] = strawberry_django.field()

    circuit_maintenance_impact: CircuitMaintenanceImpactType = strawberry_django.field()
    circuit_maintenance_impact_list: List[CircuitMaintenanceImpactType] = (
        strawberry_django.field()
    )

    circuit_maintenance_notification: CircuitMaintenanceNotificationsType = (
        strawberry_django.field()
    )
    circuit_maintenance_notification_list: List[CircuitMaintenanceNotificationsType] = (
        strawberry_django.field()
    )


schema = [CircuitMaintenanceQuery]
