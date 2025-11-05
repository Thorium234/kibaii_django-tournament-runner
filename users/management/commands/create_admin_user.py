from django.core.management.base import BaseCommand
from users.models import CustomUser

class Command(BaseCommand):
    help = 'Creates a superuser non-interactively'

    def handle(self, *args, **kwargs):
        if not CustomUser.objects.filter(username='admin').exists():
            CustomUser.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Successfully created superuser admin.'))
        else:
            self.stdout.write(self.style.WARNING('Superuser admin already exists.'))
