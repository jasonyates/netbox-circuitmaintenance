
from netbox.views import generic
from django.db.models import Count, Q
from . import forms, models, tables, filtersets
from .models import CircuitMaintenanceImpact
from django.views.generic import View
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
import datetime
import calendar
from django.utils.safestring import mark_safe
from django.urls import reverse
from utilities.views import register_model_view, ViewTab
from circuits.models import Circuit, Provider
from dcim.models import Site

TERMINAL_STATUSES = ('COMPLETED', 'CANCELLED')

# Circuit Maintenance Views
class CircuitMaintenanceView(generic.ObjectView):
    queryset = models.CircuitMaintenance.objects.prefetch_related('impact').all()

    def get_extra_context(self, request, instance):
        # Load the maintenance event impact
        impact = models.CircuitMaintenanceImpact.objects.filter(circuitmaintenance=instance)

        # Load the maintenance event notifications
        notification = models.CircuitMaintenanceNotifications.objects.filter(circuitmaintenance=instance)

        return {
            "impacts": impact,
            "notifications": notification
        }

class CircuitMaintenanceListView(generic.ObjectListView):
    queryset = models.CircuitMaintenance.objects.annotate(
        impact_count=Count('impact')
    )
    table = tables.CircuitMaintenanceTable
    filterset = filtersets.CircuitMaintenanceFilterSet
    filterset_form = forms.CircuitMaintenanceFilterForm

class CircuitMaintenanceEditView(generic.ObjectEditView):
    queryset = models.CircuitMaintenance.objects.all()
    form = forms.CircuitMaintenanceForm

class CircuitMaintenanceDeleteView(generic.ObjectDeleteView):
    queryset = models.CircuitMaintenance.objects.all()

class CircuitMaintenanceBulkEditView(generic.BulkEditView):
    queryset = models.CircuitMaintenance.objects.all()
    filterset = filtersets.CircuitMaintenanceFilterSet
    table = tables.CircuitMaintenanceTable
    form = forms.CircuitMaintenanceBulkEditForm

class CircuitMaintenanceBulkDeleteView(generic.BulkDeleteView):
    queryset = models.CircuitMaintenance.objects.all()
    filterset = filtersets.CircuitMaintenanceFilterSet
    table = tables.CircuitMaintenanceTable


# Circuit Maintenance Impact views
class CircuitMaintenanceImpactEditView(generic.ObjectEditView):
    queryset = models.CircuitMaintenanceImpact.objects.all()
    form = forms.CircuitMaintenanceImpactForm

class CircuitMaintenanceImpactDeleteView(generic.ObjectDeleteView):
    queryset = models.CircuitMaintenanceImpact.objects.all()


# Circuit Maintenance Notification views
class CircuitMaintenanceNotificationsEditView(generic.ObjectEditView):
    queryset = models.CircuitMaintenanceNotifications.objects.all()
    form = forms.CircuitMaintenanceNotificationsForm

class CircuitMaintenanceNotificationsDeleteView(generic.ObjectDeleteView):
    queryset = models.CircuitMaintenanceNotifications.objects.all()

class CircuitMaintenanceNotificationView(generic.ObjectView):
    queryset = models.CircuitMaintenanceNotifications.objects.all()


