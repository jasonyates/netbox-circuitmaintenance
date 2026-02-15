# Changelog

## v0.8.0

### New Features
- Added maintenance summary dashboard with stats cards, 14-day timeline and grouped-by-provider tables (#2)
- Summary stat cards are clickable and link to filtered maintenance list views
- Added unmatched notifications list view for triaging orphaned parser notifications (#16)
- Notifications can now be created without an associated maintenance event (nullable FK)
- Added provider timezone field to maintenance events, defaulting to UTC (#20)
- Timezone displayed on maintenance detail page alongside start/end times
- Timezone available in create, edit, bulk edit, filter forms and REST API
- Added date range filters (`start_after` / `start_before`) to maintenance filterset
- Added "Summary", "Maintenance Calendar" and "Unmatched Notifications" to plugin navigation menu
- Renamed "Maintenance Schedule" to "Maintenance Calendar"

### Dependencies
- Added `django-timezone-field>=7.0`

### Migration Notes
- Migration `0009` makes the notification FK nullable (keeps CASCADE) and adds the `time_zone` field
- All existing maintenance events are backfilled with `UTC` as the default timezone

## v0.7.0

### Breaking Changes
- API field `email_recieved` renamed to `email_received` (typo fix)
- API serializers restructured: removed separate nested serializer classes, added `brief_fields`

### Bug Fixes
- Fixed XSS vulnerability in notification email display (now sanitised with nh3)
- Fixed DEGRADED impact badge color (`orage` -> `orange`)
- Fixed calendar year navigation (prev/next were both broken)
- Fixed calendar not showing events spanning month boundaries
- Fixed broken search in CircuitMaintenanceImpact filterset
- Fixed malformed HTML and Bootstrap 5 attributes in summary table column
- Fixed verbose_name typo (`Imapct` -> `Impact`)
- Removed invalid `max_length` parameter from DateTimeFields
- Removed unnecessary `null=True` from `acknowledged` BooleanField

### Enhancements
- Added `clone_fields` for better clone functionality (#13)
- Added date range validation (end must be after start)
- Added unique constraint preventing duplicate circuit/maintenance associations
- Added SearchIndex for global search support
- Added GraphQL type definitions (#7)
- Added ICS/iCal subscription feed (#14)
- Added historical maintenance tab on Circuit, Provider, and Site pages (#3)
- Added responsive CSS for calendar views
- Added htmx-powered calendar month navigation (no page reload)
- Added "View Full Calendar" link on dashboard widget
- Circuit dropdown in impact form now filtered by maintenance provider (#12)
- Filter form date fields now use DateTimePicker widgets
- Expanded search to include summary, provider name, and internal ticket
- Centralised active status constants (DRY)

### Dependencies
- Added `nh3>=0.2.14` (HTML sanitisation)
- Added `icalendar>=5.0.0` (ICS feed generation)

## 0.6.0 (2025-09-08)

* Netbox 4.4 support
* Bug fix by @PetrVoronov
* Highlight current date in calendar event view

## 0.5.0 (2025-06-02)

* Netbox 4.2 support

## 0.4.2 (2024-09-29)

* Adding Maintenance calendar widget
* Fix #26 - f string quote issue with NB 4.1

## 0.4.1 (2024-09-19)

* Adding Maintenance Schedule calendar


## 0.4.0 (2024-09-19)

* Adds support for Netbox 4.0 and 4.1
* Adds widget to show circuit maintenance events
* Updates styling to match new Netbox style


## 0.3.0 (2023-04-28)

* Fixed support for Netbox 3.5. NOTE: Plugin version 0.3.0+ is only compatible with Netbox 3.5+

## 0.2.2 (2023-01-18)

* Fix API Filtersets
* Viewing notification content opens a new tab
* Updating RESCHEDULED to RE-SCHEDULED to match circuitparser

## 0.2.1 (2023-01-17)

* Updating to DynamicModelChoiceField
* Hiding maintenance schedule for now

## 0.1.0 (2023-01-15)

* First release on PyPI.


