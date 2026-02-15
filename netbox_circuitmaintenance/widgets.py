from django.db.models import Count
from django.template.loader import render_to_string
from django.utils import timezone as django_timezone
from django.utils.safestring import mark_safe
from extras.dashboard.utils import register_widget
from extras.dashboard.widgets import DashboardWidget

from .constants import ACTIVE_STATUSES
from .models import CircuitMaintenance
from .views import MaintenanceCalendar


@register_widget
class UpcomingMaintenanceWidget(DashboardWidget):
    default_title = "Upcoming Circuit Maintenance Events"
    description = "Active / Upcoming Maintenance"
    template_name = "netbox_circuitmaintenance/widget.html"
    width = 8
    height = 3

    def render(self, request):

        return render_to_string(
            self.template_name,
            {
                "circuitmaintenance": CircuitMaintenance.objects.restrict(
                    request.user, "view"
                )
                .filter(status__in=ACTIVE_STATUSES)
                .annotate(impact_count=Count("impact")),
            },
        )


@register_widget
class MaintenanceCalendarWidget(DashboardWidget):
    default_title = "Upcoming Circuit Maintenance Calendar"
    description = (
        "Show a simplified calendar view showing upcoming maintenance events this month"
    )
    template_name = "netbox_circuitmaintenance/calendar_widget.html"
    width = 8
    height = 6

    def render(self, request):

        curr_month = django_timezone.now().date()

        # Load calendar
        cal = MaintenanceCalendar(curr_month.year, curr_month.month)
        html_calendar = cal.formatmonth(curr_month.year, curr_month.month)
        return render_to_string(
            self.template_name, {"calendar": mark_safe(html_calendar)}
        )
