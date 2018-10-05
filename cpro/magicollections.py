from magi.magicollections import (
    MagiCollection,
    AccountCollection as _AccountCollection,
    ActivityCollection as _ActivityCollection,
    BadgeCollection as _BadgeCollection,
    UserCollection as _UserCollection
)

from cpro import models, forms, filters, collections_settings, utils

############################################################
# Account Collection 

class AccountCollection(_AccountCollection):
    class AddView(_AccountCollection.AddView):
        after_save            = collections_settings.addAccountAfterSave
        after_template        = 'include/accountJSstarter'
        back_to_list_button   = False
        extra_context         = collections_settings.modAccountExtraContext
        form_class = collections_settings.getAccountForm
        # TODO: Not sure how to handle the ENABLED_COLLECTIONS here
        js_files              = ENABLED_COLLECTIONS['account']['add'].get('js_files', []) + ['mod_account']
        otherbuttons_template = 'include/advancedButton'
        redirect_after_add    = collections_settings.redirectAfterAddAccount

    class EditView(_AccountCollection.EditView):
        after_template = 'include/accountJSstarter'
        extra_context  = collections_settings.modAccountExtraContext
        form_class     = forms.AccountFormAdvanced
        # TODO: Not sure how to handle the ENABLED_COLLECTIONS here
        js_files       = ENABLED_COLLECTIONS['account']['edit'].get('js_files', []) + ['mod_account']

    class ListView(_AccountCollection.ListView):
        before_template  = 'include/beforeLeaderboard'
        distinct         = True
        default_ordering = '-level'
        extra_context    = collections_settings.leaderboardExtraContext
        filter_form      = forms.FilterAccounts
        # TODO: Replaced by get_queryset
        filter_queryset  = filters.filterAccounts
        # TODO: Not sure how to handle the ENABLED_COLLECTIONS here
        js_files         = ENABLED_COLLECTIONS['account']['list'].get('js_files', []) + ['leaderboard']
        # TODO: Not sure if this lambda works
        show_add_button  = lambda request: not request.user.is_authenticated()

############################################################
# Activity Collection

class ActivityCollection(_ActivityCollection):
    # TODO: Not sure if this is ported properly since it's directly taken from the old `settings.py` file
    ACTIVITY_TAGS = [
        ('cards', _('New Cards')),
        ('event', _('Event')),
        ('live', _('Live')),
        ('comedy', _('Comedy')),
        ('room', _('Room Decoration')),
        ('introduction', _('Introduce yourself')),
        ('idols', _('Idols')),
        ('anime', _('Anime')),
        ('cosplay', _('Cosplay')),
        ('fanart', _('Fan made')),
        ('merch', _('Merchandise')),
        ('community', _('Community')),
        ('unrelated', _('Unrelated')),
        ('AR Idol Date', 'AR Idol Date'),
    ]

    # TODO: Not sure if this is ported properly since it's directly taken from the old `settings.py` file
    def filterActivitiesList(queryset, parameters, request):
        if request.user.is_superuser and 'force_old' in request.GET:
            if 'owner_id' in request.GET:
                return queryset.filter(owner_id=request.GET['owner_id'])
            return queryset
        return queryset.filter(id__gt=2600)

    # TODO: Not sure if this is ported properly since it's directly taken from the old `settings.py` file
    def filterActivities(queryset, parameters, request):
        if request.user.is_superuser:
            return queryset
        return filterActivitiesList(queryset, parameters, request)

    class AddView(_ActivityCollection.AddView):
        before_save     = collections_settings.activitiesBeforeSave
        # TODO: Replaced by get_queryset
        filter_queryset = filterActivities

    class EditView(_ActivityCollection.EditView):
        before_save     = collections_settings.activitiesBeforeSave
        # TODO: Replaced by get_queryset
        filter_queryset = filterActivities

    class ItemView(_ActivityCollection.ItemView):
        # TODO: Replaced by get_queryset
        filter_queryset = filterActivities

    class ListView(_ActivityCollection.ListView):
        # TODO: Replaced by get_queryset
        filter_queryset = filterActivitiesList

############################################################
# Badge Collection 

class BadgeCollection(_BadgeCollection):
    class AddView(_BadgeCollection.AddView):
        before_save = collections_settings.badgesBeforeSave

    class EditView(_BadgeCollection.EditView):
        before_save = collections_settings.badgesBeforeSave

############################################################
# Card Collection 

