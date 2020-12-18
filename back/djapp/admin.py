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
    list_display = ('email', 'get_contact_name', 'zip_code', 'get_email_confirmed', 'get_is_active', 'start_date', 'created')
    search_fields = ('email', 'first_name', 'last_name', 'zip_code')
    ordering = ('-created',)

    def get_contact_name(self, obj: models.Coach):
        return f'{obj.first_name.capitalize()} {obj.last_name.upper()}'
    get_contact_name.short_description = 'Contact'

    def get_email_confirmed(self, obj: models.Coach):
        return bool(obj.email_confirmed)
    get_email_confirmed.short_description = 'Email OK ?'
    get_email_confirmed.boolean = True

    def get_is_active(self, obj: models.Coach):
        return obj.is_active
    get_is_active.short_description = 'Actif ?'
    get_is_active.boolean = True


@admin.register(models.HostOrganization)
class HostOrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'get_contact_name', 'zip_code', 'get_email_confirmed', 'get_validated', 'get_is_active',
                    'start_date', 'created')
    search_fields = ('name', 'contact_email', 'contact_first_name', 'contact_last_name', 'zip_code')
    ordering = ('-created',)
    actions = ('run_matchings',)

    def get_email_confirmed(self, obj: models.HostOrganization):
        return bool(obj.email_confirmed)
    get_email_confirmed.short_description = 'Email OK ?'
    get_email_confirmed.boolean = True

    def get_validated(self, obj: models.HostOrganization):
        return bool(obj.validated)
    get_validated.short_description = 'Validé ?'
    get_validated.boolean = True

    def get_is_active(self, obj: models.HostOrganization):
        return obj.is_active
    get_is_active.short_description = 'Actif ?'
    get_is_active.boolean = True

    def get_contact_name(self, obj):
        return f'{obj.contact_first_name.capitalize()} {obj.contact_last_name.upper()}'
    get_contact_name.short_description = 'Contact'

    def run_matchings(self, request, queryset):
        n_error = 0
        n_success = 0
        n_matchings = 0
        matcher = Matcher()
        for host in queryset:
            try:
                matchings = matcher.run_process_for_host(host)
                n_matchings += len(matchings)
                n_success += 1
            except Exception as ex:
                n_error += 1
                logger.exception('Error processing matchings %r', host)
                self.message_user(request, (
                    'Erreur de traitement sur #%s - %s: %s'
                ) % (host.pk, host.name, ex), messages.ERROR)

        msg = f'{n_success} structure(s) traitée(s) avec succès, {n_matchings} matching(s)'
        level = messages.SUCCESS
        if n_error != 0:
            msg = f'{n_error} erreur(s), ' + msg
            level = messages.ERROR
        self.message_user(request, msg, level)
    run_matchings.short_description = 'Lancer le matching'


@admin.register(models.Matching)
class Matching(admin.ModelAdmin):
    list_display = ('id', 'coach', 'get_coach_experience', 'host', 'coach_contact_ok', 'host_contact_ok', 'host_meeting_ok', 'created')
    search_fields = ('coach__email', 'coach__first_name', 'coach__last_name', 'host__name', 'host__contact_first_name', 'host__contact_last_name')
    ordering = ('-created',)
    list_select_related = ('coach', 'host')

    def get_coach_experience(self, obj):
        return obj.coach.has_experience
    get_coach_experience.short_description = 'Experience ?'
    get_coach_experience.boolean = True
