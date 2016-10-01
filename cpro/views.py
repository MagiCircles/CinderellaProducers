import random, hashlib
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings as django_settings
from django.core.exceptions import PermissionDenied
from web.views_collections import item_view, list_view
from web.settings import ENABLED_COLLECTIONS
from web.views import _index_extraContext as web_index_extraContext
from web.forms import CreateUserForm
from cpro import models, filters
from web import models as web_models
from django.forms.util import ErrorList
from web.utils import ajaxContext, globalContext
from django.contrib.auth import authenticate, login as login_action

def _index_extraContext(context):
    web_index_extraContext(context)
    context['card'] = models.Card.objects.order_by('?').filter(art__isnull=False).exclude(art='').exclude(art_on_homepage=False, art_awakened_on_homepage=False)[0]
    if not context['card'].art_on_homepage:
        context['awakened'] = True
    elif not context['card'].art_awakened_on_homepage:
        context['awakened'] = False
    else:
        context['awakened'] = random.choice([True, False]) if context['card'].id_awakened else False

def index(request):
    collection = ENABLED_COLLECTIONS['activity'].copy()
    collection['list'] = collection['list'].copy()
    collection['list']['before_template'] = 'include/index'
    collection['list']['extra_context'] = _index_extraContext
    collection['list']['full_width'] = True
    collection['list']['js_files'] = collection['list'].get('js_files', []) + ['bower/countdown/dest/jquery.countdown.min']
    if 'filter_form' in collection['list']:
        del(collection['list']['filter_form'])
    return list_view(request, 'activity', collection)

def signup(request):
    if request.user.is_authenticated():
        redirectToProfile(request)
    if request.method == "POST":
        form = CreateUserForm(request.POST, request=request)
        if form.is_valid():
            if hashlib.md5(form.cleaned_data['email']).hexdigest() not in django_settings.EMAILS_ALLOWED:
                errors = form._errors.setdefault("email", ErrorList())
                errors.append(u"Cinderella Producers is currently in beta and is only open to pre-registered emails. If you want to join when it launches, use this link: http://eepurl.com/chcC2r")
            else:
                new_user = models.User.objects.create_user(**form.cleaned_data)
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                preferences = web_models.UserPreferences.objects.create(user=user, language=request.LANGUAGE_CODE)
                login_action(request, user)
                url = '/accounts/add/{}{}'.format(
                    ('?next={}'.format(urlquote(request.GET['next'])) if 'next' in request.GET else ''),
                    ('&next_title={}'.format(request.GET['next_title']) if 'next' in request.GET and 'next_title' in request.GET else ''))
                return redirect(url)
    else:
        form = CreateUserForm(request=request)
    context = globalContext(request)
    context['form'] = form
    context['next'] = request.GET.get('next', None)
    context['next_title'] = request.GET.get('next_title', None)
    return render(request, 'pages/signup.html', context)

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
    if request.method != "POST":
        raise PermissionDenied()
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

def favoritecard(request, card):
    print request.method
    if request.method != "POST":
        raise PermissionDenied()
    # Note: calling filterCards will add extra info need to display the card
    card = get_object_or_404(filters.filterCards(models.Card.objects.all(), {}, request), pk=card)
    print 'card favorited'
    print card.favorited
    if card.favorited:
        models.FavoriteCard.objects.filter(card=card, owner=request.user).delete()
        card.favorited = 0
    else:
        models.FavoriteCard.objects.create(card=card, owner=request.user)
        card.favorited = 1
    return item_view(request, 'card', ENABLED_COLLECTIONS['card'], pk=card.id, item=card, ajax=True)

def account_about(request, account):
    context = ajaxContext(request)
    context['account'] = get_object_or_404(models.Account.objects.select_related('starter'), pk=account)
    return render(request, 'ajax/account_about.html', context)
