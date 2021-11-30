from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from os import environ
import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        master = environ.get('MASTER', 'master')
        User = get_user_model()
        if not User.objects.filter(username=master).exists():
            User.objects.create_superuser(
                master, '', environ.get('MASTER_PASS', 'master'))
            logger.info('Created master account')
        else:
            logger.info('Master exist')
