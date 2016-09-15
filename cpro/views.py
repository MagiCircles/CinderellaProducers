import random
from django.shortcuts import render, get_object_or_404
from web.views_collections import item_view, list_view
from web.settings import ENABLED_COLLECTIONS
from web.views import _index_extraContext as web_index_extraContext
from cpro import models, filters

def _index_extraContext(context):
    web_index_extraContext(context)
    context['card'] = models.Card.objects.order_by('?').filter(art__isnull=False).exclude(art='')[0]
    context['awakened'] = random.choice([True, False]) if context['card'].id_awakened else False

def index(request):
    collection = ENABLED_COLLECTIONS['activity'].copy()
    collection['list'] = collection['list'].copy()
    collection['list']['before_template'] = 'include/index'
    collection['list']['extra_context'] = _index_extraContext
    collection['list']['full_width'] = True
    return list_view(request, 'activity', collection)

def cardstat(request, card):
    context = {
        'card': get_object_or_404(models.Card, pk=card),
    }
    return render(request, 'include/cards-stats.html', context)

def addcard(request, card):
    card = get_object_or_404(filters.filterCards(models.Card.objects.all(), {}, request), pk=card)
    # Note: calling filterCards will add extra info need to display the card
    account = get_object_or_404(models.Account, pk=request.POST.get('account', None), owner=request.user)
    models.OwnedCard.objects.create(card=card, account=account)
    card.total_owned += 1
    return item_view(request, 'card', ENABLED_COLLECTIONS['card'], pk=card.id, item=card, ajax=True)

def account_about(request, account):
    context = {
        'account': get_object_or_404(models.Account.objects.select_related('starter'), pk=account),
    }
    return render(request, 'ajax/account_about.html', context)
