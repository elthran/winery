from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Reset database."

    def handle(self, *args, **options):
        try:
            call_command("delete_database")
            call_command("clean_migrations")
            call_command("makemigrations")
            call_command("migrate")
            call_command("seed")
        except Exception as e:
            raise CommandError(f"Failed to reset database: {e}")
        self.stdout.write(self.style.SUCCESS("Successfully reset database"))
