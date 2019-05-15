from django.utils.translation import ugettext_lazy as _
from django.conf import settings as django_settings
from django.db.models import Prefetch
from cpro import forms, raw, models
from cpro.utils import shrinkImageFromData

# todo

# ############################################################
# # Activities

# def activitiesBeforeSave(request, instance, type=None):
#     if instance.image:
#         if instance.image and '/' not in instance.image.name:
#             filename = instance.image.name
#             instance.image = shrinkImageFromData(instance.image.read(), filename, resize='fit')
#             instance.image.name = instance._meta.model._meta.get_field('image').upload_to(instance, filename)
#     return instance

# ############################################################
# # Badges

# def badgesBeforeSave(request, instance, type=None):
#     if instance.image:
#         if instance.image and '/' not in instance.image.name:
#             filename = instance.image.name
#             instance.image = shrinkImageFromData(instance.image.read(), filename, resize='cover')
#             instance.image.name = instance._meta.model._meta.get_field('image').upload_to(instance, filename)
#     return instance

# ############################################################
# # Account

# def getAccountForm(request, context, collection):
#     formClass = forms.AccountFormSimple
#     if 'advanced' in request.GET:
#         formClass = forms.AccountFormAdvanced
#         context['advanced'] = True
#     return formClass

# def leaderboardExtraContext(context):
#     request = context['request']
#     context['types'] = models.TYPE_CHOICES
#     context['favorite_characters'] = getattr(django_settings, 'FAVORITE_CHARACTERS', [])
#     context['starters'] = getattr(django_settings, 'STARTERS', [])
#     if 'favorite_character' in request.GET and request.GET['favorite_character']:
#         context['favorite_character_idol'] = models.Idol.objects.get(id=request.GET['favorite_character'])
#     if 'own_card' in request.GET and request.GET['own_card']:
#         context['own_card'] = models.Card.objects.get(id=request.GET['own_card'])

# def addAccountAfterSave(request, account):
#     if account.starter_id:
#         oc = models.OwnedCard.objects.create(card_id=account.starter_id, account=account)
#         account.center_id = oc.id
#         account.update_cache_center()
#         account.save()
#     return account

# def modAccountExtraContext(context):
#     context['starters'] = getattr(django_settings, 'STARTERS', [])

# def redirectAfterAddAccount(request, item, ajax):
#     return '/cards/?get_started'

# ############################################################
# # Events

# def eventsExtraContext(context):
#     request = context['request']
#     if 'idol' in request.GET and request.GET['idol']:
#         context['idol'] = models.Idol.objects.get(id=request.GET['idol'])

# ############################################################
# # Profile

# def profileGetAccountTabs(context):
#     from web.views import profileExtraContext
#     profileExtraContext(context)
#     request = context['request']
#     for account in context['item'].all_accounts:
#         show = request.GET.get('account{}'.format(account.id), 'Cards')
#         account.show = show if show in raw.ACCOUNT_TABS_LIST else 'Cards'
#     context['account_tabs'] = raw.ACCOUNT_TABS


# ############################################################
# # Owned Card

# def ownedCardRedirectAfter(request, item, ajax=False):
#     if ajax:
#         if 'collection' in request.GET:
#             return '/ajax/cardcollection/{}/'.format(item.card_id)
#         return '/ajax/card/{}/'.format(item.card_id)
#     if 'back_to_profile' in request.GET:
#         return item.account.owner.item_url
#     return item.card.item_url
