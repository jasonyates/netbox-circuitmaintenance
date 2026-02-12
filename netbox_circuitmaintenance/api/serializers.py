from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from ..models import (
    CircuitMaintenance,
    CircuitMaintenanceImpact,
    CircuitMaintenanceNotifications,
)
from circuits.api.serializers import CircuitSerializer, ProviderSerializer


class CircuitMaintenanceSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_circuitmaintenance-api:circuitmaintenance-detail'
    )
    provider = ProviderSerializer(nested=True)

    class Meta:
        model = CircuitMaintenance
        fields = (
            'id', 'url', 'display', 'name', 'summary', 'status', 'provider',
            'start', 'end', 'internal_ticket', 'acknowledged', 'comments',
            'tags', 'custom_fields', 'created', 'last_updated',
        )
        brief_fields = ('id', 'url', 'display', 'name', 'status', 'provider', 'start', 'end')


class CircuitMaintenanceImpactSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_circuitmaintenance-api:circuitmaintenanceimpact-detail'
    )
    circuit = CircuitSerializer(nested=True)
    circuitmaintenance = CircuitMaintenanceSerializer(nested=True)

    class Meta:
        model = CircuitMaintenanceImpact
        fields = (
            'id', 'url', 'display', 'circuitmaintenance', 'circuit', 'impact',
            'custom_fields', 'created', 'last_updated',
        )
        brief_fields = ('id', 'url', 'display', 'circuit', 'impact')


class CircuitMaintenanceNotificationsSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_circuitmaintenance-api:circuitmaintenancenotifications-detail'
    )
    circuitmaintenance = CircuitMaintenanceSerializer(nested=True)

    class Meta:
        model = CircuitMaintenanceNotifications
        fields = (
            'id', 'url', 'display', 'circuitmaintenance', 'email_body',
            'subject', 'email_from', 'email_received', 'created', 'last_updated',
        )
        brief_fields = ('id', 'url', 'display', 'subject', 'email_from', 'email_received')
