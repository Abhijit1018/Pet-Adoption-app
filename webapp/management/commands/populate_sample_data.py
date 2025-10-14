from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from webapp.models import Pet, UserProfile, AdoptionRequest
from django.utils import timezone
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populate the database with sample users and pets'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample users and pets...'))
        
        # Sample user data with realistic information
        sample_users = [
            {
                'username': 'sarah_johnson',
                'email': 'sarah.johnson@gmail.com',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'profile': {
                    'age': 28,
                    'gender': 'F',
                    'phone_number': '+1-555-0123',
                    'location': 'Seattle, WA'
                }
            },
            {
                'username': 'mike_chen',
                'email': 'mike.chen@yahoo.com',
                'first_name': 'Michael',
                'last_name': 'Chen',
                'profile': {
                    'age': 35,
                    'gender': 'M',
                    'phone_number': '+1-555-0456',
                    'location': 'Portland, OR'
                }
            },
            {
                'username': 'emma_williams',
                'email': 'emma.williams@hotmail.com',
                'first_name': 'Emma',
                'last_name': 'Williams',
                'profile': {
                    'age': 24,
                    'gender': 'F',
                    'phone_number': '+1-555-0789',
                    'location': 'San Francisco, CA'
                }
            },
            {
                'username': 'david_martinez',
                'email': 'david.martinez@outlook.com',
                'first_name': 'David',
                'last_name': 'Martinez',
                'profile': {
                    'age': 42,
                    'gender': 'M',
                    'phone_number': '+1-555-0321',
                    'location': 'Los Angeles, CA'
                }
            },
            {
                'username': 'lisa_thompson',
                'email': 'lisa.thompson@gmail.com',
                'first_name': 'Lisa',
                'last_name': 'Thompson',
                'profile': {
                    'age': 31,
                    'gender': 'F',
                    'phone_number': '+1-555-0654',
                    'location': 'Denver, CO'
                }
            },
            {
                'username': 'james_brown',
                'email': 'james.brown@icloud.com',
                'first_name': 'James',
                'last_name': 'Brown',
                'profile': {
                    'age': 29,
                    'gender': 'M',
                    'phone_number': '+1-555-0987',
                    'location': 'Austin, TX'
                }
            },
            {
                'username': 'sophia_davis',
                'email': 'sophia.davis@gmail.com',
                'first_name': 'Sophia',
                'last_name': 'Davis',
                'profile': {
                    'age': 26,
                    'gender': 'F',
                    'phone_number': '+1-555-0147',
                    'location': 'Chicago, IL'
                }
            },
            {
                'username': 'ryan_wilson',
                'email': 'ryan.wilson@yahoo.com',
                'first_name': 'Ryan',
                'last_name': 'Wilson',
                'profile': {
                    'age': 33,
                    'gender': 'M',
                    'phone_number': '+1-555-0258',
                    'location': 'Miami, FL'
                }
            }
        ]

        # Sample pet data organized by category with realistic descriptions
        sample_pets = {
            'Dog': [
                {
                    'name': 'Buddy',
                    'breed': 'Golden Retriever',
                    'age': 3,
                    'description': 'Buddy is a friendly and energetic Golden Retriever who loves playing fetch and swimming. He\'s great with kids and other dogs. House trained and knows basic commands.',
                    'status': 'available',
                    'contact_email': 'sarah.johnson@gmail.com',
                    'contact_phone': '+1-555-0123'
                },
                {
                    'name': 'Luna',
                    'breed': 'Border Collie',
                    'age': 2,
                    'description': 'Luna is an intelligent and active Border Collie. She loves mental challenges and outdoor activities. Perfect for an active family who enjoys hiking and training.',
                    'status': 'available',
                    'contact_email': 'mike.chen@yahoo.com',
                    'contact_phone': '+1-555-0456'
                },
                {
                    'name': 'Charlie',
                    'breed': 'Labrador Mix',
                    'age': 5,
                    'description': 'Charlie is a calm and gentle Labrador mix. He\'s excellent with children and seniors. Loves long walks and belly rubs. Fully vaccinated and neutered.',
                    'status': 'adopted',
                    'contact_email': 'emma.williams@hotmail.com',
                    'contact_phone': '+1-555-0789'
                },
                {
                    'name': 'Max',
                    'breed': 'German Shepherd',
                    'age': 4,
                    'description': 'Max is a loyal and protective German Shepherd. Well-trained guard dog who is also gentle with family. Needs an experienced owner with a large yard.',
                    'status': 'available',
                    'contact_email': 'david.martinez@outlook.com',
                    'contact_phone': '+1-555-0321'
                },
                {
                    'name': 'Bella',
                    'breed': 'Pug',
                    'age': 1,
                    'description': 'Bella is an adorable young Pug with a playful personality. She\'s small, affectionate, and perfect for apartment living. Loves attention and treats.',
                    'status': 'available',
                    'contact_email': 'lisa.thompson@gmail.com',
                    'contact_phone': '+1-555-0654'
                },
                {
                    'name': 'Rocky',
                    'breed': 'Rottweiler',
                    'age': 6,
                    'description': 'Rocky is a mature Rottweiler with a calm temperament. He\'s well-socialized and great with older children. Looking for a quiet home to enjoy his golden years.',
                    'status': 'available',
                    'contact_email': 'james.brown@icloud.com',
                    'contact_phone': '+1-555-0987'
                }
            ],
            'Cat': [
                {
                    'name': 'Whiskers',
                    'breed': 'Persian',
                    'age': 2,
                    'description': 'Whiskers is a beautiful Persian cat with long, fluffy fur. She\'s calm and loves being pampered. Perfect lap cat who enjoys quiet environments.',
                    'status': 'available',
                    'contact_email': 'sophia.davis@gmail.com',
                    'contact_phone': '+1-555-0147'
                },
                {
                    'name': 'Shadow',
                    'breed': 'Domestic Shorthair',
                    'age': 4,
                    'description': 'Shadow is a mysterious black cat who\'s very affectionate once he gets to know you. Independent but loving, and great at keeping mice away.',
                    'status': 'available',
                    'contact_email': 'ryan.wilson@yahoo.com',
                    'contact_phone': '+1-555-0258'
                },
                {
                    'name': 'Mittens',
                    'breed': 'Maine Coon',
                    'age': 3,
                    'description': 'Mittens is a large, gentle Maine Coon with distinctive white paws. He\'s very social and loves playing with feather toys. Great with other cats.',
                    'status': 'adopted',
                    'contact_email': 'sarah.johnson@gmail.com',
                    'contact_phone': '+1-555-0123'
                },
                {
                    'name': 'Cleo',
                    'breed': 'Siamese',
                    'age': 1,
                    'description': 'Cleo is a talkative Siamese kitten who loves attention. She\'s very intelligent and playful. Would do well as an only cat or with another young cat.',
                    'status': 'available',
                    'contact_email': 'mike.chen@yahoo.com',
                    'contact_phone': '+1-555-0456'
                },
                {
                    'name': 'Oreo',
                    'breed': 'Tuxedo Cat',
                    'age': 5,
                    'description': 'Oreo is a handsome tuxedo cat with perfect black and white markings. He\'s laid-back and enjoys sunny windowsills. Good with children and dogs.',
                    'status': 'available',
                    'contact_email': 'emma.williams@hotmail.com',
                    'contact_phone': '+1-555-0789'
                }
            ],
            'Bird': [
                {
                    'name': 'Sunny',
                    'breed': 'Cockatiel',
                    'age': 2,
                    'description': 'Sunny is a cheerful cockatiel who loves to whistle and learn new songs. He\'s very social and enjoys being around people. Comes with a large cage.',
                    'status': 'available',
                    'contact_email': 'david.martinez@outlook.com',
                    'contact_phone': '+1-555-0321'
                },
                {
                    'name': 'Kiwi',
                    'breed': 'Lovebird',
                    'age': 1,
                    'description': 'Kiwi is a vibrant green lovebird who is hand-tamed and very affectionate. She loves head scratches and sitting on shoulders. Perfect for bird enthusiasts.',
                    'status': 'available',
                    'contact_email': 'lisa.thompson@gmail.com',
                    'contact_phone': '+1-555-0654'
                }
            ],
            'Rabbit': [
                {
                    'name': 'Snowball',
                    'breed': 'Holland Lop',
                    'age': 2,
                    'description': 'Snowball is a fluffy white Holland Lop rabbit who loves fresh vegetables and hopping around the yard. She\'s litter trained and very gentle.',
                    'status': 'available',
                    'contact_email': 'james.brown@icloud.com',
                    'contact_phone': '+1-555-0987'
                },
                {
                    'name': 'Cocoa',
                    'breed': 'Mini Rex',
                    'age': 1,
                    'description': 'Cocoa is a chocolate-colored Mini Rex rabbit with incredibly soft fur. He\'s curious and playful, and enjoys exploring new environments safely.',
                    'status': 'available',
                    'contact_email': 'sophia.davis@gmail.com',
                    'contact_phone': '+1-555-0147'
                }
            ]
        }

        # Lost pets data
        lost_pets = [
            {
                'name': 'Milo',
                'category': 'Dog',
                'breed': 'Beagle',
                'age': 3,
                'description': 'Lost near Central Park on September 20th. Milo is a friendly Beagle wearing a red collar with tags. He responds to his name and loves treats.',
                'status': 'lost',
                'contact_email': 'ryan.wilson@yahoo.com',
                'contact_phone': '+1-555-0258'
            },
            {
                'name': 'Princess',
                'category': 'Cat',
                'breed': 'Ragdoll',
                'age': 4,
                'description': 'Missing since September 22nd from Oak Street area. Princess is a blue-eyed Ragdoll cat, very fluffy with cream and brown markings. She\'s microchipped.',
                'status': 'lost',
                'contact_email': 'sarah.johnson@gmail.com',
                'contact_phone': '+1-555-0123'
            }
        ]

        # Found pets data
        found_pets = [
            {
                'name': 'Unknown',
                'category': 'Dog',
                'breed': 'Mixed Breed',
                'age': 2,
                'description': 'Found this friendly mixed breed dog near the river on September 25th. No collar or tags. Very well-behaved and seems house trained. Looking for owner.',
                'status': 'found',
                'contact_email': 'mike.chen@yahoo.com',
                'contact_phone': '+1-555-0456'
            }
        ]

        created_users = []
        
        # Create users and their profiles
        for user_data in sample_users:
            # Check if user already exists
            if User.objects.filter(username=user_data['username']).exists():
                self.stdout.write(f'User {user_data["username"]} already exists, skipping...')
                user = User.objects.get(username=user_data['username'])
            else:
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password='petlover123',  # Default password
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name']
                )
                
                # Set join date to a random date in the past 6 months
                days_ago = random.randint(1, 180)
                user.date_joined = timezone.now() - timedelta(days=days_ago)
                
                # Set last login to a random recent date
                if random.choice([True, False, True]):  # 2/3 chance of having logged in
                    user.last_login = timezone.now() - timedelta(days=random.randint(1, 30))
                
                user.save()
                
                # Create user profile
                profile, created = UserProfile.objects.get_or_create(
                    user=user,
                    defaults=user_data['profile']
                )
                
                self.stdout.write(f'Created user: {user_data["username"]}')
            
            created_users.append(user)

        # Create pets for each category
        pet_count = 0
        for category, pets_in_category in sample_pets.items():
            for pet_data in pets_in_category:
                # Find the owner by email
                owner = None
                for user in created_users:
                    if user.email == pet_data['contact_email']:
                        owner = user
                        break
                
                if owner:
                    # Check if pet already exists
                    if not Pet.objects.filter(name=pet_data['name'], owner=owner).exists():
                        # Create random date in the past 3 months
                        days_ago = random.randint(1, 90)
                        created_date = timezone.now() - timedelta(days=days_ago)
                        
                        # Convert status to match model choices
                        status_mapping = {
                            'available': 'for_adoption',
                            'adopted': 'adopted'
                        }
                        mapped_status = status_mapping.get(pet_data['status'], pet_data['status'])
                        
                        pet = Pet.objects.create(
                            name=pet_data['name'],
                            species=category.lower(),
                            breed=pet_data['breed'],
                            age=str(pet_data['age']) + ' years',
                            description=pet_data['description'],
                            status=mapped_status,
                            location=owner.userprofile.location or 'Location not specified',
                            contact_email=pet_data['contact_email'],
                            contact_phone=pet_data['contact_phone'],
                            owner=owner
                        )
                        # Manually set the date_added field
                        pet.date_added = created_date
                        pet.save()
                        
                        pet_count += 1
                        self.stdout.write(f'Created {category}: {pet_data["name"]} (Owner: {owner.username})')

        # Create lost pets
        for pet_data in lost_pets:
            owner = None
            for user in created_users:
                if user.email == pet_data['contact_email']:
                    owner = user
                    break
            
            if owner:
                if not Pet.objects.filter(name=pet_data['name'], owner=owner, status='lost').exists():
                    days_ago = random.randint(1, 10)  # Lost recently
                    created_date = timezone.now() - timedelta(days=days_ago)
                    
                    pet = Pet.objects.create(
                        name=pet_data['name'],
                        species=pet_data['category'].lower(),
                        breed=pet_data['breed'],
                        age=str(pet_data['age']) + ' years',
                        description=pet_data['description'],
                        status=pet_data['status'],
                        location=owner.userprofile.location or 'Location not specified',
                        contact_email=pet_data['contact_email'],
                        contact_phone=pet_data['contact_phone'],
                        owner=owner
                    )
                    pet.date_added = created_date
                    pet.save()
                    
                    pet_count += 1
                    self.stdout.write(f'Created LOST pet: {pet_data["name"]} (Owner: {owner.username})')

        # Create found pets
        for pet_data in found_pets:
            owner = None
            for user in created_users:
                if user.email == pet_data['contact_email']:
                    owner = user
                    break
            
            if owner:
                if not Pet.objects.filter(name=pet_data['name'], owner=owner, status='found').exists():
                    days_ago = random.randint(1, 5)  # Found very recently
                    created_date = timezone.now() - timedelta(days=days_ago)
                    
                    pet = Pet.objects.create(
                        name=pet_data['name'],
                        species=pet_data['category'].lower(),
                        breed=pet_data['breed'],
                        age=str(pet_data['age']) + ' years',
                        description=pet_data['description'],
                        status=pet_data['status'],
                        location=owner.userprofile.location or 'Location not specified',
                        contact_email=pet_data['contact_email'],
                        contact_phone=pet_data['contact_phone'],
                        owner=owner,
                        found_date=created_date
                    )
                    pet.date_added = created_date
                    pet.save()
                    
                    pet_count += 1
                    self.stdout.write(f'Created FOUND pet: {pet_data["name"]} (Finder: {owner.username})')

        # Create some adoption requests
        available_pets = Pet.objects.filter(status='for_adoption')
        adopters = created_users[:4]  # First 4 users as potential adopters
        
        adoption_count = 0
        for pet in available_pets[:6]:  # Create requests for first 6 available pets
            if adopters:
                adopter = random.choice(adopters)
                # Make sure adopter is not the owner
                if adopter != pet.owner:
                    if not AdoptionRequest.objects.filter(user=adopter, pet=pet).exists():
                        days_ago = random.randint(1, 14)
                        request_date = timezone.now() - timedelta(days=days_ago)
                        
                        adoption_request = AdoptionRequest.objects.create(
                            user=adopter,
                            pet=pet,
                            message=f"Hi! I'm very interested in adopting {pet.name}. I have experience with {pet.species}s and can provide a loving home. Please let me know if {pet.name} is still available."
                        )
                        # Update the created_at field to simulate older requests
                        adoption_request.created_at = request_date
                        adoption_request.save()
                        adoption_count += 1
                        self.stdout.write(f'Created adoption request: {adopter.username} wants {pet.name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\nDatabase populated successfully!\n'
                f'- Created {len(created_users)} users\n'
                f'- Created {pet_count} pets\n'
                f'- Created {adoption_count} adoption requests\n'
                f'\nAll users have password: petlover123'
            )
        )