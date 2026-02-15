import datetime

from circuits.models import Circuit, CircuitType, Provider
from django.test import TestCase
from django.urls import reverse
from utilities.testing import ViewTestCases

from ..models import CircuitMaintenance, CircuitMaintenanceImpact
from ..views import Calendar


class CircuitMaintenanceViewTest(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
):
    model = CircuitMaintenance

    def _get_base_url(self):
        return "plugins:netbox_circuitmaintenance:circuitmaintenance_{}"

    @classmethod
    def setUpTestData(cls):
        providers = (
            Provider(name="View Provider 1", slug="view-provider-1"),
            Provider(name="View Provider 2", slug="view-provider-2"),
        )
        Provider.objects.bulk_create(providers)

        maintenances = (
            CircuitMaintenance(
                name="VIEW-MAINT-001",
                summary="View test 1",
                status="CONFIRMED",
                provider=providers[0],
                start=datetime.datetime(2025, 6, 1, 9, 0, tzinfo=datetime.timezone.utc),
                end=datetime.datetime(2025, 6, 1, 17, 0, tzinfo=datetime.timezone.utc),
            ),
            CircuitMaintenance(
                name="VIEW-MAINT-002",
                summary="View test 2",
                status="TENTATIVE",
                provider=providers[0],
                start=datetime.datetime(2025, 7, 1, 9, 0, tzinfo=datetime.timezone.utc),
                end=datetime.datetime(2025, 7, 1, 17, 0, tzinfo=datetime.timezone.utc),
            ),
            CircuitMaintenance(
                name="VIEW-MAINT-003",
                summary="View test 3",
                status="COMPLETED",
                provider=providers[1],
                start=datetime.datetime(2025, 5, 1, 9, 0, tzinfo=datetime.timezone.utc),
                end=datetime.datetime(2025, 5, 1, 17, 0, tzinfo=datetime.timezone.utc),
            ),
        )
        CircuitMaintenance.objects.bulk_create(maintenances)

        cls.form_data = {
            "name": "VIEW-MAINT-NEW",
            "summary": "New view maintenance",
            "status": "CONFIRMED",
            "provider": providers[1].pk,
            "start": datetime.datetime(2025, 8, 1, 9, 0, tzinfo=datetime.timezone.utc),
            "end": datetime.datetime(2025, 8, 1, 17, 0, tzinfo=datetime.timezone.utc),
            "acknowledged": False,
            "tags": [],
        }


