"""
Standalone unit tests for timezone conversion logic.
These tests don't require NetBox to be installed.
"""

import unittest
import zoneinfo
from datetime import datetime


class TestTimezoneConversionLogic(unittest.TestCase):
    """Test the core timezone conversion logic used in the plugin"""

    def test_utc_to_eastern_winter(self):
        """Test UTC to Eastern (EST) conversion in winter"""
        # January 15, 2024 19:00 UTC
        utc_time = datetime(2024, 1, 15, 19, 0, 0, tzinfo=zoneinfo.ZoneInfo("UTC"))

        # Convert to America/New_York (EST in winter)
        est_time = utc_time.astimezone(zoneinfo.ZoneInfo("America/New_York"))

        # EST is UTC-5 in winter, so 19:00 UTC = 14:00 EST
        self.assertEqual(est_time.hour, 14)
        self.assertEqual(est_time.day, 15)

    def test_eastern_to_utc_winter(self):
        """Test Eastern (EST) to UTC conversion in winter"""
        # January 15, 2024 14:00 EST
        est_time = datetime(
            2024, 1, 15, 14, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")
        )

        # Convert to UTC
        utc_time = est_time.astimezone(zoneinfo.ZoneInfo("UTC"))

        # EST is UTC-5, so 14:00 EST = 19:00 UTC
        self.assertEqual(utc_time.hour, 19)
        self.assertEqual(utc_time.day, 15)

    def test_eastern_to_utc_summer(self):
        """Test Eastern (EDT) to UTC conversion in summer"""
        # July 15, 2024 14:00 EDT
        edt_time = datetime(
            2024, 7, 15, 14, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")
        )

        # Convert to UTC
        utc_time = edt_time.astimezone(zoneinfo.ZoneInfo("UTC"))

        # EDT is UTC-4 in summer, so 14:00 EDT = 18:00 UTC
        self.assertEqual(utc_time.hour, 18)
        self.assertEqual(utc_time.day, 15)

    def test_london_to_utc_winter(self):
        """Test London (GMT) to UTC conversion in winter"""
        # January 15, 2024 12:00 GMT
        london_time = datetime(
            2024, 1, 15, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/London")
        )

        # Convert to UTC
        utc_time = london_time.astimezone(zoneinfo.ZoneInfo("UTC"))

        # GMT is UTC+0 in winter
        self.assertEqual(utc_time.hour, 12)

    def test_london_to_utc_summer(self):
        """Test London (BST) to UTC conversion in summer"""
        # July 15, 2024 12:00 BST
        london_time = datetime(
            2024, 7, 15, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo("Europe/London")
        )

        # Convert to UTC
        utc_time = london_time.astimezone(zoneinfo.ZoneInfo("UTC"))

        # BST is UTC+1 in summer, so 12:00 BST = 11:00 UTC
        self.assertEqual(utc_time.hour, 11)

    def test_tokyo_to_utc(self):
        """Test Tokyo (JST) to UTC conversion"""
        # January 15, 2024 21:00 JST
        tokyo_time = datetime(
            2024, 1, 15, 21, 0, 0, tzinfo=zoneinfo.ZoneInfo("Asia/Tokyo")
        )

        # Convert to UTC
        utc_time = tokyo_time.astimezone(zoneinfo.ZoneInfo("UTC"))

        # JST is always UTC+9, so 21:00 JST = 12:00 UTC
        self.assertEqual(utc_time.hour, 12)

    def test_los_angeles_to_utc_winter(self):
        """Test Los Angeles (PST) to UTC conversion in winter"""
        # January 15, 2024 09:00 PST
        la_time = datetime(
            2024, 1, 15, 9, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/Los_Angeles")
        )

        # Convert to UTC
        utc_time = la_time.astimezone(zoneinfo.ZoneInfo("UTC"))

        # PST is UTC-8 in winter, so 09:00 PST = 17:00 UTC
        self.assertEqual(utc_time.hour, 17)

    def test_crossing_date_boundary_forward(self):
        """Test timezone conversion that crosses date boundary forward"""
        # Sydney, 2:00 AM Jan 16
        sydney_time = datetime(
            2024, 1, 16, 2, 0, 0, tzinfo=zoneinfo.ZoneInfo("Australia/Sydney")
        )

        # Convert to UTC
        utc_time = sydney_time.astimezone(zoneinfo.ZoneInfo("UTC"))

        # AEDT is UTC+11 in summer, so 02:00 Jan 16 AEDT = 15:00 Jan 15 UTC
        self.assertEqual(utc_time.day, 15)
        self.assertEqual(utc_time.hour, 15)

    def test_crossing_date_boundary_backward(self):
        """Test timezone conversion that crosses date boundary backward"""
        # Los Angeles, 8:00 PM Jan 15 PST
        la_time = datetime(
            2024, 1, 15, 20, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/Los_Angeles")
        )

        # Convert to UTC
        utc_time = la_time.astimezone(zoneinfo.ZoneInfo("UTC"))

        # PST is UTC-8, so 20:00 Jan 15 PST = 04:00 Jan 16 UTC
        self.assertEqual(utc_time.day, 16)
        self.assertEqual(utc_time.hour, 4)

    def test_naive_datetime_with_timezone_replacement(self):
        """Test converting naive datetime by adding timezone"""
        # Create naive datetime
        naive_time = datetime(2024, 1, 15, 14, 0, 0)

        # Add timezone (interpret as EST)
        est_time = naive_time.replace(tzinfo=zoneinfo.ZoneInfo("America/New_York"))

        # Convert to UTC
        utc_time = est_time.astimezone(zoneinfo.ZoneInfo("UTC"))

        # EST is UTC-5, so 14:00 EST = 19:00 UTC
        self.assertEqual(utc_time.hour, 19)

    def test_timezone_comparison(self):
        """Test comparing timezone strings"""
        tz_ny = zoneinfo.ZoneInfo("America/New_York")
        tz_utc = zoneinfo.ZoneInfo("UTC")
        tz_ny2 = zoneinfo.ZoneInfo("America/New_York")

        # Different timezones should have different string representations
        self.assertNotEqual(str(tz_ny), str(tz_utc))

        # Same timezone should match
        self.assertEqual(str(tz_ny), str(tz_ny2))

    def test_invalid_timezone_raises_exception(self):
        """Test that invalid timezone raises ZoneInfoNotFoundError"""
        with self.assertRaises(zoneinfo.ZoneInfoNotFoundError):
            zoneinfo.ZoneInfo("Invalid/Timezone")

    def test_common_timezones_exist(self):
        """Test that common timezones we use in choices are valid"""
        common_timezones = [
            "UTC",
            "GMT",
            "America/New_York",
            "America/Chicago",
            "America/Los_Angeles",
            "Europe/London",
            "Europe/Paris",
            "Europe/Berlin",
            "Asia/Tokyo",
            "Asia/Singapore",
            "Asia/Dubai",
            "Australia/Sydney",
            "Pacific/Auckland",
        ]

        for tz_name in common_timezones:
            with self.subTest(timezone=tz_name):
                # Should not raise exception
                tz = zoneinfo.ZoneInfo(tz_name)
                self.assertIsNotNone(tz)

    def test_time_delta_preserved_across_conversion(self):
        """Test that time deltas are preserved when converting timezones"""
        # Create a 4-hour maintenance window in EST
        start_est = datetime(
            2024, 1, 15, 14, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")
        )
        end_est = datetime(
            2024, 1, 15, 18, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/New_York")
        )

        # Convert both to UTC
        start_utc = start_est.astimezone(zoneinfo.ZoneInfo("UTC"))
        end_utc = end_est.astimezone(zoneinfo.ZoneInfo("UTC"))

        # Duration should remain 4 hours
        duration = end_utc - start_utc
        self.assertEqual(duration.total_seconds(), 4 * 3600)


if __name__ == "__main__":
    unittest.main()
