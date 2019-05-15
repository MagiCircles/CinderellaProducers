import random
from collections import OrderedDict
from django.conf import settings as django_settings
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.db.models import Q, Prefetch
from magi.forms import get_account_simple_form
from magi.magicollections import (
    MagiCollection,
    UserCollection as _UserCollection,
    AccountCollection as _AccountCollection,
    ActivityCollection as _ActivityCollection,
    BadgeCollection as _BadgeCollection,
    DonateCollection as _DonateCollection,
)
from magi.utils import (
    setSubField,
    torfc2822,
    CuteFormType,
    CuteFormTransform,
    FAVORITE_CHARACTERS_IMAGES,
    custom_item_template,
)
from cpro import models, forms, raw

############################################################
# Change settings of existing MagiCollections

############################################################
# User

# todo
# class UserCollection(_UserCollection):
#     class ItemView(_UserCollection.ItemView):
#         js_files = _UserCollection.ItemView.js_files + ['cards']

#         def extra_context(self, context):
#             super(UserCollection.ItemView, self).extra_context(context)
#             request = context['request']
#             for account in context['item'].all_accounts:
#                 show = request.GET.get('account{}'.format(account.id), 'Cards')
#                 account.show = show if show in raw.ACCOUNT_TABS_LIST else 'Cards'
#             context['account_tabs'] = raw.ACCOUNT_TABS

############################################################
# Account

class AccountCollection(_AccountCollection):
    navbar_link = False

    filter_cuteform = _AccountCollection.filter_cuteform.copy()
    filter_cuteform.update({
        'i_producer_rank': {
            'type': CuteFormType.HTML,
        },
        'accept_friend_requests': {
            'type': CuteFormType.YesNo,
        },
        'i_os': {
            'to_cuteform': lambda k, v: v.lower(),
            'transform': CuteFormTransform.FlaticonWithText,
        },
        'i_play_with': {
            'to_cuteform': lambda k, v: models.Account.PLAY_WITH[
                models.Account.get_reverse_i('play_with', k)]['icon'],
            'transform': CuteFormTransform.FlaticonWithText,
        },
        'starter': {
            'to_cuteform': lambda k, v: django_settings.STARTERS[k]['icon'],
        },
        'center_type': {
            'image_folder': 'color',
        },
        'center': {
            'to_cuteform': lambda k, oc: oc.icon_url,
            'extra_settings': {
	        'modal': 'true',
                'modal-text': 'true',
            },
        },
        'center_rarity': {
            'type': CuteFormType.HTML,
            'to_cuteform': lambda k, v: models.Card.get_reverse_i('rarity', k),
        },
    })
    form_class = forms.AccountForm

    class ListView(_AccountCollection.ListView):
        before_template = 'include/beforeLeaderboard'
        item_template = custom_item_template
        filter_form = forms.AccountFilterForm
        ajax_callback = 'loadAccountFilters'

        # todo when collectibles are ready
        # def get_queryset(self, queryset, parameters, request):
        #     if 'own_card' in parameters and parameters['own_card']:
        #         queryset = queryset.filter(ownedcards__card__id=parameters['own_card'])
        #     if 'favorite_card' in parameters and parameters['favorite_card']:
        #         queryset = queryset.filter(owner__favoritecards__card__id=parameters['favorite_card'])
        #     return queryset

        # todo
        # def aextra_context(self, context):
        #     super(AccountCollection.ListView, self).extra_context(context)
        #     context['types'] = models.TYPES

        #     if 'idol' in context['request'].GET and context['request'].GET['idol']:
        #         context['idol'] = models.Idol.objects.filter(id__in=context['request'].GET['idol'].split(','))[0]
        #     if 'own_card' in context['request'].GET and context['request'].GET['own_card']:
        #         context['own_card'] = models.Card.objects.get(id=context['request'].GET['own_card'])

    class ItemView(_AccountCollection.ItemView):
        template = custom_item_template

    class AddView(_AccountCollection.AddView):
        back_to_list_button = False
        simpler_form = get_account_simple_form(forms.AccountForm, simple_fields=[
            'friend_id', 'level', 'starter',
        ])

        def after_save(self, request, account, type=None):
            super(AccountCollection.AddView, self).after_save(request, account, type=type)
            # Add starter as first card
            if account.starter_id:
                oc = models.OwnedCard.objects.create(card_id=account.starter_id, account=account)
                account.center_id = oc.id
                account.update_cache_center()
                account.save()
            return account

        def redirect_after_add(self, request, item, ajax):
            return '/cards/?get_started'

