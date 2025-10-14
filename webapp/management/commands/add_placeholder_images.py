from django.core.management.base import BaseCommand
from webapp.models import Pet
from django.core.files.base import ContentFile
import requests
from io import BytesIO

class Command(BaseCommand):
    help = 'Assign placeholder images to pets without images'

    def handle(self, *args, **options):
        # Free placeholder image services for different animals
        placeholder_urls = {
            'dog': [
                'https://place.dog/500/500',
                'https://placedog.net/500/500?random=1',
                'https://placedog.net/500/500?random=2',
                'https://placedog.net/500/500?random=3',
                'https://placedog.net/500/500?random=4',
            ],
            'cat': [
                'https://placekitten.com/500/500',
                'https://placekitten.com/g/500/500',
                'https://placekitten.com/501/501',
                'https://placekitten.com/502/502',
                'https://placekitten.com/503/503',
            ]
        }
        
        # For birds and rabbits, we'll use simple color backgrounds with emojis
        # since there aren't good placeholder services for these
        
        updated_count = 0
        
        # Get pets without images
        pets_without_images = Pet.objects.filter(image__isnull=True) | Pet.objects.filter(image='')
        
        for pet in pets_without_images:
            image_url = None
            
            # Get appropriate placeholder
            if pet.species in placeholder_urls:
                # Use index to get different images for different pets
                pet_index = pet.id % len(placeholder_urls[pet.species])
                image_url = placeholder_urls[pet.species][pet_index]
            
            if image_url:
                try:
                    # Download image
                    response = requests.get(image_url, timeout=10)
                    if response.status_code == 200:
                        # Create filename
                        filename = f"{pet.species}_{pet.name.lower().replace(' ', '_')}_{pet.id}.jpg"
                        
                        # Save image to pet
                        pet.image.save(
                            filename,
                            ContentFile(response.content),
                            save=True
                        )
                        
                        updated_count += 1
                        self.stdout.write(f'Added placeholder image for {pet.name} ({pet.species})')
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'Failed to download image for {pet.name}: HTTP {response.status_code}')
                        )
                
                except requests.RequestException as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error downloading image for {pet.name}: {e}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error updating {pet.name}: {e}')
                    )
            else:
                self.stdout.write(f'No placeholder available for {pet.name} ({pet.species})')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully added placeholder images for {updated_count} pets')
        )