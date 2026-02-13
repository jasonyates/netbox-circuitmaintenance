# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NetBox plugin (v0.6.0) for tracking circuit maintenance events. Records provider maintenance windows, associates impacted circuits, stores provider notification emails, and provides calendar/dashboard views. Requires NetBox 4.4+.

Plugin base URL is `/maintenance/` (configured via `base_url` in `PluginConfig`).

## Development Commands

```bash
# Format code (isort + black)
make format

# Lint (flake8, max line length 120)
make lint

# Format + lint + unittest
make test

# Run pre-commit hooks
make pre-commit

# Clean build artifacts
make clean
```

Install dev dependencies: `pip install -e ".[dev]"`

## Build & Release

```bash
bumpver update --minor   # or --patch / --major (auto-commits, tags, pushes)
python -m build
twine upload dist/*
```

`bumpver` updates version in: `pyproject.toml`, `README.md`, `netbox_circuitmaintenance/__init__.py`

## Architecture

This is a standard NetBox plugin following Django/DRF conventions. All plugin code lives in `netbox_circuitmaintenance/`.

### Models (`models.py`)

Three models, all extending `NetBoxModel`:

- **CircuitMaintenance** — Core record. Links to `circuits.Provider` (FK). Has status choices following the [BCOP maintenance notification standard](https://github.com/jda/maintnote-std/blob/master/standard.md): TENTATIVE, CONFIRMED, CANCELLED, IN-PROCESS, COMPLETED, RE-SCHEDULED, UNKNOWN.
- **CircuitMaintenanceImpact** — Links a maintenance to a `circuits.Circuit` (FK) with impact level (NO-IMPACT, REDUCED-REDUNDANCY, DEGRADED, OUTAGE). Has `clean()` validation that prevents modifications once maintenance is COMPLETED or CANCELLED.
- **CircuitMaintenanceNotifications** — Stores raw email notifications (BinaryField) and parsed email body/metadata. Note: field is spelled `email_recieved` (typo is in the DB schema).

### REST API (`api/`)

Three ViewSets at `/api/plugins/netbox-circuitmaintenance/`:
- `circuitmaintenance/`
- `circuitmaintenanceimpact/`
- `circuitmaintenancenotifications/`

Serializers support nested creation. FilterSets mirror the main app filtersets.

### Template Extensions (`template_content.py`)

Injects maintenance tables into existing NetBox pages:
- **Circuit detail** (`circuits.circuit`) — shows active/upcoming maintenance for that circuit
- **Provider detail** (`circuits.provider`) — shows maintenance for that provider
- **Site detail** (`dcim.site`) — shows maintenance for circuits terminating at that site

### Dashboard Widgets (`widgets.py`)

- `UpcomingMaintenanceWidget` — list of upcoming/active events
- `MaintenanceCalendarWidget` — calendar view of current month

### Calendar View (`views.py`)

`CircuitMaintenanceScheduleView` renders an HTML calendar (subclassing `calendar.HTMLCalendar`) with maintenance events shown as badges. Accessible via the plugin nav menu.

### Parsers (`parsers/`)

Example AWS Lambda function (`parsers/aws-sns-lambda/`) that receives provider emails via SES→S3→SNS, parses them with the `circuit_maintenance_parser` library, and creates records via the NetBox API using `pynetbox`.

## Code Style

- Black for formatting, isort for imports
- Flake8 with max-line-length=120, max-complexity=18
- Python 3.10, 3.11, 3.12 supported
