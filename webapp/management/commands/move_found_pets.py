from django.core.management.base import BaseCommand
from webapp.models import Pet
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Move found pets to adoption status after 15 days'

    def handle(self, *args, **options):
        # Find pets that are marked as 'found' and have been found for 15+ days
        cutoff_date = timezone.now() - timedelta(days=15)
        
        found_pets = Pet.objects.filter(
            status='found',
            found_date__isnull=False,
            found_date__lte=cutoff_date
        )
        
        moved_count = 0
        for pet in found_pets:
            if pet.auto_move_to_adoption():
                moved_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Moved "{pet.name}" (ID: {pet.id}) from found to adoption'
                    )
                )
        
        if moved_count == 0:
            self.stdout.write(
                self.style.WARNING('No pets needed to be moved to adoption')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully moved {moved_count} pet(s) to adoption status'
                )
            )