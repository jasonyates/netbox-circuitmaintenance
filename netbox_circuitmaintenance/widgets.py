from django import forms
from extras.dashboard.utils import register_widget
from extras.dashboard.widgets import DashboardWidget, WidgetConfigForm
from django.template.loader import render_to_string
from .models import CircuitMaintenance
from .constants import ACTIVE_STATUSES
from django.db.models import Count
from .views import Calendar
import datetime
from django.utils.safestring import mark_safe

@register_widget
class UpcomingMaintenanceWidget(DashboardWidget):
    default_title = 'Upcoming Circuit Maintenance Events'
    description = 'Active / Upcoming Maintenance'
    template_name = 'netbox_circuitmaintenance/widget.html'
    width = 8
    height = 3

    def render(self, request):
        
        return render_to_string(self.template_name, {
            'circuitmaintenance': CircuitMaintenance.objects.filter(status__in=ACTIVE_STATUSES).annotate(
                impact_count=Count('impact')
            ),
        })
    
@register_widget
class MaintenanceCalendarWidget(DashboardWidget):
    default_title = 'Upcoming Circuit Maintenance Calendar'
    description = 'Show a simplified calendar view showing upcoming maintenance events this month'
    template_name = 'netbox_circuitmaintenance/calendar_widget.html'
    width = 8
    height = 6

    def render(self, request):

        curr_month = datetime.date.today()

        # Load calendar
        cal = Calendar(curr_month.year, curr_month.month)
        html_calendar = cal.formatmonth(curr_month.year, curr_month.month)
        return render_to_string(self.template_name, {"calendar":  mark_safe(html_calendar)})
