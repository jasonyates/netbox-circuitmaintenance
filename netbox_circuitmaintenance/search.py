from netbox.search import SearchIndex, register_search

from .models import CircuitMaintenance, CircuitMaintenanceNotifications


@register_search
class CircuitMaintenanceIndex(SearchIndex):
    model = CircuitMaintenance
    fields = (
        ('name', 100),
        ('summary', 500),
        ('internal_ticket', 1000),
        ('comments', 5000),
    )


@register_search
class CircuitMaintenanceNotificationsIndex(SearchIndex):
    model = CircuitMaintenanceNotifications
    fields = (
        ('subject', 100),
        ('email_from', 1000),
    )
