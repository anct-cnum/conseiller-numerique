import logging
logger = logging.getLogger(__name__)

from djapp import models

#Verify Duplicate coach (conseiller)
def count_apply_coaches_filters(qs, filters):
    qs = qs.filter(email=filters['email'])
    qs = qs.filter(zip_code=filters['zip_code'])
    qs = qs.count()
    return qs

def count_queryset_coaches(filters):
    qs = models.Coach.objects.all()
    qs = count_apply_coaches_filters(qs, filters)
    return qs

def verify_duplicate_coach(filters):
    nbDoublon = count_queryset_coaches(filters)
    if nbDoublon==0 :
        return False
    logger.warning('Inscription refusée : il existe déjà au moins un doublon pour cette inscription conseiller %s', filters)
    return True

#Verify Duplicate Host organization (structure)
def count_apply_host_organizations_filters(qs, filters):
    qs = qs.filter(siret=filters['siret'])
    qs = qs.filter(contact_email=filters['contact_email'])
    qs = qs.filter(zip_code=filters['zip_code'])
    qs = qs.count()
    return qs

def count_queryset_host_organizations(filters):
    qs = models.HostOrganization.objects.all()
    qs = count_apply_host_organizations_filters(qs, filters)
    return qs

def verify_duplicate_host_organization(filters):
    nbDoublon = count_queryset_host_organizations(filters)
    if nbDoublon==0 :
        return False
    logger.warning('Inscription refusée : il existe déjà au moins un doublon pour cette inscription structure %s', filters)
    return True
