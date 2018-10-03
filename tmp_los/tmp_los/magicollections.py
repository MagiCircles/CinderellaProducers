from magi.magicollections import MagiCollection
from tmp_los import models, forms

# Create your magicollections here.

class IdolCollection(MagiCollection):
    queryset = models.Idol.objects.all()
    multipart = True
    form_class = forms.IdolForm
    icon = 'idolized'
