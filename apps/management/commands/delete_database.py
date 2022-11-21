import os

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Delete db.sqlite3 file."

    def handle(self, *args, **options):
        try:
            SITE_ROOT = os.path.abspath(os.path.dirname(__file__) + "../" * 4)
            filename = f"{SITE_ROOT}/db.sqlite3"

            if os.path.exists(filename):
                self.stdout.write(f"Removing: {filename}")
                os.remove(filename)
            else:
                self.stdout.write(f"{filename} already removed.")
        except Exception as e:
            raise CommandError(f"Failed to delete db.sqlite3 file: {e}")
        self.stdout.write(self.style.SUCCESS("Successfully deleted db.sqlite3 file"))
