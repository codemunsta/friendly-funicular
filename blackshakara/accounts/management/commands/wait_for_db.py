import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError

from psycopg2 import OperationalError as PGOpError


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Awaiting database ...')
        db_started = False
        while db_started is False:
            try:
                self.check(databases=['default'])
                db_started = True
            except (PGOpError, OperationalError):
                self.stdout.write('unavailable... rerouting...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available'))
