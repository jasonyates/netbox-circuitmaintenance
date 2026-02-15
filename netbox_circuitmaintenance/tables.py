import django_tables2 as tables

from netbox.tables import NetBoxTable, columns
from .models import CircuitMaintenance, CircuitMaintenanceImpact, CircuitMaintenanceNotifications


class CircuitMaintenanceTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )

    provider = tables.Column(
        linkify=True
    )

    status = columns.ChoiceFieldColumn()

    impact_count = tables.Column(verbose_name="Impacted Circuits")

    summary = tables.TemplateColumn(
        '<span data-bs-toggle="tooltip" title="{{ record.summary }}">{{ record.summary|truncatewords:15 }}</span>'
    )

    class Meta(NetBoxTable.Meta):
        model = CircuitMaintenance
        fields = ('pk', 'id', 'name', 'summary', 'status', 'provider', 'start', 'end', 'time_zone', 'internal_ticket', 'acknowledged', 'impact_count', 'actions')
        default_columns = ('name', 'summary', 'provider', 'start', 'end', 'acknowledged', 'internal_ticket', 'status', 'impact_count')


class CircuitMaintenanceImpactTable(NetBoxTable):
    pk = None
    circuitmaintenance = tables.Column(
        verbose_name='Maintenance ID',
        linkify=True,
    )
    maintenance_start = tables.Column(
        verbose_name='Start',
        accessor=tables.A('circuitmaintenance__start'),
    )
    maintenance_end = tables.Column(
        verbose_name='End',
        accessor=tables.A('circuitmaintenance__end'),
    )
    maintenance_status = tables.Column(
        verbose_name='Status',
        accessor=tables.A('circuitmaintenance__status'),
    )
    impact = columns.ChoiceFieldColumn()
    actions = columns.ActionsColumn(actions=())

    class Meta(NetBoxTable.Meta):
        model = CircuitMaintenanceImpact
        fields = ('circuitmaintenance', 'maintenance_start', 'maintenance_end', 'maintenance_status', 'impact')
        default_columns = ('circuitmaintenance', 'maintenance_start', 'maintenance_end', 'maintenance_status', 'impact')


class CircuitMaintenanceImpactWithCircuitTable(CircuitMaintenanceImpactTable):
    circuit = tables.Column(
        linkify=True,
    )

    class Meta(CircuitMaintenanceImpactTable.Meta):
        fields = ('circuitmaintenance', 'circuit', 'maintenance_start', 'maintenance_end', 'maintenance_status', 'impact')
        default_columns = ('circuitmaintenance', 'circuit', 'maintenance_start', 'maintenance_end', 'maintenance_status', 'impact')


class CircuitMaintenanceNotificationsTable(NetBoxTable):
    subject = tables.Column(linkify=True)
    circuitmaintenance = tables.Column(verbose_name='Maintenance', linkify=True)
    email_from = tables.Column(verbose_name='From')
    email_received = tables.Column(verbose_name='Received')

    class Meta(NetBoxTable.Meta):
        model = CircuitMaintenanceNotifications
        fields = ('pk', 'id', 'subject', 'circuitmaintenance', 'email_from', 'email_received', 'actions')
        default_columns = ('subject', 'circuitmaintenance', 'email_from', 'email_received')
