from django.db.models import Q
from django.core.exceptions import PermissionDenied

############################################################
# Cards

def filterCards(queryset, parameters, request):
    if request.user.is_authenticated():
        request.user.all_accounts = request.user.accounts.all()
        accounts_pks = ','.join([str(account.pk) for account in request.user.all_accounts])
        if accounts_pks:
            queryset = queryset.extra(select={
                'total_owned': 'SELECT COUNT(*) FROM cpro_ownedcard WHERE card_id = cpro_card.id AND account_id IN ({})'.format(accounts_pks),
            })
    if 'search' in parameters and parameters['search']:
        terms = parameters['search'].split(' ')
        for term in terms:
            queryset = queryset.filter(Q(name__icontains=term)
                                       | Q(types_string__icontains=term)
                                   )
    if 'i_rarity' in parameters and parameters['i_rarity']:
        queryset = queryset.filter(i_rarity=parameters['i_rarity'])
    if 'type' in parameters and parameters['type']:
        queryset = queryset.filter(idol__i_type=parameters['type'])
    if 'is_event' in parameters and parameters['is_event']:
        if parameters['is_event'] == '2':
            queryset = queryset.filter(event__isnull=False)
        elif parameters['is_event'] == '3':
            queryset = queryset.filter(event__isnull=True)
    if 'is_limited' in parameters and parameters['is_limited']:
        if parameters['is_limited'] == '2':
            queryset = queryset.filter(is_limited=True)
        elif parameters['is_limited'] == '3':
            queryset = queryset.filter(is_limited=False)
    if 'is_awakened' in parameters and parameters['is_awakened']:
        if parameters['is_awakened'] == '2':
            queryset = queryset.filter(id_awakened__isnull=False)
        elif parameters['is_awakened'] == '3':
            queryset = queryset.filter(id_awakened__isnull=True)
    if 'has_art' in parameters and parameters['has_art']:
        if parameters['has_art'] == '2':
            queryset = queryset.filter(art__isnull=False).exclude(art='')
        elif parameters['has_art'] == '3':
            queryset = queryset.filter(Q(art__isnull=True) | Q(art=''))
    if 'i_skill' in parameters and parameters['i_skill']:
        queryset = queryset.filter(i_skill=parameters['i_skill'])
    return queryset

############################################################
# Owned Cards

def filterOwnedCards(queryset, parameters, request):
    if 'account' in parameters:
        queryset = queryset.filter(account_id=parameters['account'])
    elif 'ids' in parameters and parameters['ids']:
        queryset = queryset.filter(id__in=parameters['ids'].split(','))
    else:
        raise PermissionDenied()
    if 'search' in parameters and parameters['search']:
        terms = parameters['search'].split(' ')
        for term in terms:
            queryset = queryset.filter(Q(card__title__icontains=term)
                                       | Q(card__idol__name__icontains=term)
                                   )
    if 'i_rarity' in parameters and parameters['i_rarity']:
        queryset = queryset.filter(card__i_rarity=parameters['i_rarity'])
    if 'is_event' in parameters and parameters['is_event']:
        if parameters['is_event'] == '2':
            queryset = queryset.filter(card__event__isnull=False)
        elif parameters['is_event'] == '3':
            queryset = queryset.filter(card__event__isnull=True)
    if 'type' in parameters and parameters['type']:
        queryset = queryset.filter(card__idol__i_type=parameters['type'])
    if 'i_skill' in parameters and parameters['i_skill']:
        queryset = queryset.filter(card__i_skill=parameters['i_skill'])
    return queryset