class Calendar(calendar.HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def suffix(self, day):
        if 4 <= day <= 20 or 24 <= day <= 30:
            return "th"
        else:
            return ["st", "nd", "rd"][day % 10 - 1]
    
    def custom_strftime(self, format, t):
        return t.strftime(format).replace('SU', str(t.day) + self.suffix(t.day))

    def formatmonthname(self, theyear, themonth) :
        return f"<h1>{calendar.month_name[themonth]} {theyear}</h1>"

    def prev_month(self,month):
        if month == 1:
            return 12
        else:
            return month-1
        
    def next_month(self, month):
        if month == 12:
            return 1
        else:
            return month+1
        
    def prev_year(self, month, year):
        if month == 1:
            return year - 1
        return year

    def next_year(self, month, year):
        if month == 12:
            return year + 1
        return year

    def formatday(self, day, weekday, events, week_dates):
        """
        Return a day as a table cell with single-day events as badges
        and multi-day events as continuous bar segments.
        """
        if day == 0:
            return '<td>&nbsp;</td>'

        this_date = datetime.date(self.year, self.month, day)

        # Multi-day event bar segments
        multi_day_html = ""
        multi_day_events = [
            e for e in events
            if e.start.date() != e.end.date()
            and e.start.date() <= this_date
            and e.end.date() >= this_date
        ]
        for event in multi_day_events:
            is_actual_start = event.start.date() == this_date
            is_week_start = this_date == week_dates[0]
            is_first_cell = is_actual_start or (is_week_start and event.start.date() < week_dates[0])

            # On continuation days, add a spacer so single-day events sit below the bar
            if not is_first_cell:
                multi_day_html += '<div class="cal-span-spacer"></div>'
                continue

            # Calculate how many days the bar spans within this week
            event_end_in_week = min(event.end.date(), week_dates[-1])
            span_days = (event_end_in_week - this_date).days + 1

            # Rounded corners
            starts_here = is_actual_start
            ends_here = event.end.date() <= week_dates[-1]
            if starts_here and ends_here:
                radius_cls = "rounded"
            elif starts_here:
                radius_cls = "rounded-start"
            elif ends_here:
                radius_cls = "rounded-end"
            else:
                radius_cls = ""

            event_time = (
                f'{self.custom_strftime("SU %H:%M", event.start)} - '
                f'{self.custom_strftime("SU %H:%M", event.end)}'
            )
            tooltip = (
                f'{event_time} | {event.name} | '
                f'{event.provider} - {event.status} | '
                f'{event.impact_count} Impacted'
            )

            # Show text only on the actual event start date
            label = tooltip if is_actual_start else '&nbsp;'

            # Width spans across N columns (each column is 14.285% of table)
            width_style = f'width: calc({span_days} * 100% + {span_days - 1} * 8px);' if span_days > 1 else ''

            multi_day_html += (
                f'<a href="{event.get_absolute_url()}" '
                f'class="cal-span text-bg-{event.get_status_color()} {radius_cls}" '
                f'style="{width_style}" '
                f'title="{tooltip}">'
                f'{label}</a>'
            )

        # Single-day events
        single_html = ""
        single_day_events = [
            e for e in events
            if e.start.date() == e.end.date() and e.start.date() == this_date
        ]
        for event in single_day_events:
            event_time = f'{event.start.strftime("%H:%M")} - {event.end.strftime("%H:%M")}'
            single_html += (
                f'<span class="badge text-bg-{event.get_status_color()} d-block mb-1">'
                f'<a href="{event.get_absolute_url()}">'
                f'{event_time}<br>{event.name}<br>'
                f'{event.provider} - {event.status}<br>'
                f'{event.impact_count} Impacted</a></span>'
            )

        today = datetime.date.today()
        css_class = self.cssclasses[weekday]
        if this_date == today:
            css_class += " today-highlight"

        add_url = reverse('plugins:netbox_circuitmaintenance:circuitmaintenance_add')
        date_str = this_date.strftime('%Y-%m-%d 09:00')
        day_link = (
            f'<a href="{add_url}?start={date_str}" class="cal-day-add" '
            f'title="Add maintenance on {this_date.strftime("%d %b %Y")}">'
            f'<strong>{day}</strong> '
            f'<i class="mdi mdi-plus-circle-outline cal-add-icon"></i></a>'
        )

        cell_url = f'{add_url}?start={date_str}'

        return (
            f'<td class="{css_class}" data-href="{cell_url}">'
            f'{day_link}'
            f'{multi_day_html}'
            f'{single_html}'
            f'</td>'
        )

    def formatweek(self, theweek, events):
        """
        Return a complete week as a table row.
        """
        # Build list of actual dates for this week (for start/end detection)
        week_dates = []
        for day, wd in theweek:
            if day == 0:
                week_dates.append(None)
            else:
                week_dates.append(datetime.date(self.year, self.month, day))
        valid_dates = [d for d in week_dates if d is not None]

        week = ''.join(
            self.formatday(d, wd, events, valid_dates)
            for (d, wd) in theweek
        )
        return f'<tr>{week}</tr>'
    
    def formatmonth(self, theyear, themonth):
        import calendar as cal_module
        _, last_day = cal_module.monthrange(theyear, themonth)
        month_start = datetime.date(theyear, themonth, 1)
        month_end = datetime.date(theyear, themonth, last_day)
        events = models.CircuitMaintenance.objects.filter(
            start__date__lte=month_end,
            end__date__gte=month_start,
        ).annotate(impact_count=Count('impact'))
        v = []
        a = v.append
        a('<table class="table table-bordered">')
        a('\n')
        a(self.formatmonthname(theyear, themonth))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, events))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)


