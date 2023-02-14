from django.core.management.base import BaseCommand, CommandError
from extras.models import JobResult
from django.contrib.contenttypes.models import ContentType

from netbox_circuitmaintenance.jobs import test_my_job

class Command(BaseCommand):
    help = 'Queues a job for circuit maintenance parsing'

    def handle(self, *args, **options):

        content_type = ContentType.objects.get(app_label='netbox_circuitmaintenance', model='circuitmaintenancepoller')

        JobResult.enqueue_job(
            test_my_job,
            "Circuit Maintenance IMAP Poller",
            content_type,
            None
        )

        self.stdout.write(self.style.SUCCESS('Yes it worked'))