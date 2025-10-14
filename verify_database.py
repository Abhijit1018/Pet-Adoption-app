#!/usr/bin/env python3
"""
Database Verification Script for Pet Adoption App
This script verifies that all data is properly migrated and accessible.
"""

import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'home.settings')
django.setup()

from webapp.models import Pet, UserProfile, AdminProfile, AdoptionRequest
from django.contrib.auth.models import User

def main():
    print("="*60)
    print("PET ADOPTION APP - DATABASE VERIFICATION")
    print("="*60)
    
    # Check pets
    print("\n1. PETS VERIFICATION")
    print("-" * 30)
    pets = Pet.objects.all()
    print(f"Total pets: {pets.count()}")
    
    for pet in pets:
        print(f"\nPet: {pet.name}")
        print(f"  Status: {pet.status} -> {pet.get_status_display()}")
        print(f"  Species: {pet.species} -> {pet.get_species_display()}")
        print(f"  Breed: {pet.breed or 'Not specified'}")
        print(f"  Age: {pet.age or 'Not specified'}")
        print(f"  Gender: {pet.gender} -> {pet.get_gender_display()}")
        print(f"  Location: {pet.location}")
        print(f"  Owner: {pet.owner.username if pet.owner else 'No owner'}")
        print(f"  Image: {'✓' if pet.image else '✗'}")
        print(f"  Date Added: {pet.date_added}")
    
    # Check pets by status
    print(f"\nPets by status:")
    for status_code, status_label in Pet.STATUS_CHOICES:
        count = Pet.objects.filter(status=status_code).count()
        print(f"  {status_label}: {count}")
    
    # Check users
    print("\n2. USERS VERIFICATION")
    print("-" * 30)
    users = User.objects.all()
    print(f"Total users: {users.count()}")
    
    for user in users:
        print(f"\nUser: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Staff: {'✓' if user.is_staff else '✗'}")
        print(f"  Superuser: {'✓' if user.is_superuser else '✗'}")
        
        # Check profile
        try:
            profile = user.userprofile
            print(f"  Profile: ✓")
            print(f"    Age: {profile.age or 'Not set'}")
            print(f"    Phone: {profile.phone_number or 'Not set'}")
            print(f"    Gender: {profile.gender or 'Not set'}")
            print(f"    Location: {profile.location or 'Not set'}")
        except UserProfile.DoesNotExist:
            print(f"  Profile: ✗ (Missing)")
        
        # Check if admin
        try:
            admin = user.adminprofile
            print(f"  Admin: ✓ (Created: {admin.created_at})")
        except AdminProfile.DoesNotExist:
            print(f"  Admin: ✗")
    
    # Check adoption requests
    print("\n3. ADOPTION REQUESTS")
    print("-" * 30)
    requests = AdoptionRequest.objects.all()
    print(f"Total adoption requests: {requests.count()}")
    
    if requests.exists():
        for req in requests:
            print(f"  {req.user.username} -> {req.pet.name} ({req.status})")
    else:
        print("  No adoption requests yet")
    
    # Verification summary
    print("\n4. VERIFICATION SUMMARY")
    print("-" * 30)
    
    issues = []
    
    # Check for pets with invalid statuses
    invalid_status_pets = []
    valid_statuses = [choice[0] for choice in Pet.STATUS_CHOICES]
    for pet in pets:
        if pet.status not in valid_statuses:
            invalid_status_pets.append(pet)
    
    if invalid_status_pets:
        issues.append(f"Pets with invalid status: {len(invalid_status_pets)}")
    
    # Check for pets with invalid species
    invalid_species_pets = []
    valid_species = [choice[0] for choice in Pet.SPECIES_CHOICES]
    for pet in pets:
        if pet.species not in valid_species:
            invalid_species_pets.append(pet)
    
    if invalid_species_pets:
        issues.append(f"Pets with invalid species: {len(invalid_species_pets)}")
    
    # Check for users without profiles
    users_without_profiles = []
    for user in users:
        try:
            user.userprofile
        except UserProfile.DoesNotExist:
            users_without_profiles.append(user)
    
    if users_without_profiles:
        issues.append(f"Users without profiles: {len(users_without_profiles)}")
    
    # Final status
    if issues:
        print("❌ ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✅ ALL CHECKS PASSED!")
        print("\n🎉 Your Pet Adoption App database is working perfectly!")
        print("\nYou should now be able to see:")
        print(f"  - {Pet.objects.filter(status='for_adoption').count()} pets available for adoption")
        print(f"  - {Pet.objects.filter(status='lost').count()} lost pets")
        print(f"  - {Pet.objects.filter(status='found').count()} found pets")
        print(f"  - All {users.count()} users have proper profiles")
        
        print("\n🌐 Access your app at: http://127.0.0.1:8000/")
        print("📱 Admin panel at: http://127.0.0.1:8000/admin/")

if __name__ == "__main__":
    main()