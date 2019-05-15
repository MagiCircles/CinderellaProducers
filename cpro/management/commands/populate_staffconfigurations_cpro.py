from django.core.management.base import BaseCommand
from magi.management.commands.populate_staffconfigurations import create

class Command(BaseCommand):
    def handle(self, *args, **options):
        create({
            'key': 'account_max_level',
            'verbose_key': 'Maximum level to set on an account',
        })
