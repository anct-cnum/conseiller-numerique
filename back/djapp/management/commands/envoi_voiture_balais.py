from django.core.management.base import BaseCommand
from djapp import models

from djapp.biz import email_factory

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--offset', type=int)
        parser.add_argument('--limit', type=int)

    def handle(self, *args, **options):
        offset = options['offset']
        limit = options['limit']
        for coach in models.Coach.objects.order_by('id').all()[offset:limit]:
            matchings = models.Matching.objects.all().filter(coach=coach).count()
            if matchings == 0:
                email_factory.send_voiture_balais(coach)
        self.stdout.write('Ok.')
