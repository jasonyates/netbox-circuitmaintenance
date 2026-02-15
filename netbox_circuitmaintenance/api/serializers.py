from circuits.api.serializers import CircuitSerializer, ProviderSerializer
from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from ..models import (
    CircuitMaintenance,
    CircuitMaintenanceImpact,
    CircuitMaintenanceNotifications,
)


class CircuitMaintenanceSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_circuitmaintenance-api:circuitmaintenance-detail"
    )
    provider = ProviderSerializer(nested=True)
    time_zone = TimeZoneSerializerField(required=False)

    class Meta:
        model = CircuitMaintenance
        fields = (
            "id",
            "url",
            "display",
            "name",
            "summary",
            "status",
            "provider",
            "start",
            "end",
            "time_zone",
            "internal_ticket",
            "acknowledged",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "id",
            "url",
            "display",
            "name",
            "status",
            "provider",
            "start",
            "end",
        )


class CircuitMaintenanceImpactSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_circuitmaintenance-api:circuitmaintenanceimpact-detail"
    )
    circuit = CircuitSerializer(nested=True)
    circuitmaintenance = CircuitMaintenanceSerializer(nested=True)

    class Meta:
        model = CircuitMaintenanceImpact
        fields = (
            "id",
            "url",
            "display",
            "circuitmaintenance",
            "circuit",
            "impact",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = ("id", "url", "display", "circuit", "impact")


class CircuitMaintenanceNotificationsSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_circuitmaintenance-api:circuitmaintenancenotifications-detail"
    )
    circuitmaintenance = CircuitMaintenanceSerializer(
        nested=True, required=False, allow_null=True
    )

    class Meta:
        model = CircuitMaintenanceNotifications
        fields = (
            "id",
            "url",
            "display",
            "circuitmaintenance",
            "email_body",
            "subject",
            "email_from",
            "email_received",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = (
            "id",
            "url",
            "display",
            "subject",
            "email_from",
            "email_received",
        )
