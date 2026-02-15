from datetime import datetime, timezone

from circuits.models import Circuit, CircuitType, Provider
from utilities.testing import APIViewTestCases

from ..models import (
    CircuitMaintenance,
    CircuitMaintenanceImpact,
    CircuitMaintenanceNotifications,
)


class CircuitMaintenanceAPITest(APIViewTestCases.APIViewTestCase):
    model = CircuitMaintenance
    view_namespace = "plugins-api:netbox_circuitmaintenance"
    brief_fields = [
        "display",
        "end",
        "id",
        "name",
        "provider",
        "start",
        "status",
        "url",
    ]
    bulk_update_data = {
        "status": "TENTATIVE",
        "acknowledged": True,
    }
    user_permissions = ("circuits.view_provider",)

    @classmethod
    def setUpTestData(cls):
        providers = (
            Provider(name="API Provider 1", slug="api-provider-1"),
            Provider(name="API Provider 2", slug="api-provider-2"),
        )
        Provider.objects.bulk_create(providers)

        maintenances = (
            CircuitMaintenance(
                name="API-MAINT-001",
                summary="API test 1",
                status="CONFIRMED",
                provider=providers[0],
                start=datetime(2025, 6, 1, 9, 0, tzinfo=timezone.utc),
                end=datetime(2025, 6, 1, 17, 0, tzinfo=timezone.utc),
            ),
            CircuitMaintenance(
                name="API-MAINT-002",
                summary="API test 2",
                status="TENTATIVE",
                provider=providers[0],
                start=datetime(2025, 7, 1, 9, 0, tzinfo=timezone.utc),
                end=datetime(2025, 7, 1, 17, 0, tzinfo=timezone.utc),
            ),
            CircuitMaintenance(
                name="API-MAINT-003",
                summary="API test 3",
                status="COMPLETED",
                provider=providers[1],
                start=datetime(2025, 5, 1, 9, 0, tzinfo=timezone.utc),
                end=datetime(2025, 5, 1, 17, 0, tzinfo=timezone.utc),
            ),
        )
        CircuitMaintenance.objects.bulk_create(maintenances)

        cls.create_data = [
            {
                "name": "API-MAINT-004",
                "summary": "API create 1",
                "status": "CONFIRMED",
                "provider": providers[1].pk,
                "start": datetime(2025, 8, 1, 9, 0, tzinfo=timezone.utc),
                "end": datetime(2025, 8, 1, 17, 0, tzinfo=timezone.utc),
            },
            {
                "name": "API-MAINT-005",
                "summary": "API create 2",
                "status": "TENTATIVE",
                "provider": providers[1].pk,
                "start": datetime(2025, 9, 1, 9, 0, tzinfo=timezone.utc),
                "end": datetime(2025, 9, 1, 17, 0, tzinfo=timezone.utc),
            },
            {
                "name": "API-MAINT-006",
                "summary": "API create 3",
                "status": "CONFIRMED",
                "provider": providers[1].pk,
                "start": datetime(2025, 10, 1, 9, 0, tzinfo=timezone.utc),
                "end": datetime(2025, 10, 1, 17, 0, tzinfo=timezone.utc),
            },
        ]