class CalendarTest(TestCase):
    """Test the Calendar helper class methods."""

    def setUp(self):
        self.cal = Calendar(2025, 6)

    def test_prev_month_january(self):
        self.assertEqual(self.cal.prev_month(1), 12)

    def test_prev_month_other(self):
        self.assertEqual(self.cal.prev_month(6), 5)

    def test_next_month_december(self):
        self.assertEqual(self.cal.next_month(12), 1)

    def test_next_month_other(self):
        self.assertEqual(self.cal.next_month(6), 7)

    def test_prev_year_january(self):
        self.assertEqual(self.cal.prev_year(1, 2025), 2024)

    def test_prev_year_other_month(self):
        self.assertEqual(self.cal.prev_year(6, 2025), 2025)

    def test_next_year_december(self):
        self.assertEqual(self.cal.next_year(12, 2025), 2026)

    def test_next_year_other_month(self):
        self.assertEqual(self.cal.next_year(6, 2025), 2025)

    def test_formatmonthname(self):
        result = self.cal.formatmonthname(2025, 6)
        self.assertIn("June", result)
        self.assertIn("2025", result)

    def test_formatday_zero(self):
        """Day 0 should render empty cell."""
        result = self.cal.formatday(0, 0, [], [])
        self.assertEqual(result, "<td>&nbsp;</td>")

    def test_formatday_no_events(self):
        """Day with no events renders day number and add link."""
        result = self.cal.formatday(
            15,
            6,  # day=15, weekday=Sunday
            [],
            [datetime.date(2025, 6, 15)],
        )
        self.assertIn("<td", result)
        self.assertIn("15", result)
        self.assertIn("circuitmaintenance/add", result)
        self.assertIn("mdi-plus-circle-outline", result)

    def test_formatday_today_highlight(self):
        """Today should get the today-highlight CSS class."""
        today = datetime.date.today()
        cal = Calendar(today.year, today.month)
        result = cal.formatday(
            today.day,
            today.weekday(),
            [],
            [today],
        )
        self.assertIn("today-highlight", result)

    def test_formatday_single_day_event(self):
        """Single-day event renders as a badge."""
        provider = Provider.objects.create(name="Cal Provider", slug="cal-provider")
        maint = CircuitMaintenance.objects.create(
            name="CAL-MAINT-001",
            summary="Calendar test",
            status="CONFIRMED",
            provider=provider,
            start=datetime.datetime(2025, 6, 15, 9, 0, tzinfo=datetime.timezone.utc),
            end=datetime.datetime(2025, 6, 15, 17, 0, tzinfo=datetime.timezone.utc),
        )
        # Add impact_count annotation
        from django.db.models import Count

        events = CircuitMaintenance.objects.filter(pk=maint.pk).annotate(
            impact_count=Count("impact")
        )

        result = self.cal.formatday(
            15,
            6,
            events,
            [datetime.date(2025, 6, 15)],
        )
        self.assertIn("badge", result)
        self.assertIn("CAL-MAINT-001", result)
        self.assertIn("Cal Provider", result)
        self.assertIn("CONFIRMED", result)

    def test_formatday_multi_day_event_start(self):
        """Multi-day event start date renders spanning bar with text."""
        provider = Provider.objects.create(
            name="Cal Multi Provider", slug="cal-multi-provider"
        )
        maint = CircuitMaintenance.objects.create(
            name="CAL-MULTI-001",
            summary="Multi-day test",
            status="CONFIRMED",
            provider=provider,
            start=datetime.datetime(2025, 6, 15, 9, 0, tzinfo=datetime.timezone.utc),
            end=datetime.datetime(2025, 6, 17, 17, 0, tzinfo=datetime.timezone.utc),
        )
        from django.db.models import Count

        events = CircuitMaintenance.objects.filter(pk=maint.pk).annotate(
            impact_count=Count("impact")
        )

        week_dates = [datetime.date(2025, 6, d) for d in range(15, 22)]
        result = self.cal.formatday(
            15,
            6,
            events,
            week_dates,
        )
        self.assertIn("cal-span", result)
        self.assertIn("CAL-MULTI-001", result)

    def test_formatday_multi_day_event_continuation(self):
        """Multi-day event continuation date renders spacer."""
        provider = Provider.objects.create(
            name="Cal Cont Provider", slug="cal-cont-provider"
        )
        maint = CircuitMaintenance.objects.create(
            name="CAL-CONT-001",
            summary="Continuation test",
            status="CONFIRMED",
            provider=provider,
            start=datetime.datetime(2025, 6, 15, 9, 0, tzinfo=datetime.timezone.utc),
            end=datetime.datetime(2025, 6, 17, 17, 0, tzinfo=datetime.timezone.utc),
        )
        from django.db.models import Count

        events = CircuitMaintenance.objects.filter(pk=maint.pk).annotate(
            impact_count=Count("impact")
        )

        week_dates = [datetime.date(2025, 6, d) for d in range(15, 22)]
        result = self.cal.formatday(
            16,
            0,  # day 16 is continuation
            events,
            week_dates,
        )
        self.assertIn("cal-span-spacer", result)


class CalendarViewTest(TestCase):
    """Test the CircuitMaintenanceScheduleView."""

    def setUp(self):
        from django.contrib.contenttypes.models import ContentType
        from users.models import ObjectPermission, User

        self.user = User.objects.create_user(
            username="calviewuser", password="testpass123"
        )
        # Grant view permission
        obj_perm = ObjectPermission(
            name="Test CM View",
            actions=["view"],
        )
        obj_perm.save()
        obj_perm.object_types.add(
            *ContentType.objects.filter(
                app_label="netbox_circuitmaintenance",
                model="circuitmaintenance",
            )
        )
        obj_perm.users.add(self.user)
        self.client.login(username="calviewuser", password="testpass123")

    def test_schedule_view_get(self):
        url = reverse("plugins:netbox_circuitmaintenance:maintenanceschedule")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_schedule_view_specific_month(self):
        url = reverse("plugins:netbox_circuitmaintenance:maintenanceschedule")
        response = self.client.get(url, {"month": 3, "year": 2025})
        self.assertEqual(response.status_code, 200)
        self.assertIn("March", response.content.decode())

    def test_schedule_view_htmx(self):
        url = reverse("plugins:netbox_circuitmaintenance:maintenanceschedule")
        response = self.client.get(
            url,
            {"month": 6, "year": 2025},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        # htmx response uses partial template (no full page chrome)
        content = response.content.decode()
        self.assertIn("June", content)


class ICSFeedTest(TestCase):
    """Test the ICS/iCal feed view."""

    def setUp(self):
        self.provider = Provider.objects.create(
            name="ICS Provider", slug="ics-provider"
        )

    def test_ics_feed_content_type(self):
        url = reverse("plugins:netbox_circuitmaintenance:maintenance_ics")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/calendar", response["Content-Type"])

    def test_ics_feed_contains_events(self):
        CircuitMaintenance.objects.create(
            name="ICS-MAINT-001",
            summary="ICS test event",
            status="CONFIRMED",
            provider=self.provider,
            start=datetime.datetime.now(tz=datetime.timezone.utc),
            end=datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(hours=4),
        )
        url = reverse("plugins:netbox_circuitmaintenance:maintenance_ics")
        response = self.client.get(url)
        content = response.content.decode()
        self.assertIn("ICS-MAINT-001", content)
        self.assertIn("VCALENDAR", content)
        self.assertIn("VEVENT", content)
