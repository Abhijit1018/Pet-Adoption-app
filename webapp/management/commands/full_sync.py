"""
Comprehensive database synchronization management command
Handles foreign key dependencies properly
"""

from django.core.management.base import BaseCommand
from django.db import connections, transaction
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Complete database synchronization with dependency handling'

    def add_arguments(self, parser):
        parser.add_argument(
            '--source', 
            type=str,
            choices=['sqlite', 'mysql'],
            required=True,
            help='Source database to copy from'
        )
        parser.add_argument(
            '--target',
            type=str, 
            choices=['sqlite', 'mysql'],
            required=True,
            help='Target database to copy to'
        )

    def handle(self, *args, **options):
        source = options['source']
        target = options['target']
        
        if source == target:
            self.stdout.write(self.style.ERROR("Source and target databases cannot be the same"))
            return
        
        self.stdout.write("=== Complete Database Synchronization ===")
        self.stdout.write(f"Synchronizing from {source.upper()} to {target.upper()}")
        
        source_db = f"{source}_db"
        target_db = f"{target}_db"
        
        try:
            # Test connections
            connections[source_db].ensure_connection()
            connections[target_db].ensure_connection()
            
            # Run migrations on target
            self.stdout.write("Running migrations on target database...")
            call_command('migrate', database=target_db, verbosity=0)
            
            # Synchronize in dependency order
            with transaction.atomic(using=target_db):
                self.sync_auth_models(source_db, target_db)
                self.sync_webapp_models(source_db, target_db)
                
            self.stdout.write(self.style.SUCCESS("✓ Synchronization completed successfully!"))
            
            # Verify synchronization
            self.verify_sync(source_db, target_db)
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Synchronization failed: {str(e)}"))
    
    def sync_auth_models(self, source_db, target_db):
        """Synchronize Django auth models first (dependencies)"""
        self.stdout.write("Synchronizing authentication data...")
        
        # Sync ContentTypes first
        content_types = ContentType.objects.using(source_db).all()
        ContentType.objects.using(target_db).all().delete()
        for ct in content_types:
            ct.pk = None
            ct.save(using=target_db)
        self.stdout.write(f"Synced {len(content_types)} content types")
        
        # Sync Permissions
        permissions = Permission.objects.using(source_db).all()
        Permission.objects.using(target_db).all().delete()
        for perm in permissions:
            perm.pk = None
            perm.save(using=target_db)
        self.stdout.write(f"Synced {len(permissions)} permissions")
        
        # Sync Groups
        groups = Group.objects.using(source_db).all()
        Group.objects.using(target_db).all().delete()
        for group in groups:
            old_pk = group.pk
            group.pk = None
            group.save(using=target_db)
            # Handle many-to-many relationships
            original_group = Group.objects.using(source_db).get(pk=old_pk)
            group.permissions.set(original_group.permissions.all())
        self.stdout.write(f"Synced {len(groups)} groups")
        
        # Sync Users
        users = User.objects.using(source_db).all()
        User.objects.using(target_db).all().delete()
        for user in users:
            old_pk = user.pk
            user.pk = None
            user.save(using=target_db)
            # Handle many-to-many relationships
            original_user = User.objects.using(source_db).get(pk=old_pk)
            user.groups.set(original_user.groups.all())
            user.user_permissions.set(original_user.user_permissions.all())
        self.stdout.write(f"Synced {len(users)} users")
    
    def sync_webapp_models(self, source_db, target_db):
        """Synchronize webapp models in dependency order"""
        self.stdout.write("Synchronizing webapp data...")
        
        from webapp.models import UserProfile, AdminProfile, Pet, AdoptionRequest
        
        # Sync UserProfile (depends on User)
        user_profiles = UserProfile.objects.using(source_db).all()
        UserProfile.objects.using(target_db).all().delete()
        for profile in user_profiles:
            profile.pk = None
            profile.save(using=target_db)
        self.stdout.write(f"Synced {len(user_profiles)} user profiles")
        
        # Sync AdminProfile (depends on User)
        admin_profiles = AdminProfile.objects.using(source_db).all()
        AdminProfile.objects.using(target_db).all().delete()
        for profile in admin_profiles:
            profile.pk = None
            profile.save(using=target_db)
        self.stdout.write(f"Synced {len(admin_profiles)} admin profiles")
        
        # Sync Pet (depends on User)
        pets = Pet.objects.using(source_db).all()
        Pet.objects.using(target_db).all().delete()
        for pet in pets:
            pet.pk = None
            pet.save(using=target_db)
        self.stdout.write(f"Synced {len(pets)} pets")
        
        # Sync AdoptionRequest (depends on User and Pet)
        adoption_requests = AdoptionRequest.objects.using(source_db).all()
        AdoptionRequest.objects.using(target_db).all().delete()
        for request in adoption_requests:
            request.pk = None
            request.save(using=target_db)
        self.stdout.write(f"Synced {len(adoption_requests)} adoption requests")
    
    def verify_sync(self, source_db, target_db):
        """Verify that synchronization was successful"""
        self.stdout.write("\n=== Verification ===")
        
        models_to_check = [
            ('Users', User),
            ('User Profiles', 'webapp.UserProfile'),
            ('Admin Profiles', 'webapp.AdminProfile'), 
            ('Pets', 'webapp.Pet'),
            ('Adoption Requests', 'webapp.AdoptionRequest'),
        ]
        
        all_synced = True
        
        for name, model_class in models_to_check:
            if isinstance(model_class, str):
                app_label, model_name = model_class.split('.')
                model_class = apps.get_model(app_label, model_name)
            
            source_count = model_class.objects.using(source_db).count()
            target_count = model_class.objects.using(target_db).count()
            
            if source_count == target_count:
                self.stdout.write(self.style.SUCCESS(f"✓ {name}: {source_count} records"))
            else:
                self.stdout.write(self.style.ERROR(f"✗ {name}: {source_count} → {target_count} (mismatch!)"))
                all_synced = False
        
        if all_synced:
            self.stdout.write(self.style.SUCCESS("\n🎉 All data synchronized successfully!"))
        else:
            self.stdout.write(self.style.ERROR("\n⚠️  Some data may not have synchronized correctly."))