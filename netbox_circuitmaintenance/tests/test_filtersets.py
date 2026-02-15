from datetime import datetime, timezone

from django.test import TestCase

from circuits.models import Circuit, CircuitType, Provider
from utilities.testing import ChangeLoggedFilterSetTests

from ..filtersets import (
    CircuitMaintenanceFilterSet,
    CircuitMaintenanceImpactFilterSet,
    CircuitMaintenanceNotificationsFilterSet,
)
from ..models import (
    CircuitMaintenance,
    CircuitMaintenanceImpact,
    CircuitMaintenanceNotifications,
)


class CircuitMaintenanceFilterSetTest(TestCase, ChangeLoggedFilterSetTests):
    queryset = CircuitMaintenance.objects.all()
    filterset = CircuitMaintenanceFilterSet
    ignore_fields = ('provider', 'time_zone', 'start_after', 'start_before')

    @classmethod
    def setUpTestData(cls):
        providers = (
            Provider(name='Provider Alpha', slug='provider-alpha'),
            Provider(name='Provider Beta', slug='provider-beta'),
        )
        Provider.objects.bulk_create(providers)

        maintenances = (
            CircuitMaintenance(
                name='MAINT-001',
                summary='Fiber cut repair',
                status='CONFIRMED',
                provider=providers[0],
                start=datetime(2025, 6, 1, 9, 0, tzinfo=timezone.utc),
                end=datetime(2025, 6, 1, 17, 0, tzinfo=timezone.utc),
                internal_ticket='CHG-111',
                acknowledged=True,
            ),
            CircuitMaintenance(
                name='MAINT-002',
                summary='Router upgrade',
                status='TENTATIVE',
                provider=providers[0],
                start=datetime(2025, 7, 1, 9, 0, tzinfo=timezone.utc),
                end=datetime(2025, 7, 1, 17, 0, tzinfo=timezone.utc),
                internal_ticket='CHG-222',
                acknowledged=False,
            ),
            CircuitMaintenance(
                name='MAINT-003',
                summary='Switch replacement',
                status='COMPLETED',
                provider=providers[1],
                start=datetime(2025, 5, 1, 9, 0, tzinfo=timezone.utc),
                end=datetime(2025, 5, 1, 17, 0, tzinfo=timezone.utc),
                internal_ticket='CHG-333',
                acknowledged=True,
            ),
        )
        CircuitMaintenance.objects.bulk_create(maintenances)

    def test_q_name(self):
        params = {'q': 'MAINT-001'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_q_summary(self):
        params = {'q': 'Fiber cut'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_q_provider(self):
        params = {'q': 'Alpha'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_q_internal_ticket(self):
        params = {'q': 'CHG-222'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_status(self):
        params = {'status': 'CONFIRMED'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_provider(self):
        provider = Provider.objects.get(slug='provider-beta')
        params = {'provider': provider.pk}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_acknowledged(self):
        params = {'acknowledged': True}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class CircuitMaintenanceImpactFilterSetTest(TestCase, ChangeLoggedFilterSetTests):
    queryset = CircuitMaintenanceImpact.objects.all()
    filterset = CircuitMaintenanceImpactFilterSet
    ignore_fields = ('circuitmaintenance', 'circuit')

    @classmethod
    def setUpTestData(cls):
        provider = Provider.objects.create(
            name='Impact FS Provider', slug='impact-fs-provider'
        )
        circuit_type = CircuitType.objects.create(
            name='FS Transit', slug='fs-transit'
        )
        circuits = (
            Circuit(cid='FS-CID-001', provider=provider, type=circuit_type),
            Circuit(cid='FS-CID-002', provider=provider, type=circuit_type),
            Circuit(cid='FS-CID-003', provider=provider, type=circuit_type),
        )
        Circuit.objects.bulk_create(circuits)

        maintenance = CircuitMaintenance.objects.create(
            name='MAINT-FS-IMP',
            summary='FilterSet impact test',
            status='CONFIRMED',
            provider=provider,
            start=datetime(2025, 6, 1, 9, 0, tzinfo=timezone.utc),
            end=datetime(2025, 6, 1, 17, 0, tzinfo=timezone.utc),
        )

        impacts = (
            CircuitMaintenanceImpact(
                circuitmaintenance=maintenance,
                circuit=circuits[0],
                impact='OUTAGE',
            ),
            CircuitMaintenanceImpact(
                circuitmaintenance=maintenance,
                circuit=circuits[1],
                impact='DEGRADED',
            ),
            CircuitMaintenanceImpact(
                circuitmaintenance=maintenance,
                circuit=circuits[2],
                impact='NO-IMPACT',
            ),
        )
        CircuitMaintenanceImpact.objects.bulk_create(impacts)

    def test_q_circuit_cid(self):
        params = {'q': 'FS-CID-001'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_q_maintenance_name(self):
        params = {'q': 'MAINT-FS-IMP'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_impact(self):
        params = {'impact': 'OUTAGE'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)


class CircuitMaintenanceNotificationsFilterSetTest(TestCase, ChangeLoggedFilterSetTests):
    queryset = CircuitMaintenanceNotifications.objects.all()
    filterset = CircuitMaintenanceNotificationsFilterSet
    ignore_fields = ('circuitmaintenance', 'email')

    @classmethod
    def setUpTestData(cls):
        provider = Provider.objects.create(
            name='Notif FS Provider', slug='notif-fs-provider'
        )
        maintenance = CircuitMaintenance.objects.create(
            name='MAINT-FS-NOTIF',
            summary='FilterSet notification test',
            status='CONFIRMED',
            provider=provider,
            start=datetime(2025, 6, 1, 9, 0, tzinfo=timezone.utc),
            end=datetime(2025, 6, 1, 17, 0, tzinfo=timezone.utc),
        )

        notifications = (
            CircuitMaintenanceNotifications(
                circuitmaintenance=maintenance,
                email=b'raw1',
                email_body='Body one',
                subject='Planned Maintenance Window',
                email_from='noc@alpha.com',
                email_received=datetime(2025, 5, 28, 10, 0, tzinfo=timezone.utc),
            ),
            CircuitMaintenanceNotifications(
                circuitmaintenance=maintenance,
                email=b'raw2',
                email_body='Body two',
                subject='Emergency Maintenance',
                email_from='alerts@beta.com',
                email_received=datetime(2025, 5, 29, 10, 0, tzinfo=timezone.utc),
            ),
            CircuitMaintenanceNotifications(
                circuitmaintenance=maintenance,
                email=b'raw3',
                email_body='Body three',
                subject='Maintenance Complete',
                email_from='noc@alpha.com',
                email_received=datetime(2025, 5, 30, 10, 0, tzinfo=timezone.utc),
            ),
        )
        CircuitMaintenanceNotifications.objects.bulk_create(notifications)

    def test_q_subject(self):
        params = {'q': 'Emergency'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_q_email_from(self):
        params = {'q': 'alpha.com'}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
