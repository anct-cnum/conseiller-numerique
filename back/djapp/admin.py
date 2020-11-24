import logging

from django.contrib import admin, messages

from djapp import models
from djapp.biz.matching import Matcher


logger = logging.getLogger(__name__)


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)


@admin.register(models.Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'zip_code', 'start_date', 'created')
    search_fields = ('email', 'first_name', 'last_name', 'zip_code')
    ordering = ('-created',)


@admin.register(models.HostOrganization)
class HostOrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'contact_first_name', 'contact_last_name', 'start_date', 'created')
    search_fields = ('name', 'contact_email', 'contact_first_name', 'contact_last_name', 'zip_code')
    ordering = ('-created',)
    actions = ('run_matchings',)

    def run_matchings(self, request, queryset):
        n_error = 0
        n_success = 0
        matcher = Matcher()
        for host in queryset:
            try:
                matcher.run_process_for_host(host)
                n_success += 1
            except Exception as ex:
                n_error += 1
                logger.exception('Error processing matchings %r', host)
                self.message_user(request, (
                    'Erreur de traitement sur #%s - %s: %s'
                ) % (host.pk, host.name, ex), messages.ERROR)
        if n_error == 0:
            self.message_user(request, (
                '%s structure(s) traitée(s) avec succès'
            ) % (n_success,), messages.SUCCESS)
        else:
            self.message_user(request, (
                '%s erreur(s), %s structure(s) traitée(s) avec succès'
            ) % (n_error, n_success), messages.ERROR)
    run_matchings.short_description = 'Lancer le matching'


@admin.register(models.Matching)
class Matching(admin.ModelAdmin):
    list_display = ('id', 'coach', 'get_coach_experience', 'host', 'get_coach_accepted', 'get_host_accepted', 'created')
    search_fields = ('coach__email', 'coach__first_name', 'coach__last_name', 'host__name', 'host__contact_first_name', 'host__contact_last_name')
    ordering = ('-created',)
    list_select_related = ('coach', 'host')

    def get_coach_experience(self, obj):
        return obj.coach.has_experience and 'Oui' or '-'

    def get_coach_accepted(self, obj):
        if obj.coach_accepted:
            return 'Oui'
        if obj.coach_rejected:
            return '-'
        return ' '

    def get_host_accepted(self, obj):
        if obj.host_accepted:
            return 'Oui'
        if obj.host_rejected:
            return '-'
        return ' '
