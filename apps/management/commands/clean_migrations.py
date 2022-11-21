import os
import glob

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Delete all migration files except __init__."

    def handle(self, *args, **options):
        try:
            SITE_ROOT = os.path.abspath(os.path.dirname(__file__) + "../" * 4)
            dir_path = f"{SITE_ROOT}/apps/migrations/*.*"
            files = glob.glob(dir_path)
            for filename in files:
                if filename.endswith("__init__.py"):
                    continue
                self.stdout.write(f"Removing: {filename}")
                os.remove(filename)
        except Exception as e:
            raise CommandError(f"Failed to clean migrations folder: {e}")
        self.stdout.write(self.style.SUCCESS("Successfully cleaned migrations folder."))