############################################################
# Activity

class ActivityCollection(_ActivityCollection):
    class ListView(_ActivityCollection.ListView):
        pass
        #before_template = 'include/index'
        #full_width = True

        # def extra_context(self, context):
        # todo
        #     super(ActivityCollection.ListView, self).extra_context(context)
        #     if context.get('shortcut_url', None) == '':
        #         context['page_title'] = context['site_description']
        #         context['card'] = models.Card.objects.order_by('?').filter(art__isnull=False).exclude(art='').exclude(art_on_homepage=False, art_awakened_on_homepage=False)[0]
        #         if not context['card'].art_on_homepage:
        #             context['awakened'] = True
        #         elif not context['card'].art_awakened_on_homepage:
        #             context['awakened'] = False
        #         else:
        #             context['awakened'] = random.choice([True, False]) if context['card'].id_awakened else False

############################################################
# Badge

class BadgeCollection(_BadgeCollection):
    enabled = True

class DonateCollection(_DonateCollection):
    enabled = True

############################################################
############################################################
############################################################

############################################################
# Cinderella Producers original collections

############################################################
# Card

class CardCollection(MagiCollection):
    queryset = models.Card.objects.all()
    name = 'deresute/card'
    plural_name = 'deresute/cards'
    title = _('Card')
    plural_title = _('Cards')
    icon = 'cards'
    reportable = False
    blockable = False
    navbar_link_list = 'cinderellagirls'

    filter_cuteform = {
        'i_rarity': {
            'type': CuteFormType.HTML,
            'to_cuteform': lambda k, v: models.Card.get_reverse_i('rarity', k),
        },
        'i_type': {
            'image_folder': 'color',
        },
    }
    filter_cuteform.update({
        _field: {
            'type': CuteFormType.YesNo,
        } for _field in ['is_event', 'is_limited', 'has_art', 'has_2x_art']
    })
        # 'type': {
        #     'image_folder': 'color',
        # },
        # 'is_event': {
        #     'type': CuteFormType.OnlyNone,
        # },
        # 'is_awakened': {
        #     'type': CuteFormType.OnlyNone,
        # },
        # 'is_limited': {
        #     'type': CuteFormType.OnlyNone,
        # },
        # 'is_limited': {
        #     'type': CuteFormType.OnlyNone,
        # },
        # 'has_art': {
        #     'type': CuteFormType.OnlyNone,
        # },

    # def queryset_total_owned_and_favorited(self, queryset, request):
    #     if request.user.is_authenticated():
    #         request.user.all_accounts = request.user.accounts.all()
    #         accounts_pks = ','.join([str(account.pk) for account in request.user.all_accounts])
    #         if accounts_pks:
    #             queryset = queryset.extra(select={
    #                 'total_owned': 'SELECT COUNT(*) FROM cpro_ownedcard WHERE card_id = cpro_card.id AND account_id IN ({})'.format(accounts_pks),
    #                 'favorited': 'SELECT COUNT(*) FROM cpro_favoritecard WHERE card_id = cpro_card.id AND owner_id IN ({})'.format(request.user.id),
    #             })
    #     return queryset

    class ListView(MagiCollection.ListView):
        default_ordering = '-release_date'
        filter_form = forms.CardFilterForm
        # ajax_pagination_callback = 'updateCards' todo
        per_line = 3
        item_padding = (15, 0, 0, 0)
        item_buttons_classes = ['btn', 'btn-white', 'btn-circle', 'btn-lg' ]
        show_item_buttons_as_icons = True
        show_item_buttons_justified = False
        show_item_buttons_in_one_line = False
        # js_files = ['cards'] # todo
        # filter_form = forms.FilterCards todo
        # before_template = 'include/beforeCards' todo
        # after_template = 'include/afterCards' todo

        # OrderedDict([('edit', {'ajax_url': u'/ajax/deresute/cards/edit/100577/', 'classes': ['btn', 'btn-secondary', 'btn-lines', 'staff-only'], 'ajax_title': False, 'show': True, 'url': u'/deresute/cards/edit/100577/', 'image': False, 'title': u'Edit card', 'open_in_new_window': False, 'has_permissions': True, 'icon': 'edit'}), ('translate', {'ajax_url': False, 'classes': ['btn', 'btn-secondary', 'btn-lines'], 'ajax_title': False, 'show': False, 'url': False, 'image': False, 'title': 'translate', 'open_in_new_window': False, 'has_permissions': False, 'icon': False}), ('report', {'ajax_url': False, 'classes': ['btn', 'btn-secondary', 'btn-lines'], 'ajax_title': False, 'show': False, 'url': False, 'image': False, 'title': 'report', 'open_in_new_window': False, 'has_permissions': False, 'icon': False})])
        def buttons_per_item(self, request, context, item):
            # show, has_permissions, title, url, classes and may contain icon, image, url, open_in_new_window, ajax_url, ajax_title. Can be specified in collection.
            buttons = OrderedDict([
                ('info', {
                    'show': True, 'has_permissions': True,
                    'title': _('Open {thing}').format(thing=_('Card').lower()),
                    'url': item.item_url,
                    'ajax_url': item.ajax_item_url,
                    'ajax_title': unicode(item),
                    'classes': self.item_buttons_classes,
                    'icon': 'about',
                })
            ])
            buttons.update(super(CardCollection.ListView, self).buttons_per_item(request, context, item))
            buttons['edit']['classes'] = self.item_buttons_classes # todo remove
            return buttons

        # todo
        def aextra_context(self, context):
            request = context['request']
            context['get_started'] = 'get_started' in request.GET
            context['next'] = request.GET.get('next', None)
            context['next_title'] = request.GET.get('next_title', None)
            context['favorite_of'] = request.GET.get('favorite_of', None)
            if context['is_last_page']:
                context['share_sentence'] = _('Check out my collection of cards!')
            if 'event' in request.GET and request.GET['event']:
                context['event'] = models.Event.objects.get(id=request.GET['event'])
            elif 'idol' in request.GET and request.GET['idol']:
                context['idol'] = models.Idol.objects.get(id=request.GET['idol'])

        # todo
        def aget_queryset(self, queryset, parameters, request):
            queryset = self.collection.queryset_total_owned_and_favorited(queryset, request)
            if 'favorite_of' in parameters and parameters['favorite_of']:
                queryset = queryset.filter(fans__owner_id=parameters['favorite_of'])
            if 'ids' in parameters and parameters['ids']:
                queryset = queryset.filter(id__in=parameters['ids'].split(','))
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
            if 'idol' in parameters and parameters['idol']:
                queryset = queryset.filter(idol=parameters['idol'])
            if 'event' in parameters and parameters['event']:
                queryset = queryset.filter(event=parameters['event'])
            return queryset

    class ItemView(MagiCollection.ItemView):
        ajax_callback = 'updateCardsAndOwnedCards'
        js_files = ['cards', 'collection']
        show_edit_button = False

        def extra_context(self, context):
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

        def get_queryset(self, queryset, parameters, request):
            return self.collection.queryset_total_owned_and_favorited(queryset, request)

    class AddView(MagiCollection.AddView):
        staff_required = True
        # todo form_class = forms.CardForm
        multipart = True
        staff_required = True

    class EditView(MagiCollection.EditView):
        # todo form_class = forms.CardForm
        multipart = True
        staff_required = True

