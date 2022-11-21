from django.core.management.base import BaseCommand, CommandError


from apps.seeds import main as seed


class Command(BaseCommand):
    help = "Seeds database."

    def handle(self, *args, **options):
        try:
            seed()
        except Exception as e:
            raise CommandError(f"Failed to seed database: {e}")
        self.stdout.write(self.style.SUCCESS("Successfully seeded database"))
