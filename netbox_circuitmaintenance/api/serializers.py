from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import CircuitMaintenance, CircuitMaintenanceImpact, CircuitMaintenanceNotifications
from circuits.api.nested_serializers import NestedProviderSerializer, NestedCircuitSerializer



class NestedCircuitMaintenanceImpactSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_circuitmaintenance-api:circuitmaintenanceimpact-detail'
    )

    circuit = NestedCircuitSerializer()

    class Meta:
        model = CircuitMaintenanceImpact
        fields = (
            'id', 'url', 'circuit', 'impact', 'created', 'last_updated',
        )

class NestedCircuitMaintenanceSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_circuitmaintenance-api:circuitmaintenance-detail'
    )

    provider = NestedProviderSerializer()

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

    provider = NestedProviderSerializer()
    impact = NestedCircuitMaintenanceImpactSerializer(many=True)
    notification = NestedCircuitMaintenanceNotificationsSerializer(many=True)

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

    circuit = NestedCircuitSerializer()
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
