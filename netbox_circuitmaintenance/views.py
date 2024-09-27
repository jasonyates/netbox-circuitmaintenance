
from netbox.views import generic
from django.db.models import Count
from . import forms, models, tables, filtersets
from django.views.generic import View
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
import datetime
import calendar
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.conf import settings

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
            return year-1
        elif month == 12:
            return year+1
        else:
            return year

    def next_year(self, month, year):
        if month == 1:
            return year-1
        elif month == 12:
            return year+1
        else:
            return year

    def formatday(self, day, weekday, events):
        """
        Return a day as a table cell.
        """
        events_from_day = events.filter(Q(start__day=day) | Q(end__day=day))
        events_html = "<ul>"
        for event in events_from_day:
            if events_html != '<ul>':
                events_html += '<br><br>'

            # Format time of the event
            if self.custom_strftime('SU', event.start) == self.custom_strftime('SU', event.end):
                event_time = f'{self.custom_strftime("%H:%M", event.start)} - {self.custom_strftime("%H:%M", event.end)}'
            else:
                event_time = f'{self.custom_strftime("SU %H:%M", event.start)} - {self.custom_strftime("SU %H:%M", event.end)}'
            
            # Add the event to the day
            events_html += f'<span class="badge text-bg-{event.get_status_color()}"><a href="{event.get_absolute_url()}">{event_time}<br>{event.name} <br>{event.provider} - {event.status}<br>{event.impact_count} Impacted</a></span>'
        events_html += "</ul>"
 
        if day == 0:
            return '<td>&nbsp;</td>'
        else:
            return '<td class="%s"><strong>%d</strong>%s</td>' % (self.cssclasses[weekday], day, events_html)
 
    def formatweek(self, theweek, events):
        """
        Return a complete week as a table row.
        """
        week = ''.join(self.formatday(d, wd, events) for (d, wd) in theweek)
        return '<tr>%s</tr>' % week
    
    def formatmonth(self, theyear, themonth):
        events = models.CircuitMaintenance.objects.filter(Q(start__month=themonth) | Q(end__month=themonth)).annotate(impact_count=Count('impact'))
        v = []
        a = v.append
        a('<table class="table">')
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
class CircuitMaintenanceScheduleView(View):
    template_name = 'netbox_circuitmaintenance/calendar.html'


    def get(self, request):

        curr_month = datetime.date.today()

        # Check if we have a month and year in the URL
        if request.GET and 'month' in request.GET:
            month = int(request.GET["month"])
            year = int(request.GET["year"])

        else:
            month = curr_month.month
            year = curr_month.year

        # Load calendar
        cal = Calendar()
        html_calendar = cal.formatmonth(year, month)
        html_calendar = html_calendar.replace('<td ', '<td  width="300" height="150"')

        return render(
            request,
            self.template_name,
            {
                "calendar":  mark_safe(html_calendar),
                "this_month": curr_month.month,
                "this_year": curr_month.year,
                "month": month,
                "year": year,
                "next_month": cal.next_month(month),
                "next_year": cal.next_year(month, year),
                "prev_month": cal.prev_month(month),
                "prev_year": cal.prev_year(month, year),
                "basepath": settings.BASE_PATH,
            }
        )