from django import template
from cpro.model_choices import PLAY_WITH_ICONS

register = template.Library()

@register.filter
def torfc2822(date):
    return date.strftime("%B %d, %Y %H:%M:%S %z")

@register.filter
def play_with_to_icon(play_with):
    return PLAY_WITH_ICONS[play_with]
