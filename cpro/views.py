import random
from django.shortcuts import render, get_object_or_404
from web.views_collections import item_view, list_view
from web.settings import ENABLED_COLLECTIONS
from web.views import _index_extraContext as web_index_extraContext
from cpro import models, filters
from web.utils import ajaxContext

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
    del(collection['list']['filter_form'])
    return list_view(request, 'activity', collection)

def cardstat(request, card):
    context = ajaxContext(request)
    context['card'] = get_object_or_404(models.Card, pk=card)
    return render(request, 'include/cards-stats.html', context)

def cardcollection(request, card):
    collection = ENABLED_COLLECTIONS['card'].copy()
    collection['item'] = collection['item'].copy()
    request.GET = request.GET.copy()
    request.GET['collection'] = True
    collection['item']['template'] = '../include/cards-collection'
    return item_view(request, 'card', collection, pk=card, ajax=True)

def addcard(request, card):
    collection = 'collection' in request.GET
    queryset = models.Card
    if not collection:
        # Note: calling filterCards will add extra info need to display the card
        queryset = filters.filterCards(models.Card.objects.all(), {}, request)
    card = get_object_or_404(queryset, pk=card)
    account = get_object_or_404(models.Account, pk=request.POST.get('account', None), owner=request.user)
    models.OwnedCard.objects.create(card=card, account=account)
    if not collection:
        card.total_owned += 1
    if collection:
        return cardcollection(request, card.id)
    else:
        return item_view(request, 'card', ENABLED_COLLECTIONS['card'], pk=card.id, item=card, ajax=True)

def account_about(request, account):
    context = ajaxContext(request)
    context['account'] = get_object_or_404(models.Account.objects.select_related('starter'), pk=account)
    return render(request, 'ajax/account_about.html', context)
