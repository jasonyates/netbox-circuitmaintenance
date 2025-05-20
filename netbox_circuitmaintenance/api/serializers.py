from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import CircuitMaintenance, CircuitMaintenanceImpact, CircuitMaintenanceNotifications
from circuits.api.serializers import ProviderSerializer, CircuitSerializer



class NestedCircuitMaintenanceImpactSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_circuitmaintenance-api:circuitmaintenanceimpact-detail'
    )

    circuit = CircuitSerializer(nested=True)

    class Meta:
        model = CircuitMaintenanceImpact
        fields = (
            'id', 'url', 'circuit', 'impact', 'created', 'last_updated',
        )

class NestedCircuitMaintenanceSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_circuitmaintenance-api:circuitmaintenance-detail'
    )

    provider = ProviderSerializer(nested=True)

    class Meta:
        model = CircuitMaintenance
        fields = (
            'id', 'url', 'name', 'status',  'provider', 'start', 'end', 'acknowledged', 'created', 'last_updated',
        )

class NestedCircuitMaintenanceNotificationsSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_circuitmaintenance-api:circuitmaintenancenotifications-detail'
    )

    class Meta:
        model = CircuitMaintenanceNotifications
        fields = (
            'id', 'url', 'subject', 'email_from', 'email_recieved', 'created', 'last_updated',
        )


class CircuitMaintenanceSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_circuitmaintenance-api:circuitmaintenance-detail'
    )

    provider = ProviderSerializer(nested=True)
    impact = NestedCircuitMaintenanceImpactSerializer(required=False, many=True)
    notification = NestedCircuitMaintenanceNotificationsSerializer(required=False, many=True)

    class Meta:
        model = CircuitMaintenance
        fields = (
            'id', 'url', 'display', 'name', 'summary', 'status', 'provider', 'start', 'end', 'impact', 'internal_ticket', 'acknowledged', 'notification', 'comments', 'tags', 'custom_fields', 'created',
            'last_updated',
        )

class CircuitMaintenanceImpactSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_circuitmaintenance-api:circuitmaintenanceimpact-detail'
    )

    circuit = CircuitSerializer(nested=True)
    circuitmaintenance = NestedCircuitMaintenanceSerializer()

    class Meta:
        model = CircuitMaintenanceImpact
        fields = (
            'id', 'url', 'circuitmaintenance', 'circuit', 'impact', 'custom_fields', 'created', 'last_updated',
        )

class CircuitMaintenanceNotificationsSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_circuitmaintenance-api:circuitmaintenancenotifications-detail'
    )

    circuitmaintenance = NestedCircuitMaintenanceSerializer()

    class Meta:
        model = CircuitMaintenanceNotifications
        fields = (
            'id', 'url', 'circuitmaintenance', 'email_body', 'subject', 'email_from', 'email_recieved', 'created', 'last_updated',
        )
