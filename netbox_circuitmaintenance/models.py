from django.db import models
from django.core.exceptions import ValidationError
from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet
from django.urls import reverse
from timezone_field import TimeZoneField

class CircuitMaintenanceTypeChoices(ChoiceSet):

    # Valid maintenance status choices. From BCOP standard - https://github.com/jda/maintnote-std/blob/master/standard.md

    key = 'DocTypeChoices.CircuitMaintenance'

    CHOICES = [
        ('TENTATIVE', 'Tentative', 'yellow'),
        ('CONFIRMED', 'Confirmed', 'green'),
        ('CANCELLED', 'Cancelled', 'blue'),
        ('IN-PROCESS', 'In-Progress', 'orange'),
        ('COMPLETED', 'Completed', 'indigo'),
        ('RE-SCHEDULED', 'Rescheduled', 'green'),
        ('UNKNOWN', 'Unknown', 'blue'),
    ]

class CircuitMaintenanceImpactTypeChoices(ChoiceSet):

    # Valid maintenance status choices. From BCOP standard - https://github.com/jda/maintnote-std/blob/master/standard.md

    key = 'DocTypeChoices.CircuitMaintenanceImpact'

    CHOICES = [
        ('NO-IMPACT', 'No-Impact', 'green'),
        ('REDUCED-REDUNDANCY', 'Reduced Redundancy', 'yellow'),
        ('DEGRADED', 'Degraded', 'orange'),
        ('OUTAGE', 'Outage', 'red'),
    ]

class CircuitMaintenance(NetBoxModel):
    name = models.CharField(
        max_length=100,
        verbose_name="Maintenance ID",
        help_text="The provider supplied maintenance ID / ticket number"
    )

    summary = models.CharField(
        max_length=200,
        help_text="Brief summary of the maintenance event"
    )

    status = models.CharField(
        max_length=30,
        choices=CircuitMaintenanceTypeChoices
    )

    provider = models.ForeignKey(
        to='circuits.provider',
        on_delete=models.CASCADE,
        related_name='maintenance',
        default=None
    )

    start = models.DateTimeField(
        help_text='Start date and time of the maintenance event e.g. 2022-12-25 14:30'
    )

    end = models.DateTimeField(
        help_text='End date and time of the maintenance event e.g. 2022-12-26 14:30'
    )

    time_zone = TimeZoneField(
        default='UTC',
        verbose_name="Provider Timezone",
        help_text="The provider's local timezone for this maintenance (informational only; times remain in UTC)"
    )

    internal_ticket = models.CharField(
        max_length=100,
        verbose_name="Internal Ticket #",
        help_text="An internal ticket or change reference for this maintenance",
        blank=True
    )

    acknowledged = models.BooleanField(
        default=False,
        verbose_name="Acknowledged?",
        help_text="Confirm if this maintenance event has been acknowledged"
    )

    comments = models.TextField(
        blank=True
    )

    clone_fields = (
        'status', 'provider', 'acknowledged', 'time_zone',
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Circuit Maintenance'
        verbose_name_plural = 'Circuit Maintenances'

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.start and self.end and self.end <= self.start:
            raise ValidationError({
                'end': 'End date/time must be after start date/time.'
            })

    def get_status_color(self):
        return CircuitMaintenanceTypeChoices.colors.get(self.status)

    def get_absolute_url(self):
        return reverse('plugins:netbox_circuitmaintenance:circuitmaintenance', args=[self.pk])

class CircuitMaintenanceImpact(NetBoxModel):

    circuitmaintenance = models.ForeignKey(
        to=CircuitMaintenance,
        on_delete=models.CASCADE,
        related_name='impact',
        verbose_name="Circuit Maintenance ID",
    )

    circuit = models.ForeignKey(
        to='circuits.circuit',
        on_delete=models.CASCADE,
        related_name='maintenance'
    )

    impact = models.CharField(
        max_length=30,
        choices=CircuitMaintenanceImpactTypeChoices,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('impact',)
        verbose_name = 'Circuit Maintenance Impact'
        verbose_name_plural = 'Circuit Maintenance Impact'
        constraints = [
            models.UniqueConstraint(
                fields=['circuitmaintenance', 'circuit'],
                name='unique_maintenance_circuit',
            )
        ]

    def get_impact_color(self):
        return CircuitMaintenanceImpactTypeChoices.colors.get(self.impact)

    def __str__(self):
        return self.circuitmaintenance.name + " - " + self.circuit.cid

    def get_absolute_url(self):
        return reverse('plugins:netbox_circuitmaintenance:circuitmaintenance', args=[self.circuitmaintenance.pk])

    def clean(self):
        super().clean()

        # Check we are not alerting a circuitmaintenaceimpact once the maintenance is complete
        if self.circuitmaintenance.status == "COMPLETED" or self.circuitmaintenance.status == "CANCELLED":
            raise ValidationError("You cannot alter a circuit maintenance impact once it has completed.")

class CircuitMaintenanceNotifications(NetBoxModel):

    circuitmaintenance = models.ForeignKey(
        to=CircuitMaintenance,
        on_delete=models.CASCADE,
        related_name='notification',
        verbose_name="Circuit Maintenance ID",
        null=True,
        blank=True,
    )

    email = models.BinaryField()

    email_body = models.TextField(
        verbose_name="Email Body"
    )

    subject = models.CharField(
        max_length=100
    )

    email_from = models.EmailField(
        verbose_name="Email From",
    )

    email_received = models.DateTimeField(
        verbose_name="Email Received"
    )

    class Meta:
        ordering = ('email_received',)
        verbose_name = 'Circuit Maintenance Notification'
        verbose_name_plural = 'Circuit Maintenance Notification'

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('plugins:netbox_circuitmaintenance:circuitnotification', args=[self.pk])