# CircuitMaintenanceSchedule
class CircuitMaintenanceScheduleView(PermissionRequiredMixin, View):
    permission_required = 'netbox_circuitmaintenance.view_circuitmaintenance'
    template_name = 'netbox_circuitmaintenance/calendar.html'
    partial_template_name = 'netbox_circuitmaintenance/calendar_partial.html'

    def get(self, request):
        curr_month = datetime.date.today()

        if request.GET.get('month'):
            month = int(request.GET["month"])
            year = int(request.GET["year"])
        else:
            month = curr_month.month
            year = curr_month.year

        cal = Calendar(year, month)
        html_calendar = cal.formatmonth(year, month)

        context = {
            "calendar": mark_safe(html_calendar),
            "this_month": curr_month.month,
            "this_year": curr_month.year,
            "month": month,
            "year": year,
            "next_month": cal.next_month(month),
            "next_year": cal.next_year(month, year),
            "prev_month": cal.prev_month(month),
            "prev_year": cal.prev_year(month, year),
        }

        template = self.partial_template_name if request.headers.get('HX-Request') else self.template_name
        return render(request, template, context)


# Historical Maintenance tab views for Circuit, Provider, and Site detail pages

@register_model_view(Circuit, 'historical-maintenance')
class CircuitHistoricalMaintenanceTabView(generic.ObjectChildrenView):
    queryset = Circuit.objects.all()
    child_model = CircuitMaintenanceImpact
    table = tables.CircuitMaintenanceImpactTable
    filterset = filtersets.CircuitMaintenanceImpactFilterSet
    template_name = 'netbox_circuitmaintenance/historical_maintenance_tab.html'
    tab = ViewTab(
        label='Historical Maintenance',
        hide_if_empty=True,
        badge=lambda obj: CircuitMaintenanceImpact.objects.filter(
            circuit=obj, circuitmaintenance__status__in=TERMINAL_STATUSES
        ).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.restrict(request.user, 'view').filter(
            circuit=parent, circuitmaintenance__status__in=TERMINAL_STATUSES
        ).order_by('-circuitmaintenance__end')


@register_model_view(Provider, 'historical-maintenance')
class ProviderHistoricalMaintenanceTabView(generic.ObjectChildrenView):
    queryset = Provider.objects.all()
    child_model = CircuitMaintenanceImpact
    table = tables.CircuitMaintenanceImpactWithCircuitTable
    filterset = filtersets.CircuitMaintenanceImpactFilterSet
    template_name = 'netbox_circuitmaintenance/historical_maintenance_tab.html'
    tab = ViewTab(
        label='Historical Maintenance',
        hide_if_empty=True,
        badge=lambda obj: CircuitMaintenanceImpact.objects.filter(
            circuitmaintenance__provider=obj, circuitmaintenance__status__in=TERMINAL_STATUSES
        ).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.restrict(request.user, 'view').filter(
            circuitmaintenance__provider=parent, circuitmaintenance__status__in=TERMINAL_STATUSES
        ).order_by('-circuitmaintenance__end')


@register_model_view(Site, 'historical-maintenance')
class SiteHistoricalMaintenanceTabView(generic.ObjectChildrenView):
    queryset = Site.objects.all()
    child_model = CircuitMaintenanceImpact
    table = tables.CircuitMaintenanceImpactWithCircuitTable
    filterset = filtersets.CircuitMaintenanceImpactFilterSet
    template_name = 'netbox_circuitmaintenance/historical_maintenance_tab.html'
    tab = ViewTab(
        label='Historical Maintenance',
        hide_if_empty=True,
        badge=lambda obj: CircuitMaintenanceImpact.objects.filter(
            Q(circuit__termination_a___site=obj) | Q(circuit__termination_z___site=obj),
            circuitmaintenance__status__in=TERMINAL_STATUSES,
        ).count(),
    )

    def get_children(self, request, parent):
        return self.child_model.objects.restrict(request.user, 'view').filter(
            Q(circuit__termination_a___site=parent) | Q(circuit__termination_z___site=parent),
            circuitmaintenance__status__in=TERMINAL_STATUSES,
        ).order_by('-circuitmaintenance__end')