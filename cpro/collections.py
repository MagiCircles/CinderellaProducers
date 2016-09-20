from django.utils.translation import ugettext_lazy as _
from django.conf import settings as django_settings
from django.db.models import Prefetch
from cpro import forms, raw, models
from cpro.utils import shrinkImageFromData

############################################################
# Activities

def activitiesBeforeSave(request, instance, type=None):
    if instance.image:
        if instance.image and '/' not in instance.image.name:
            filename = instance.image.name
            instance.image = shrinkImageFromData(instance.image.read(), filename, resize=True)
            instance.image.name = instance._meta.model._meta.get_field('image').upload_to(instance, filename)
    return instance

############################################################
# Account

def getAccountForm(request, context, collection):
    formClass = forms.AccountFormSimple
    if 'advanced' in request.GET:
        formClass = forms.AccountFormAdvanced
        context['advanced'] = True
    return formClass

def leaderboardExtraContext(context):
    context['types'] = models.TYPE_CHOICES
    context['favorite_characters'] = getattr(django_settings, 'FAVORITE_CHARACTERS', [])
    context['starters'] = getattr(django_settings, 'STARTERS', [])

def addAccountAfterSave(request, account):
    if account.starter_id:
        oc = models.OwnedCard.objects.create(card_id=account.starter_id, account=account)
        account.center_id = oc.id
        account.update_cache_center()
        account.save()
    return account

def modAccountExtraContext(context):
    context['starters'] = getattr(django_settings, 'STARTERS', [])

def redirectAfterAddAccount(request, item, ajax):
    return '/cards/?get_started'

############################################################
# Profile

def profileGetAccountTabs(context):
    from web.views import profileExtraContext
    profileExtraContext(context)
    request = context['request']
    for account in context['item'].all_accounts:
        show = request.GET.get('account{}'.format(account.id), 'Cards')
        account.show = show if show in raw.ACCOUNT_TABS_LIST else 'Cards'
    context['account_tabs'] = raw.ACCOUNT_TABS

############################################################
# Card

def cardExtraContext(context):
    request = context['request']
    if request.user.is_authenticated():
        context['collection'] = 'collection' in request.GET
        if context['collection']:
            request.user.all_accounts = request.user.accounts.all().prefetch_related(
                Prefetch('ownedcards', queryset=models.OwnedCard.objects.filter(card_id=context['item'].id).order_by('-card__i_rarity', '-awakened', 'card__idol__i_type'), to_attr='all_owned'),
            )
            # Set values to avoid using select_related since we already have them
            for account in request.user.all_accounts:
                account.owner = request.user
                for oc in account.all_owned:
                    oc.card = context['item']
                    oc.is_mine = True

def cardsExtraContext(context):
    request = context['request']
    context['get_started'] = 'get_started' in request.GET
    if context['is_last_page']:
        context['share_sentence'] = _('Check out my collection of cards!')

############################################################
# Owned Card

def ownedCardRedirectAfter(request, item, ajax=False):
    if ajax:
        if 'collection' in request.GET:
            return '/ajax/cardcollection/{}/'.format(item.card_id)
        return '/ajax/card/{}/'.format(item.card_id)
    if 'back_to_profile' in request.GET:
        return item.account.owner.item_url
    return item.card.item_url

def foreachOwnedCard(index, item, context):
    item.is_mine = context['request'].user.id == item.cached_account.owner.id

############################################################
# Idols

def idolsExtraContext(context):
    request = context['request']
    if 'ordering' in request.GET:
        context['ordering'] = request.GET['ordering']
