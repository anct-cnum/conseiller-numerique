from django.core.management.base import BaseCommand
from djapp import models
from djapp.biz.matching import Matcher


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('end_pk')

    def handle(self, *args, **options):
        end_pk = options['end_pk']
        matcher = Matcher()
        for host in models.HostOrganization.objects.filter(pk__lte=end_pk):
            self.stdout.write('Run for host %r...' % (host,))
            matchings = matcher.run_process_for_host(host)
            self.stdout.write('Run for host %r: %s matchings' % (host, len(matchings)))
        self.stdout.write('Ok.')
