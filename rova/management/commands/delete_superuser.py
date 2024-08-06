from django.core.management.base import BaseCommand
from rova.models import CustomUser

from django.core.management.base import BaseCommand
from rova.models import CustomUser  # Adjust the import based on your actual app and model name

class Command(BaseCommand):
    help = 'Delete a superuser account'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='The username of the superuser to delete')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        try:
            user = CustomUser.objects.get(username=username, is_superuser=True)
            user.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted superuser {username}'))
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Superuser {username} does not exist'))