############################################################
# Owned Card

class OwnedCardCollection(MagiCollection):
    queryset = models.OwnedCard.objects.all().select_related('card')
    title = _('Card')
    plural_title = _('Cards')
    icon = 'album'
    navbar_link = False
    reportable = False

    filter_cuteform = {
        'i_rarity': {
            'type': CuteFormType.HTML,
            'to_cuteform': lambda k, v: models.RARITY_SHORT_DICT[k],
        },
        'type': {
            'image_folder': 'color',
        },
        'is_event': {
            'type': CuteFormType.OnlyNone,
        },
    }

    class ListView(MagiCollection.ListView):
        default_ordering = '-card__i_rarity,-awakened,-card__release_date,card__idol__i_type'
        per_line = 6
        page_size = 48
        col_break = 'xs'
        # filter_form = forms.FilterOwnedCards todo
        ajax_callback = 'reloadOwnedCardsAfterModalNotProfile'
        ajax_pagination_callback = 'updateOwnedCards'
        show_edit_button = False
        before_template = 'include/beforeOwnedCards'
        js_files = ['ownedcards']

        def get_queryset(self, queryset, parameters, request):
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

        def foreach_items(self, index, item, context):
            item.is_mine = context['request'].user.id == item.cached_account.owner.id

    class ItemView(MagiCollection.ItemView):
        show_edit_button = False
        comments_enabled = False
        ajax_callback = 'reloadOwnedCardsAfterModalNotProfile'
        js_files = ['ownedcards']

    class AddView(MagiCollection.AddView):
        enabled = False

    class EditView(MagiCollection.EditView):
        # todo form_class = forms.EditOwnedCardForm
        allow_delete = True
        back_to_list_button = False
        js_files = ['edit_ownedcard']

        def get_queryset(self, queryset, parameters, request):
            # Used when checking if the center has been updated
            return queryset.select_related('account')

        def _redirect_after_edit_or_delete(self, request, item, ajax):
            if ajax:
                if 'collection' in request.GET:
                    return '/ajax/cardcollection/{}/'.format(item.card_id)
                return '/ajax/card/{}/'.format(item.card_id)
            if 'back_to_profile' in request.GET:
                return item.account.owner.item_url
            return item.card.item_url

        redirect_after_edit   = _redirect_after_edit_or_delete
        redirect_after_delete = _redirect_after_edit_or_delete

