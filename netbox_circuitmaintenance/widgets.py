from django import forms
from extras.dashboard.utils import register_widget
from extras.dashboard.widgets import DashboardWidget, WidgetConfigForm
from django.template.loader import render_to_string
from .models import CircuitMaintenance 
from django.db.models import Count

@register_widget
class ReminderWidget(DashboardWidget):
    default_title = 'Upcoming Circuit Maintenance Events'
    description = 'Show a list of upcoming circuit maintenance events'
    template_name = 'netbox_circuitmaintenance/widget.html'
    width = 8
    height = 3

    def render(self, request):
        
        return render_to_string(self.template_name, {
            'circuitmaintenance': CircuitMaintenance.objects.filter(status__in=['TENTATIVE', 'CONFIRMED', 'IN-PROCESS', 'RE-SCHEDULED', 'UNKNOWN']).annotate(
                impact_count=Count('impact')
            ),
        })
