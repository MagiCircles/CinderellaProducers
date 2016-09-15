from cpro import forms, raw

############################################################
# Account

def getAccountForm(request, context, collection):
    formClass = forms.AccountFormSimple
    if 'advanced' in request.GET:
        formClass = forms.AccountFormAdvanced
        context['advanced'] = True
    return formClass

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
# Owned Card

def ownedCardRedirectAfter(request, item, ajax=False):
    if ajax:
        return '/ajax/card/{}/'.format(item.card_id)
    if 'back_to_profile' in request.GET:
        return item.account.owner.item_url
    return item.card.item_url

def foreachOwnedCard(index, item, context):
    item.is_mine = context['request'].user.id == item.cached_account.owner.id