############################################################
# Idol

class IdolCollection(MagiCollection):
    queryset = models.Idol.objects.all()
    name = 'cinderellagirls/idol'
    plural_name = 'cinderellagirls/idols'
    title = _('Idol')
    plural_title = _('Idols')
    icon = 'idolized'
    navbar_link_list = 'cinderellagirls'

    reportable = False
    blockable = False

    form_class = forms.getIdolForm(models.Idol)
    multipart = True

    filter_cuteform = {
        'i_type': {
            'image_folder': 'color',
        },
        'i_astrological_sign': {
        },
        'i_blood_type': {
            'type': CuteFormType.HTML,
        },
        'i_writing_hand': {
            'type': CuteFormType.HTML,
        },
        'has_signature': {
            'type': CuteFormType.YesNo,
        },
        'has_cv': {
            'type': CuteFormType.YesNo,
        },
    }

    fields_icons = {
        'name': 'id',
        'japanese_name': 'id',
        'cards': 'cards',
        'events': 'event',
        'fans': 'users',
        'age': 'scoreup',
        'birthday': 'event',
        'height': 'measurements',
        'weight': 'scoreup',
        'blood_type': 'hp',
        'writing_hand': 'fingers',
        'bust': 'measurements',
        'waist': 'measurements',
        'hips': 'measurements',
        'hometown': 'home',
        'romaji_hometown': 'home',
        'hobbies': 'star',
        'description': 'description',
        'cv': 'voice-actress',
        'romaji_cv': 'voice-actress',
        'signature': 'author',
        'description': 'about',
    }

    fields_images = {
        'type': lambda _item: _item.type_image_url,
        'astrological_sign': lambda _item: _item.astrological_sign_image_url,
    }

    class ListView(MagiCollection.ListView):
        filter_form = forms.IdolFilterForm
        default_ordering = '-_cache_total_fans'

        per_line = 4
        item_padding = (0, 10)
        show_items_names = True

        ajax_callback = 'loadIdolFilters'

    class AddView(MagiCollection.AddView):
        staff_required = True
        permissions_required = ['manage_main_items']

    class EditView(MagiCollection.EditView):
        staff_required = True
        permissions_required = ['manage_main_items']
        allow_delete = True

