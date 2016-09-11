from cpro import forms

def getAccountForm(request, context, collection):
    formClass = forms.AccountFormSimple
    if 'advanced' in request.GET:
        formClass = forms.AccountFormAdvanced
        context['advanced'] = True
    return formClass
