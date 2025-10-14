from django.core.management.base import BaseCommand
from webapp.models import Pet
from PIL import Image, ImageDraw, ImageFont
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Create simple placeholder images for pets without photos'

    def handle(self, *args, **options):
        # Colors for different species
        colors = {
            'dog': '#D2691E',      # SaddleBrown
            'cat': '#708090',      # SlateGray  
            'bird': '#4169E1',     # RoyalBlue
            'rabbit': '#F5DEB3'    # Wheat
        }
        
        # Create media/pet_images directory if it doesn't exist
        media_dir = os.path.join(settings.MEDIA_ROOT, 'pet_images')
        os.makedirs(media_dir, exist_ok=True)
        
        created_count = 0
        
        # Get pets without images
        pets_without_images = Pet.objects.filter(image__isnull=True) | Pet.objects.filter(image='')
        
        for pet in pets_without_images:
            try:
                # Create a 400x400 placeholder image
                img = Image.new('RGB', (400, 400), colors.get(pet.species, '#808080'))
                draw = ImageDraw.Draw(img)
                
                # Add pet name and species text
                try:
                    # Try to use a basic font
                    font = ImageFont.truetype("arial.ttf", 24)
                except:
                    # Fall back to default font
                    font = ImageFont.load_default()
                
                # Add text
                text_lines = [
                    pet.name,
                    f"({pet.species.title()})",
                    pet.breed or "Mixed Breed"
                ]
                
                y_offset = 150
                for line in text_lines:
                    # Get text size
                    bbox = draw.textbbox((0, 0), line, font=font)
                    text_width = bbox[2] - bbox[0]
                    
                    # Center the text
                    x = (400 - text_width) // 2
                    draw.text((x, y_offset), line, fill='white', font=font)
                    y_offset += 40
                
                # Save image
                filename = f"{pet.species}_{pet.name.lower().replace(' ', '_')}_{pet.id}.png"
                filepath = os.path.join(media_dir, filename)
                img.save(filepath)
                
                # Update pet with image path
                pet.image = f'pet_images/{filename}'
                pet.save()
                
                created_count += 1
                self.stdout.write(f'Created placeholder for {pet.name} ({pet.species})')
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating image for {pet.name}: {e}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} placeholder images')
        )