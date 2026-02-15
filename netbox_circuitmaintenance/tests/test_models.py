from datetime import datetime, timezone

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from circuits.models import Circuit, CircuitType, Provider

from ..models import (
    CircuitMaintenance,
    CircuitMaintenanceImpact,
    CircuitMaintenanceNotifications,
)


class CircuitMaintenanceModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.provider = Provider.objects.create(
            name='Test Provider', slug='test-provider'
        )
        cls.maintenance = CircuitMaintenance.objects.create(
            name='MAINT-001',
            summary='Test maintenance event',
            status='CONFIRMED',
            provider=cls.provider,
            start=datetime(2025, 6, 1, 9, 0, tzinfo=timezone.utc),
            end=datetime(2025, 6, 1, 17, 0, tzinfo=timezone.utc),
            internal_ticket='CHG-12345',
            acknowledged=True,
        )

    def test_create_maintenance(self):
        self.assertEqual(self.maintenance.name, 'MAINT-001')
        self.assertEqual(self.maintenance.summary, 'Test maintenance event')
        self.assertEqual(self.maintenance.status, 'CONFIRMED')
        self.assertEqual(self.maintenance.provider, self.provider)
        self.assertEqual(self.maintenance.internal_ticket, 'CHG-12345')
        self.assertTrue(self.maintenance.acknowledged)

    def test_str_returns_name(self):
        self.assertEqual(str(self.maintenance), 'MAINT-001')

    def test_get_absolute_url(self):
        url = self.maintenance.get_absolute_url()
        self.assertEqual(
            url,
            f'/plugins/maintenance/circuitmaintenance/{self.maintenance.pk}/'
        )

    def test_get_status_color(self):
        status_colors = {
            'TENTATIVE': 'yellow',
            'CONFIRMED': 'green',
            'CANCELLED': 'blue',
            'IN-PROCESS': 'orange',
            'COMPLETED': 'indigo',
            'RE-SCHEDULED': 'green',
            'UNKNOWN': 'blue',
        }
        for status, expected_color in status_colors.items():
            self.maintenance.status = status
            self.assertEqual(
                self.maintenance.get_status_color(), expected_color,
                f'Status {status} should return color {expected_color}'
            )

    def test_clean_end_before_start(self):
        m = CircuitMaintenance(
            name='MAINT-BAD',
            summary='Bad dates',
            status='CONFIRMED',
            provider=self.provider,
            start=datetime(2025, 6, 2, 9, 0, tzinfo=timezone.utc),
            end=datetime(2025, 6, 1, 9, 0, tzinfo=timezone.utc),
        )
        with self.assertRaises(ValidationError) as cm:
            m.clean()
        self.assertIn('end', cm.exception.message_dict)

    def test_clean_end_equals_start(self):
        m = CircuitMaintenance(
            name='MAINT-EQUAL',
            summary='Equal dates',
            status='CONFIRMED',
            provider=self.provider,
            start=datetime(2025, 6, 1, 9, 0, tzinfo=timezone.utc),
            end=datetime(2025, 6, 1, 9, 0, tzinfo=timezone.utc),
        )
        with self.assertRaises(ValidationError):
            m.clean()

    def test_clean_valid_dates(self):
        m = CircuitMaintenance(
            name='MAINT-OK',
            summary='Good dates',
            status='CONFIRMED',
            provider=self.provider,
            start=datetime(2025, 6, 1, 9, 0, tzinfo=timezone.utc),
            end=datetime(2025, 6, 1, 17, 0, tzinfo=timezone.utc),
        )
        # Should not raise
        m.clean()

    def test_clone_fields(self):
        expected = ('status', 'provider', 'acknowledged', 'time_zone')
        self.assertEqual(CircuitMaintenance.clone_fields, expected)


class CircuitMaintenanceImpactModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.provider = Provider.objects.create(
            name='Impact Provider', slug='impact-provider'
        )
        cls.circuit_type = CircuitType.objects.create(
            name='Transit', slug='transit'
        )
        cls.circuit = Circuit.objects.create(
            cid='CID-001',
            provider=cls.provider,
            type=cls.circuit_type,
        )
        cls.circuit2 = Circuit.objects.create(
            cid='CID-002',
            provider=cls.provider,
            type=cls.circuit_type,
        )
        cls.maintenance = CircuitMaintenance.objects.create(
            name='MAINT-IMP-001',
            summary='Impact test',
            status='CONFIRMED',
            provider=cls.provider,
            start=datetime(2025, 6, 1, 9, 0, tzinfo=timezone.utc),
            end=datetime(2025, 6, 1, 17, 0, tzinfo=timezone.utc),
        )
        cls.impact = CircuitMaintenanceImpact.objects.create(
            circuitmaintenance=cls.maintenance,
            circuit=cls.circuit,
            impact='OUTAGE',
        )

    def test_create_impact(self):
        self.assertEqual(self.impact.circuitmaintenance, self.maintenance)
        self.assertEqual(self.impact.circuit, self.circuit)
        self.assertEqual(self.impact.impact, 'OUTAGE')

    def test_str_format(self):
        expected = f'{self.maintenance.name} - {self.circuit.cid}'
        self.assertEqual(str(self.impact), expected)

    def test_get_impact_color(self):
        impact_colors = {
            'NO-IMPACT': 'green',
            'REDUCED-REDUNDANCY': 'yellow',
            'DEGRADED': 'orange',
            'OUTAGE': 'red',
        }
        for impact_level, expected_color in impact_colors.items():
            self.impact.impact = impact_level
            self.assertEqual(
                self.impact.get_impact_color(), expected_color,
                f'Impact {impact_level} should return color {expected_color}'
            )

    def test_clean_completed_maintenance(self):
        self.maintenance.status = 'COMPLETED'
        self.maintenance.save()
        impact = CircuitMaintenanceImpact(
            circuitmaintenance=self.maintenance,
            circuit=self.circuit2,
            impact='OUTAGE',
        )
        with self.assertRaises(ValidationError):
            impact.clean()
        # Restore status for other tests
        self.maintenance.status = 'CONFIRMED'
        self.maintenance.save()

    def test_clean_cancelled_maintenance(self):
        self.maintenance.status = 'CANCELLED'
        self.maintenance.save()
        impact = CircuitMaintenanceImpact(
            circuitmaintenance=self.maintenance,
            circuit=self.circuit2,
            impact='OUTAGE',
        )
        with self.assertRaises(ValidationError):
            impact.clean()
        self.maintenance.status = 'CONFIRMED'
        self.maintenance.save()

    def test_clean_active_maintenance(self):
        impact = CircuitMaintenanceImpact(
            circuitmaintenance=self.maintenance,
            circuit=self.circuit2,
            impact='DEGRADED',
        )
        # Should not raise
        impact.clean()

    def test_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            CircuitMaintenanceImpact.objects.create(
                circuitmaintenance=self.maintenance,
                circuit=self.circuit,
                impact='DEGRADED',
            )

    def test_get_absolute_url(self):
        url = self.impact.get_absolute_url()
        self.assertEqual(
            url,
            f'/plugins/maintenance/circuitmaintenance/{self.maintenance.pk}/'
        )


class CircuitMaintenanceNotificationsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.provider = Provider.objects.create(
            name='Notif Provider', slug='notif-provider'
        )
        cls.maintenance = CircuitMaintenance.objects.create(
            name='MAINT-NOTIF-001',
            summary='Notification test',
            status='CONFIRMED',
            provider=cls.provider,
            start=datetime(2025, 6, 1, 9, 0, tzinfo=timezone.utc),
            end=datetime(2025, 6, 1, 17, 0, tzinfo=timezone.utc),
        )
        cls.notification = CircuitMaintenanceNotifications.objects.create(
            circuitmaintenance=cls.maintenance,
            email=b'raw email bytes',
            email_body='Maintenance will occur on your circuit.',
            subject='Scheduled Maintenance Notice',
            email_from='noc@provider.com',
            email_received=datetime(2025, 5, 28, 10, 0, tzinfo=timezone.utc),
        )

    def test_create_notification(self):
        self.assertEqual(self.notification.circuitmaintenance, self.maintenance)
        self.assertEqual(self.notification.subject, 'Scheduled Maintenance Notice')
        self.assertEqual(self.notification.email_from, 'noc@provider.com')

    def test_str_returns_subject(self):
        self.assertEqual(str(self.notification), 'Scheduled Maintenance Notice')

    def test_get_absolute_url(self):
        url = self.notification.get_absolute_url()
        self.assertEqual(
            url,
            f'/plugins/maintenance/circuitnotification/{self.notification.pk}/'
        )
