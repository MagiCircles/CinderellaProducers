from web.utils import globalContext as web_globalContext
from cpro import raw, models

def globalContext(request):
    context = web_globalContext(request)
    return context

def onPreferencesEdited(request):
    accounts = models.Account.objects.filter(owner_id=request.user.id).select_related('owner', 'owner__preferences')
    for account in accounts:
        account.force_cache_owner()
