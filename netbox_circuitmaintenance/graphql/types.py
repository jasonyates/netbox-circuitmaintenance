from typing import Annotated, Optional

import strawberry
import strawberry_django
from netbox.graphql.types import NetBoxObjectType

from ..models import (
    CircuitMaintenance,
    CircuitMaintenanceImpact,
    CircuitMaintenanceNotifications,
)
from .filters import (
    CircuitMaintenanceFilter,
    CircuitMaintenanceImpactFilter,
    CircuitMaintenanceNotificationsFilter,
)


@strawberry_django.type(
    CircuitMaintenance,
    fields=[
        "id",
        "name",
        "summary",
        "status",
        "start",
        "end",
        "internal_ticket",
        "acknowledged",
        "comments",
        "created",
        "last_updated",
    ],
    filters=CircuitMaintenanceFilter,
)
class CircuitMaintenanceType(NetBoxObjectType):
    provider: Annotated["ProviderType", strawberry.lazy("circuits.graphql.types")]  # noqa: F821


@strawberry_django.type(
    CircuitMaintenanceImpact,
    fields=[
        "id",
        "impact",
        "created",
        "last_updated",
    ],
    filters=CircuitMaintenanceImpactFilter,
)
class CircuitMaintenanceImpactType(NetBoxObjectType):
    circuitmaintenance: Annotated[
        "CircuitMaintenanceType",
        strawberry.lazy("netbox_circuitmaintenance.graphql.types"),
    ]
    circuit: Annotated["CircuitType", strawberry.lazy("circuits.graphql.types")]  # noqa: F821


@strawberry_django.type(
    CircuitMaintenanceNotifications,
    fields=[
        "id",
        "email_body",
        "subject",
        "email_from",
        "email_received",
        "created",
        "last_updated",
    ],
    filters=CircuitMaintenanceNotificationsFilter,
)
class CircuitMaintenanceNotificationsType(NetBoxObjectType):
    circuitmaintenance: Optional[
        Annotated[
            "CircuitMaintenanceType",
            strawberry.lazy("netbox_circuitmaintenance.graphql.types"),
        ]
    ]
