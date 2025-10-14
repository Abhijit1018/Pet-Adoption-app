"""
Enhanced Pet Image Manager
Downloads and assigns diverse, high-quality images to pets based on their species
"""

from django.core.management.base import BaseCommand
from webapp.models import Pet
from PIL import Image, ImageDraw, ImageFont
import os
import requests
import random
from io import BytesIO
import time

class Command(BaseCommand):
    help = 'Update pet images with high-quality, diverse animal photos'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', help='Replace existing images')
        parser.add_argument('--download', action='store_true', help='Download from internet (requires connection)')

    def handle(self, *args, **options):
        self.stdout.write("=== Pet Image Update System ===")
        
        force_update = options.get('force', False)
        download_mode = options.get('download', False)
        
        # Create media directory if it doesn't exist
        media_dir = 'media/pet_images'
        os.makedirs(media_dir, exist_ok=True)
        
        # Get all pets
        pets = Pet.objects.all()
        self.stdout.write(f"Found {pets.count()} pets to process")
        
        if download_mode:
            self.download_diverse_images()
        else:
            self.generate_diverse_images()
        
        # Assign images to pets
        self.assign_images_to_pets(pets, force_update)
        
        # Clean up duplicate/unused images
        self.cleanup_unused_images()
        
        self.stdout.write(self.style.SUCCESS("✅ Pet image update completed!"))

    def generate_diverse_images(self):
        """Generate diverse, attractive placeholder images for different animal types"""
        self.stdout.write("Generating diverse animal images...")
        
        # Animal types with color schemes and characteristics
        animal_templates = {
            'dog': {
                'colors': ['#8B4513', '#DEB887', '#000000', '#FFFFFF', '#D2691E', '#F4A460'],
                'breeds': ['Golden Retriever', 'German Shepherd', 'Bulldog', 'Labrador', 'Husky', 'Poodle', 'Beagle', 'Border Collie']
            },
            'cat': {
                'colors': ['#696969', '#FFB6C1', '#F5DEB3', '#000000', '#FFFFFF', '#DDA0DD'],
                'breeds': ['Persian', 'Siamese', 'Maine Coon', 'British Shorthair', 'Bengal', 'Ragdoll', 'Tabby', 'Russian Blue']
            },
            'bird': {
                'colors': ['#FF6347', '#32CD32', '#FFD700', '#4169E1', '#FF1493', '#00CED1'],
                'breeds': ['Parrot', 'Canary', 'Cockatiel', 'Budgie', 'Lovebird', 'Finch', 'Macaw', 'Cockatoo']
            },
            'rabbit': {
                'colors': ['#F5F5DC', '#D2B48C', '#696969', '#FFFFFF', '#CD853F'],
                'breeds': ['Holland Lop', 'Netherland Dwarf', 'Flemish Giant', 'Angora', 'Rex']
            },
            'horse': {
                'colors': ['#8B4513', '#000000', '#FFFFFF', '#DEB887', '#A0522D'],
                'breeds': ['Arabian', 'Thoroughbred', 'Quarter Horse', 'Clydesdale', 'Mustang']
            },
            'other': {
                'colors': ['#FFB6C1', '#98FB98', '#87CEEB', '#DDA0DD', '#F0E68C'],
                'breeds': ['Hamster', 'Guinea Pig', 'Ferret', 'Turtle', 'Fish']
            }
        }
        
        generated = 0
        
        for animal_type, config in animal_templates.items():
            for i, breed in enumerate(config['breeds']):
                try:
                    # Create image with gradient background
                    img = Image.new('RGB', (500, 400), color='white')
                    draw = ImageDraw.Draw(img)
                    
                    # Create gradient background
                    color1 = config['colors'][i % len(config['colors'])]
                    color2 = config['colors'][(i + 1) % len(config['colors'])]
                    
                    for y in range(400):
                        ratio = y / 400
                        r1, g1, b1 = tuple(int(color1[j:j+2], 16) for j in (1, 3, 5))
                        r2, g2, b2 = tuple(int(color2[j:j+2], 16) for j in (1, 3, 5))
                        
                        r = int(r1 * (1 - ratio) + r2 * ratio)
                        g = int(g1 * (1 - ratio) + g2 * ratio)
                        b = int(b1 * (1 - ratio) + b2 * ratio)
                        
                        draw.line([(0, y), (500, y)], fill=(r, g, b))
                    
                    # Add decorative elements
                    self.add_animal_silhouette(draw, animal_type, 500, 400)
                    
                    # Add text
                    try:
                        font = ImageFont.truetype("arial.ttf", 36)
                    except:
                        font = ImageFont.load_default()
                    
                    # Add breed name with shadow effect
                    text = breed
                    bbox = draw.textbbox((0, 0), text, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    
                    x = (500 - text_width) // 2
                    y = 320
                    
                    # Shadow
                    draw.text((x+2, y+2), text, font=font, fill='black')
                    # Main text
                    draw.text((x, y), text, font=font, fill='white')
                    
                    # Add cute decorative elements
                    self.add_decorative_elements(draw, animal_type)
                    
                    # Save image
                    filename = f"{animal_type}_{breed.lower().replace(' ', '_')}_{i+1}.jpg"
                    filepath = os.path.join('media/pet_images', filename)
                    img.save(filepath, 'JPEG', quality=85)
                    
                    generated += 1
                    self.stdout.write(f"Generated: {filename}")
                    
                except Exception as e:
                    self.stdout.write(f"Failed to generate {animal_type}_{breed}: {str(e)}")
                    continue
        
        self.stdout.write(f"Generated {generated} diverse images")

    def add_animal_silhouette(self, draw, animal_type, width, height):
        """Add simple animal silhouette shapes"""
        center_x, center_y = width // 2, height // 2 - 50
        
        if animal_type == 'dog':
            # Simple dog silhouette
            draw.ellipse([center_x-60, center_y-40, center_x+60, center_y+40], fill=(255,255,255,100))
            draw.ellipse([center_x-20, center_y-60, center_x+20, center_y-20], fill=(255,255,255,80))
        elif animal_type == 'cat':
            # Cat silhouette with pointed ears
            draw.ellipse([center_x-50, center_y-30, center_x+50, center_y+50], fill=(255,255,255,100))
            draw.polygon([(center_x-30, center_y-30), (center_x-40, center_y-60), (center_x-10, center_y-40)], fill=(255,255,255,80))
            draw.polygon([(center_x+30, center_y-30), (center_x+40, center_y-60), (center_x+10, center_y-40)], fill=(255,255,255,80))
        elif animal_type == 'bird':
            # Bird silhouette
            draw.ellipse([center_x-40, center_y-20, center_x+40, center_y+40], fill=(255,255,255,100))
            draw.polygon([(center_x-40, center_y), (center_x-80, center_y-10), (center_x-60, center_y+20)], fill=(255,255,255,80))

    def add_decorative_elements(self, draw, animal_type):
        """Add decorative elements based on animal type"""
        if animal_type == 'dog':
            # Add paw prints
            for i in range(3):
                x = 50 + i * 150
                y = 50 + i * 20
                draw.ellipse([x, y, x+20, y+25], fill=(255,255,255,150))
        elif animal_type == 'cat':
            # Add small hearts
            for i in range(4):
                x = 80 + i * 100
                y = 60 + (i % 2) * 30
                draw.ellipse([x, y, x+15, y+15], fill=(255,192,203,150))

    def assign_images_to_pets(self, pets, force_update):
        """Assign appropriate images to pets based on their species and breed"""
        self.stdout.write("\nAssigning images to pets...")
        
        # Get list of available images
        image_files = [f for f in os.listdir('media/pet_images') if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        # Categorize images by animal type
        categorized_images = {
            'dog': [f for f in image_files if f.startswith('dog_')],
            'cat': [f for f in image_files if f.startswith('cat_')],
            'bird': [f for f in image_files if f.startswith('bird_')],
            'rabbit': [f for f in image_files if f.startswith('rabbit_')],
            'horse': [f for f in image_files if f.startswith('horse_')],
            'other': [f for f in image_files if f.startswith('other_')]
        }
        
        # Add any existing good images to appropriate categories
        existing_good = ['Bird_animal_travel_nature_bird.jpeg', 'lop_eared_rabbits___Lop_eared_rabbit_Oryctolagus.jpeg']
        for img in existing_good:
            if os.path.exists(f'media/pet_images/{img}'):
                if 'bird' in img.lower():
                    categorized_images['bird'].append(img)
                elif 'rabbit' in img.lower():
                    categorized_images['rabbit'].append(img)
        
        used_images = set()
        updated_count = 0
        
        for pet in pets:
            # Skip if pet already has image and not forcing update
            if pet.image and not force_update:
                continue
            
            # Determine animal category from pet species or breed
            species = pet.species.lower() if pet.species else 'other'
            breed = pet.breed.lower() if pet.breed else ''
            
            # Map species to image categories
            if 'dog' in species or 'puppy' in species:
                category = 'dog'
            elif 'cat' in species or 'kitten' in species:
                category = 'cat'
            elif 'bird' in species or any(b in species for b in ['parrot', 'canary', 'cockatiel']):
                category = 'bird'
            elif 'rabbit' in species or 'bunny' in species:
                category = 'rabbit'
            elif 'horse' in species or 'pony' in species:
                category = 'horse'
            else:
                category = 'other'
            
            # Get available images for this category
            available_images = [img for img in categorized_images.get(category, []) if img not in used_images]
            
            # If no images in preferred category, try others
            if not available_images:
                for cat, images in categorized_images.items():
                    available_images = [img for img in images if img not in used_images]
                    if available_images:
                        break
            
            if available_images:
                # Choose image (prefer breed-specific if possible)
                chosen_image = None
                if breed:
                    # Try to find breed-specific image
                    breed_matches = [img for img in available_images if breed.replace(' ', '_') in img.lower()]
                    if breed_matches:
                        chosen_image = breed_matches[0]
                
                if not chosen_image:
                    chosen_image = available_images[0]
                
                # Assign image to pet
                pet.image = f'pet_images/{chosen_image}'
                pet.save()
                used_images.add(chosen_image)
                updated_count += 1
                
                self.stdout.write(f"✅ {pet.name} ({species}): {chosen_image}")
            else:
                self.stdout.write(f"⚠️  No available image for {pet.name} ({species})")
        
        self.stdout.write(f"Updated {updated_count} pet images")

    def cleanup_unused_images(self):
        """Remove duplicate and unused images"""
        self.stdout.write("\nCleaning up unused images...")
        
        # Get all images referenced by pets
        used_images = set()
        for pet in Pet.objects.all():
            if pet.image:
                image_name = os.path.basename(pet.image.name)
                used_images.add(image_name)
        
        # Get all image files
        image_files = set()
        for file in os.listdir('media/pet_images'):
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_files.add(file)
        
        # Find unused images
        unused_images = image_files - used_images
        
        # Remove old screenshot images and duplicates
        cleanup_patterns = ['Screenshot', 'placeholder', 'temp', 'duplicate']
        
        removed_count = 0
        for image in unused_images:
            should_remove = any(pattern in image for pattern in cleanup_patterns)
            
            # Also remove if it's a very small file (likely blank)
            if not should_remove:
                filepath = os.path.join('media/pet_images', image)
                if os.path.exists(filepath) and os.path.getsize(filepath) < 1000:
                    should_remove = True
            
            if should_remove:
                try:
                    os.remove(os.path.join('media/pet_images', image))
                    removed_count += 1
                    self.stdout.write(f"Removed: {image}")
                except Exception as e:
                    self.stdout.write(f"Failed to remove {image}: {str(e)}")
        
        self.stdout.write(f"Removed {removed_count} unused/duplicate images")