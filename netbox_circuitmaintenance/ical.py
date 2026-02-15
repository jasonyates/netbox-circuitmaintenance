import datetime

from django.http import HttpResponse
from django.views import View
from icalendar import Calendar, Event, vText
from utilities.views import ObjectPermissionRequiredMixin

from .models import CircuitMaintenance


class MaintenanceICalView(ObjectPermissionRequiredMixin, View):
    """Generate an ICS feed of maintenance events."""

    queryset = CircuitMaintenance.objects.all()

    def get_required_permission(self):
        return "netbox_circuitmaintenance.view_circuitmaintenance"

    def get(self, request):
        cal = Calendar()
        cal.add("prodid", "-//NetBox Circuit Maintenance//EN")
        cal.add("version", "2.0")
        cal.add("calscale", "GREGORIAN")
        cal.add("method", "PUBLISH")
        cal.add("x-wr-calname", "Circuit Maintenance")

        # Include active + recent completed (last 30 days)
        cutoff = datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(
            days=30
        )
        maintenances = (
            self.queryset.restrict(request.user, "view")
            .filter(end__gte=cutoff)
            .select_related("provider")
            .prefetch_related("impact")
        )

        for maint in maintenances:
            event = Event()
            event.add("uid", f"maintenance-{maint.pk}@netbox")
            event.add("dtstart", maint.start)
            event.add("dtend", maint.end)
            event.add("summary", f"[{maint.status}] {maint.provider} - {maint.name}")

            impact_count = maint.impact.count()
            description = maint.summary
            if impact_count:
                circuits = ", ".join(str(i.circuit) for i in maint.impact.all())
                description += f"\n\nImpacted circuits ({impact_count}): {circuits}"

            event.add("description", description)
            event.add(
                "status", "CONFIRMED" if maint.status == "CONFIRMED" else "TENTATIVE"
            )
            event["organizer"] = vText(str(maint.provider))
            cal.add_component(event)

        response = HttpResponse(
            cal.to_ical(),
            content_type="text/calendar; charset=utf-8",
        )
        response["Content-Disposition"] = (
            'attachment; filename="circuit-maintenance.ics"'
        )
        return response
