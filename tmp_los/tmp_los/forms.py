from magi.forms import AutoForm
from tmp_los import models

class IdolForm(AutoForm):
    class Meta(AutoForm.Meta):
        model = models.Idol
        save_owner_on_creation = True
