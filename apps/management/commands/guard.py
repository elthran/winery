import os
import sys

from watchgod import watch

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Watch files; run test suite on changes."

    def handle(self, *args, **options):
        self.stdout.write("Watching files, press ctrl+c to exit.")

        self.safe_run_test_suite()

        for changes in watch(settings.BASE_DIR):
            os.execv(sys.argv[0], sys.argv)
            # self.safe_run_test_suite()
            # https://watchfiles.helpmanual.io/api/watch/#watchfiles.watch
            # If test watching becomes too slow, use "changes",
            # to inteligently run specific tests.
            # https://github.com/guard/guard/wiki/Guardfile-DSL---Configuring-Guard
            # for change in changes:
            #     change_type, path = change
            #     print(change_type)
            #     print(path)

        self.stdout.write(self.style.SUCCESS("\nFinished watching files."))

    def safe_run_test_suite(self):
        try:
            call_command("test")
        except SystemExit as e:
            # "test" command raised sys.exit(1), because a test failed.
            # We don't care, because we want to keep watching for file changes.
            if e.args == (1,):
                return

            self.stderr.write(self.style.ERROR(f"Test suite crashed: {e}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Test suite crashed: {e}"))