############################################################
# Event

class EventCollection(MagiCollection):
    queryset = models.Event.objects.all()
    name = 'deresute/event'
    plural_name = 'deresute/events'
    title = _('Event')
    plural_title = _('Events')
    icon = 'event'
    reportable = False
    blockable = False

    navbar_link_list = 'cinderellagirls'

    def to_fields(self, item, to_dict=True, only_fields=None, in_list=False):
        fields = super(EventCollection, self).to_fields(item, to_dict=False, only_fields=only_fields, in_list=in_list)
        status = item.status
        if status and status != 'ended' and (not only_fields or 'countdown' in only_fields):
            fields.insert(0, ('countdown', {
                'verbose_name': _('Countdown'),
                'value': mark_safe(u'<h4 class="countdown" data-date="{date}" data-format="{left_sentence}"></h4>'.format(date=torfc2822(item.end if status == 'current' else item.beginning), left_sentence=_('{time} left') if status == 'current' else _('Starts in {time}'))),
                'icon': 'times',
            }))
        fields = OrderedDict(fields)
        # Set icons and images
        setSubField(fields, 'name', value='JP')
        setSubField(fields, 'translated_name', value='world')
        setSubField(fields, 'kind', value='event')
        setSubField(fields, 'cards', value='cards')
        for field_name in ['beginning', 'end']:
            setSubField(fields, field_name, value='date')
            setSubField(fields, field_name, key='type', value='timezone_datetime')
            setSubField(fields, field_name, key='timezones', value=['Asia/Tokyo', 'Local time'])
        for i in range(1, 6):
            setSubField(fields, 't{}_rank'.format(i), value='contest')
        for i in range(1, 6):
            setSubField(fields, 't{}_points'.format(i), value='scoreup')
        setSubField(fields, '', key='value', value=lambda field_name: '{} '.format(fields[field_name]['value']))
        return fields if to_dict else fields.items()

    class ListView(MagiCollection.ListView):
        default_ordering = '-end'
        per_line = 1
        item_template = 'default'
        before_template = 'include/beforeEvents'
        # todo filter_form = forms.FilterEvents

        def get_queryset(self, queryset, parameters, request):
            if 'search' in parameters and parameters['search']:
                terms = parameters['search'].split(' ')
                for term in terms:
                    queryset = queryset.filter(Q(name__icontains=term)
                                               | Q(translated_name__icontains=term)
                    )
            if 'i_kind' in parameters and parameters['i_kind']:
                queryset = queryset.filter(i_kind=parameters['i_kind'])
            if 'idol' in parameters and parameters['idol']:
                queryset = queryset.filter(cards__idol=parameters['idol'])
            return queryset

        def extra_context(self, context):
            request = context['request']
            if 'idol' in request.GET and request.GET['idol']:
                context['idol'] = models.Idol.objects.get(id=request.GET['idol'])

    class ItemView(MagiCollection.ItemView):
        template = 'default'
        js_files = ['event']

    class AddView(MagiCollection.AddView):
        # todo form_class = forms.EventForm
        multipart = True
        staff_required = True

    class EditView(MagiCollection.EditView):
        # todo form_class = forms.EventForm
        multipart = True
        staff_required = True
