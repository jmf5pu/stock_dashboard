from django.core.management.base import BaseCommand
from stock.models import Member

class Command(BaseCommand):
    help = "deletes all objects in the database"

    def handle(self, *args, **options):
        Member.objects.all().delete()
        print("completed")