class CircuitMaintenanceImpactAPITest(APIViewTestCases.APIViewTestCase):
    model = CircuitMaintenanceImpact
    view_namespace = "plugins-api:netbox_circuitmaintenance"
    brief_fields = ["circuit", "display", "id", "impact", "url"]
    bulk_update_data = {
        "impact": "REDUCED-REDUNDANCY",
    }
    user_permissions = (
        "circuits.view_provider",
        "circuits.view_circuit",
        "circuits.view_circuittype",
        "netbox_circuitmaintenance.view_circuitmaintenance",
    )

    @classmethod
    def setUpTestData(cls):
        provider = Provider.objects.create(
            name="Impact API Provider", slug="impact-api-provider"
        )
        circuit_type = CircuitType.objects.create(
            name="API Transit", slug="api-transit"
        )
        circuits = (
            Circuit(cid="API-CID-001", provider=provider, type=circuit_type),
            Circuit(cid="API-CID-002", provider=provider, type=circuit_type),
            Circuit(cid="API-CID-003", provider=provider, type=circuit_type),
            Circuit(cid="API-CID-004", provider=provider, type=circuit_type),
            Circuit(cid="API-CID-005", provider=provider, type=circuit_type),
            Circuit(cid="API-CID-006", provider=provider, type=circuit_type),
        )
        Circuit.objects.bulk_create(circuits)

        maintenance = CircuitMaintenance.objects.create(
            name="API-IMP-MAINT",
            summary="Impact API test",
            status="CONFIRMED",
            provider=provider,
            start=datetime(2025, 6, 1, 9, 0, tzinfo=timezone.utc),
            end=datetime(2025, 6, 1, 17, 0, tzinfo=timezone.utc),
        )

        impacts = (
            CircuitMaintenanceImpact(
                circuitmaintenance=maintenance,
                circuit=circuits[0],
                impact="OUTAGE",
            ),
            CircuitMaintenanceImpact(
                circuitmaintenance=maintenance,
                circuit=circuits[1],
                impact="DEGRADED",
            ),
            CircuitMaintenanceImpact(
                circuitmaintenance=maintenance,
                circuit=circuits[2],
                impact="NO-IMPACT",
            ),
        )
        CircuitMaintenanceImpact.objects.bulk_create(impacts)

        cls.create_data = [
            {
                "circuitmaintenance": maintenance.pk,
                "circuit": circuits[3].pk,
                "impact": "OUTAGE",
            },
            {
                "circuitmaintenance": maintenance.pk,
                "circuit": circuits[4].pk,
                "impact": "DEGRADED",
            },
            {
                "circuitmaintenance": maintenance.pk,
                "circuit": circuits[5].pk,
                "impact": "NO-IMPACT",
            },
        ]


class CircuitMaintenanceNotificationsAPITest(APIViewTestCases.APIViewTestCase):
    model = CircuitMaintenanceNotifications
    view_namespace = "plugins-api:netbox_circuitmaintenance"
    brief_fields = ["display", "email_from", "email_received", "id", "subject", "url"]
    bulk_update_data = {
        "subject": "Updated Subject",
    }
    validation_excluded_fields = ["email"]
    user_permissions = (
        "circuits.view_provider",
        "netbox_circuitmaintenance.view_circuitmaintenance",
    )

    @classmethod
    def setUpTestData(cls):
        provider = Provider.objects.create(
            name="Notif API Provider", slug="notif-api-provider"
        )
        maintenance = CircuitMaintenance.objects.create(
            name="API-NOTIF-MAINT",
            summary="Notification API test",
            status="CONFIRMED",
            provider=provider,
            start=datetime(2025, 6, 1, 9, 0, tzinfo=timezone.utc),
            end=datetime(2025, 6, 1, 17, 0, tzinfo=timezone.utc),
        )

        notifications = (
            CircuitMaintenanceNotifications(
                circuitmaintenance=maintenance,
                email=b"raw1",
                email_body="Body 1",
                subject="API Notification 1",
                email_from="noc1@provider.com",
                email_received=datetime(2025, 5, 28, 10, 0, tzinfo=timezone.utc),
            ),
            CircuitMaintenanceNotifications(
                circuitmaintenance=maintenance,
                email=b"raw2",
                email_body="Body 2",
                subject="API Notification 2",
                email_from="noc2@provider.com",
                email_received=datetime(2025, 5, 29, 10, 0, tzinfo=timezone.utc),
            ),
            CircuitMaintenanceNotifications(
                circuitmaintenance=maintenance,
                email=b"raw3",
                email_body="Body 3",
                subject="API Notification 3",
                email_from="noc3@provider.com",
                email_received=datetime(2025, 5, 30, 10, 0, tzinfo=timezone.utc),
            ),
        )
        CircuitMaintenanceNotifications.objects.bulk_create(notifications)

        cls.create_data = [
            {
                "circuitmaintenance": maintenance.pk,
                "email_body": "Body 4",
                "subject": "API Notification 4",
                "email_from": "noc4@provider.com",
                "email_received": datetime(2025, 5, 31, 10, 0, tzinfo=timezone.utc),
            },
            {
                "circuitmaintenance": maintenance.pk,
                "email_body": "Body 5",
                "subject": "API Notification 5",
                "email_from": "noc5@provider.com",
                "email_received": datetime(2025, 6, 1, 10, 0, tzinfo=timezone.utc),
            },
            {
                "circuitmaintenance": maintenance.pk,
                "email_body": "Body 6",
                "subject": "API Notification 6",
                "email_from": "noc6@provider.com",
                "email_received": datetime(2025, 6, 2, 10, 0, tzinfo=timezone.utc),
            },
        ]