class CardCollection(MagiCollection):
    queryset     = models.Card.object.all()
    title        = _('Card')
    plural_title = _('Cards')
    icon         = 'cards'

    class AddView(MagiCollection.AddView):
        form_class     = forms.CardForm
        multipart      = True
        staff_required = True

    class EditView(MagiCollection.EditView):
        form_class     = forms.CardForm
        multipart      = True
        staff_required = True

    class ItemView(MagiCollection.ItemView):
        ajax_callback   =  'updateCardsAndOwnedCards'
        extra_context   = collections_settings.cardExtraContext
        # TODO: Replaced by get_queryset
        filter_queryset = filters.filterCard
        js_files        = ['cards', 'collection']

    class ListView(MagiCollection.ListView):
        after_template           = 'include/afterCards'
        ajax_pagination_callback = 'updateCards'
        before_template          = 'include/beforeCards'
        default_ordering         = '-release_date'
        extra_context            = collections_settings.cardsExtraContext
        filter_form              = forms.FilterCards
        # TODO: Replaced by get_queryset
        filter_queryset          = filters.filterCards
        full_width               = True
        js_files                 = ['cards']

############################################################
# Event Collection 

class EventCollection(MagiCollection):
    queryset     = models.Event.objects.all()
    title        = _('Event')
    plural_title = _('Events')
    icon         = 'event'

    class AddView(MagiCollection.AddView):
        form_class     = forms.EventForm
        multipart      = True
        staff_required = True

    class EditView(MagiCollection.EditView):
        form_class     = forms.EventForm
        multipart      = True
        staff_required = True

    class ItemView(MagiCollection.ItemView):
        js_files = ['bower/countdown/dest/jquery.countdown.min', 'event']
        template = 'eventInfo'

    class ListView(MagiCollection.ListView):
        default_ordering         = '-end'
        extra_context            = collections_settings.eventsExtraContext
        filter_form              = forms.FilterEvents
        # TODO: Replaced by get_queryset
        filter_queryset          = filters.filterEvents
        per_line                 = 1

############################################################
# Idol Collection 

class IdolCollection(MagiCollection):
    queryset     = models.Idol.objects.all(),
    title        = _('Idol')
    plural_title = _('Idols')
    icon         = 'idolized'

    class AddView(MagiCollection.AddView):
        form_class     = forms.IdolForm
        multipart      = True
        staff_required = True

    class EditView(MagiCollection.EditView):
        form_class     = forms.IdolForm
        multipart      = True
        staff_required = True

    class ItemView(MagiCollection.ItemView):
        js_files = ['idolInfo']
        template = 'idolInfo'

    class ListView(MagiCollection.ListView):
        ajax_pagination_callback = 'ajaxModals'
        default_ordering         = '-_cache_total_fans'
        extra_context            = collections_settings.idolsExtraContext
        filter_form              = forms.FilterIdols
        # TODO: Replaced by get_queryset
        filter_queryset          = filters.filterIdols
        js_files                 = ['idols']
        per_line                 = 4

############################################################
# Owned Card Collection 

class OwnedCardCollection(MagiCollection):
    queryset     = models.OwnedCard.objects.all().select_related('card')
    title        = _('Card')
    plural_title = _('Cards')
    icon         = 'album'
    navbar_link  = False

    class EditView(MagiCollection.EditView):
        allow_delete          = True
        back_to_list_button   = False
        # TODO: Replaced by get_queryset, not sure if this lambda works
        filter_queryset       = lambda q, p, r: q.select_related('account')
        form_class            = forms.EditOwnedCardForm,
        js_files              = ['edit_ownedcard']
        redirect_after_edit   = collections_settings.ownedCardRedirectAfter
        redirect_after_delete = collections_settings.ownedCardRedirectAfter

    class ItemView(MagiCollection.ItemView):
        comments_enabled = False
        js_files         = ['ownedcards']

    class ListView(MagiCollection.ListView):
        ajax_pagination_callback = 'updateOwnedCards'
        before_template          = 'include/beforeOwnedCards'
        col_break                = 'xs'
        default_ordering         = '-card__i_rarity,-awakened,-card__release_date,card__idol__i_type'
        filter_form              = forms.FilterOwnedCards
        # TODO: Replaced by get_queryset
        filter_queryset          = filters.filterOwnedCards
        foreach_items            = collections_settings.foreachOwnedCard
        js_files                 = ['ownedcards']
        page_size                = 48
        per_line                 = 6

############################################################
# User Collection 

class UserCollection(_UserCollection):
    class ItemView(_UserCollection.ItemView):
        extra_context = collections_settings.profileGetAccountTabs
        # TODO: Not sure how to handle the ENABLED_COLLECTIONS here
        js_files      = ENABLED_COLLECTIONS['user']['item'].get('js_files', []) + ['profile_account_tabs', 'cards']

