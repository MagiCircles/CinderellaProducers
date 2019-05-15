from __future__ import division
import tinify, cStringIO, os
from PIL import Image
from django.conf import settings as django_settings
from django.core.files.temp import NamedTemporaryFile
from django.core.files.images import ImageFile
from magi.utils import globalContext as magi_globalContext
from cpro import raw, models

def globalContext(request):
    context = magi_globalContext(request)
    return context

def onUserEdited(request):
    # todo
    accounts = models.Account.objects.filter(owner_id=request.user.id).select_related('owner', 'owner__preferences')
    for account in accounts:
        account.force_cache_owner()

def onPreferencesEdited(request):
    # todo
    accounts = models.Account.objects.filter(owner_id=request.user.id).select_related('owner', 'owner__preferences')
    for account in accounts:
        account.force_cache_owner()

def dataToImageFile(data):
    # todo
    image = NamedTemporaryFile(delete=False)
    image.write(data)
    image.flush()
    return ImageFile(image)

def shrinkImageFromData(data, filename, resize=None):
    # todo
    _, extension = os.path.splitext(filename)
    extension = extension.lower()
    api_key = getattr(django_settings, 'TINYPNG_API_KEY', None)
    if not api_key or extension not in ['.png', '.jpg', '.jpeg']:
        return dataToImageFile(data)
    tinify.key = api_key
    source = tinify.from_buffer(data)
    if resize == 'fit':
        image = Image.open(cStringIO.StringIO(data))
        width, height = image.size
        if width > django_settings.MAX_WIDTH:
            height = (django_settings.MAX_WIDTH / width) * height
            width = django_settings.MAX_WIDTH
        if height > django_settings.MAX_HEIGHT:
            width = (django_settings.MAX_HEIGHT / height) * width
            height = django_settings.MAX_HEIGHT
        if height < django_settings.MIN_HEIGHT:
            height = django_settings.MIN_HEIGHT
        if width < django_settings.MIN_WIDTH:
            width = django_settings.MIN_WIDTH
        source = source.resize(
            method='fit',
            width=int(width),
            height=int(height),
        )
    elif resize == 'cover':
        print 'resize cover'
        source = source.resize(
            method='cover',
            width=300,
            height=300,
        )
    try:
        data = source.to_buffer()
    except: # Retry without resizing
        try:
            data = tinify.from_buffer(data).to_buffer()
        except: # Just return the original data
            pass
    return dataToImageFile(data)
