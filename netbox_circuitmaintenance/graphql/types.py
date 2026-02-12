from typing import Annotated, List

import strawberry
import strawberry_django

from netbox.graphql.types import NetBoxObjectType

from ..models import (
    CircuitMaintenance,
    CircuitMaintenanceImpact,
    CircuitMaintenanceNotifications,
)


@strawberry_django.type(
    CircuitMaintenance,
    fields=[
        'id', 'name', 'summary', 'status', 'start', 'end',
        'internal_ticket', 'acknowledged', 'comments',
        'created', 'last_updated',
    ],
)
class CircuitMaintenanceType(NetBoxObjectType):
    provider: Annotated["ProviderType", strawberry.lazy('circuits.graphql.types')]


@strawberry_django.type(
    CircuitMaintenanceImpact,
    fields=[
        'id', 'impact',
        'created', 'last_updated',
    ],
)
class CircuitMaintenanceImpactType(NetBoxObjectType):
    circuitmaintenance: Annotated["CircuitMaintenanceType", strawberry.lazy('netbox_circuitmaintenance.graphql.types')]
    circuit: Annotated["CircuitType", strawberry.lazy('circuits.graphql.types')]


@strawberry_django.type(
    CircuitMaintenanceNotifications,
    fields=[
        'id', 'email_body', 'subject',
        'email_from', 'email_received',
        'created', 'last_updated',
    ],
)
class CircuitMaintenanceNotificationsType(NetBoxObjectType):
    circuitmaintenance: Annotated["CircuitMaintenanceType", strawberry.lazy('netbox_circuitmaintenance.graphql.types')]
