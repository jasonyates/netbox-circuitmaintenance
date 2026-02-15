from django.db.models import Q
from netbox.plugins import PluginTemplateExtension

from .constants import ACTIVE_STATUSES
from .models import CircuitMaintenanceImpact


class CircuitMaintenanceList(PluginTemplateExtension):
    models = ("circuits.circuit",)

    def left_page(self):
        circuit = self.context["object"]
        active_qs = CircuitMaintenanceImpact.objects.filter(
            circuit=circuit, circuitmaintenance__status__in=ACTIVE_STATUSES
        ).select_related("circuitmaintenance", "circuit")
        return self.render(
            "netbox_circuitmaintenance/maintenance_tabs_include.html",
            extra_context={
                "active_maintenance": active_qs,
            },
        )


class ProviderMaintenanceList(PluginTemplateExtension):
    models = ("circuits.provider",)

    def left_page(self):
        provider = self.context["object"]
        active_qs = CircuitMaintenanceImpact.objects.filter(
            circuitmaintenance__provider=provider,
            circuitmaintenance__status__in=ACTIVE_STATUSES,
        ).select_related("circuitmaintenance", "circuit")
        return self.render(
            "netbox_circuitmaintenance/maintenance_tabs_include.html",
            extra_context={
                "active_maintenance": active_qs,
            },
        )


class SiteMaintenanceList(PluginTemplateExtension):
    models = ("dcim.site",)

    def left_page(self):
        site = self.context["object"]
        site_q = Q(circuit__termination_a___site=site) | Q(
            circuit__termination_z___site=site
        )
        active_qs = CircuitMaintenanceImpact.objects.filter(
            site_q, circuitmaintenance__status__in=ACTIVE_STATUSES
        ).select_related("circuitmaintenance", "circuit")
        return self.render(
            "netbox_circuitmaintenance/maintenance_tabs_include.html",
            extra_context={
                "active_maintenance": active_qs,
            },
        )


template_extensions = [
    CircuitMaintenanceList,
    ProviderMaintenanceList,
    SiteMaintenanceList,
]
