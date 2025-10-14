from django.core.management.base import BaseCommand
from webapp.models import Pet
from django.core.files.base import ContentFile
import requests
from io import BytesIO
import random

class Command(BaseCommand):
    help = 'Assign realistic images to pets based on their species and breed'

    def handle(self, *args, **options):
        # Realistic pet image URLs by species/breed
        pet_images = {
            'dog': {
                'golden retriever': [
                    'https://images.unsplash.com/photo-1552053831-71594a27632d?w=500&h=500&fit=crop',
                    'https://images.unsplash.com/photo-1551717743-49959800b1f6?w=500&h=500&fit=crop'
                ],
                'border collie': [
                    'https://images.unsplash.com/photo-1551008785-9f8e48d35d3c?w=500&h=500&fit=crop',
                    'https://images.unsplash.com/photo-1584464491033-06628f3a6b7b?w=500&h=500&fit=crop'
                ],
                'labrador mix': [
                    'https://images.unsplash.com/photo-1518717758536-85ae29035b6d?w=500&h=500&fit=crop',
                    'https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=500&h=500&fit=crop'
                ],
                'german shepherd': [
                    'https://images.unsplash.com/photo-1589941013453-ec89f33b5e95?w=500&h=500&fit=crop',
                    'https://images.unsplash.com/photo-1605568427561-40dd23c2acea?w=500&h=500&fit=crop'
                ],
                'pug': [
                    'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=500&h=500&fit=crop',
                    'https://images.unsplash.com/photo-1518717758536-85ae29035b6d?w=500&h=500&fit=crop'
                ],
                'rottweiler': [
                    'https://images.unsplash.com/photo-1605568427561-40dd23c2acea?w=500&h=500&fit=crop',
                    'https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=500&h=500&fit=crop'
                ],
                'beagle': [
                    'https://images.unsplash.com/photo-1544717297-fa95b6ee9643?w=500&h=500&fit=crop',
                    'https://images.unsplash.com/photo-1518717758536-85ae29035b6d?w=500&h=500&fit=crop'
                ],
                'mixed breed': [
                    'https://images.unsplash.com/photo-1518717758536-85ae29035b6d?w=500&h=500&fit=crop',
                    'https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=500&h=500&fit=crop',
                    'https://images.unsplash.com/photo-1544717297-fa95b6ee9643?w=500&h=500&fit=crop'
                ]
            },
            'cat': {
                'persian': [
                    'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=500&h=500&fit=crop',
                    'https://images.unsplash.com/photo-1571566882372-1598d88abd90?w=500&h=500&fit=crop'
                ],
                'domestic shorthair': [
                    'https://images.unsplash.com/photo-1574144611937-0df059b5ef3e?w=500&h=500&fit=crop',
                    'https://images.unsplash.com/photo-1533743983669-94fa5c4338ec?w=500&h=500&fit=crop'
                ],
                'maine coon': [
                    'https://images.unsplash.com/photo-1595433707802-6b2626ef1c91?w=500&h=500&fit=crop',
                    'https://images.unsplash.com/photo-1571566882372-1598d88abd90?w=500&h=500&fit=crop'
                ],
                'siamese': [
                    'https://images.unsplash.com/photo-1513360371669-4adf3dd7dff8?w=500&h=500&fit=crop',
                    'https://images.unsplash.com/photo-1574144611937-0df059b5ef3e?w=500&h=500&fit=crop'
                ],
                'tuxedo cat': [
                    'https://images.unsplash.com/photo-1533743983669-94fa5c4338ec?w=500&h=500&fit=crop',
                    'https://images.unsplash.com/photo-1574144611937-0df059b5ef3e?w=500&h=500&fit=crop'
                ],
                'ragdoll': [
                    'https://images.unsplash.com/photo-1571566882372-1598d88abd90?w=500&h=500&fit=crop',
                    'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=500&h=500&fit=crop'
                ]
            },
            'bird': {
                'cockatiel': [
                    'https://images.unsplash.com/photo-1517594422361-5beb821c2d06?w=500&h=500&fit=crop',
                    'https://images.unsplash.com/photo-1583849963827-9b85e8c0c0c5?w=500&h=500&fit=crop'
                ],
                'lovebird': [
                    'https://images.unsplash.com/photo-1444464666168-49d633b86797?w=500&h=500&fit=crop',
                    'https://images.unsplash.com/photo-1517594422361-5beb821c2d06?w=500&h=500&fit=crop'
                ]
            },
            'rabbit': {
                'holland lop': [
                    'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=500&h=500&fit=crop',
                    'https://images.unsplash.com/photo-1589952283406-b53be7093c79?w=500&h=500&fit=crop'
                ],
                'mini rex': [
                    'https://images.unsplash.com/photo-1589952283406-b53be7093c79?w=500&h=500&fit=crop',
                    'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=500&h=500&fit=crop'
                ]
            }
        }
        
        # Default fallback images for each species
        default_images = {
            'dog': 'https://images.unsplash.com/photo-1518717758536-85ae29035b6d?w=500&h=500&fit=crop',
            'cat': 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=500&h=500&fit=crop',
            'bird': 'https://images.unsplash.com/photo-1517594422361-5beb821c2d06?w=500&h=500&fit=crop',
            'rabbit': 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=500&h=500&fit=crop'
        }
        
        updated_count = 0
        
        for pet in Pet.objects.all():
            # Skip if pet already has a non-screenshot image
            if pet.image and not ('Screenshot' in pet.image.name or not pet.image.name):
                continue
            
            # Get appropriate image URL
            breed_key = pet.breed.lower() if pet.breed else None
            species_key = pet.species.lower()
            
            image_url = None
            
            # Try to find breed-specific image
            if species_key in pet_images and breed_key in pet_images[species_key]:
                image_urls = pet_images[species_key][breed_key]
                image_url = random.choice(image_urls)
            # Fall back to species default
            elif species_key in default_images:
                image_url = default_images[species_key]
            
            if image_url:
                try:
                    # Download image
                    response = requests.get(image_url, timeout=10)
                    if response.status_code == 200:
                        # Create filename
                        filename = f"{pet.species}_{pet.name.lower().replace(' ', '_')}.jpg"
                        
                        # Save image to pet
                        pet.image.save(
                            filename,
                            ContentFile(response.content),
                            save=True
                        )
                        
                        updated_count += 1
                        self.stdout.write(f'Updated image for {pet.name} ({pet.species}/{pet.breed})')
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
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated images for {updated_count} pets')
        )