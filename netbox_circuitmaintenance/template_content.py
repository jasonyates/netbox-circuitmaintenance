from netbox.plugins import PluginTemplateExtension
from django.db.models import Q
from .models import CircuitMaintenanceImpact
from .constants import ACTIVE_STATUSES

TERMINAL_STATUSES = ('COMPLETED', 'CANCELLED')


class CircuitMaintenanceList(PluginTemplateExtension):
    models = ('circuits.circuit',)

    def left_page(self):
        circuit = self.context['object']
        base_qs = CircuitMaintenanceImpact.objects.filter(circuit=circuit)
        return self.render('netbox_circuitmaintenance/maintenance_tabs_include.html', extra_context={
            'active_maintenance': base_qs.filter(circuitmaintenance__status__in=ACTIVE_STATUSES),
            'historical_maintenance': base_qs.filter(circuitmaintenance__status__in=TERMINAL_STATUSES).order_by('-circuitmaintenance__end')[:20],
        })


class ProviderMaintenanceList(PluginTemplateExtension):
    models = ('circuits.provider',)

    def left_page(self):
        provider = self.context['object']
        base_qs = CircuitMaintenanceImpact.objects.filter(circuitmaintenance__provider=provider)
        return self.render('netbox_circuitmaintenance/maintenance_tabs_include.html', extra_context={
            'active_maintenance': base_qs.filter(circuitmaintenance__status__in=ACTIVE_STATUSES),
            'historical_maintenance': base_qs.filter(circuitmaintenance__status__in=TERMINAL_STATUSES).order_by('-circuitmaintenance__end')[:20],
        })


class SiteMaintenanceList(PluginTemplateExtension):
    models = ('dcim.site',)

    def left_page(self):
        site = self.context['object']
        site_q = Q(circuit__termination_a___site=site) | Q(circuit__termination_z___site=site)
        base_qs = CircuitMaintenanceImpact.objects.filter(site_q)
        return self.render('netbox_circuitmaintenance/maintenance_tabs_include.html', extra_context={
            'active_maintenance': base_qs.filter(circuitmaintenance__status__in=ACTIVE_STATUSES),
            'historical_maintenance': base_qs.filter(circuitmaintenance__status__in=TERMINAL_STATUSES).order_by('-circuitmaintenance__end')[:20],
        })


template_extensions = [CircuitMaintenanceList, ProviderMaintenanceList, SiteMaintenanceList]
