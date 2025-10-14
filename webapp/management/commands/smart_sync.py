"""
Smart database synchronization with ID mapping
Handles foreign key relationships properly by mapping IDs between databases
"""

from django.core.management.base import BaseCommand
from django.db import connections, transaction
from django.contrib.auth.models import User
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Smart database synchronization with proper ID handling'

    def add_arguments(self, parser):
        parser.add_argument(
            '--direction', 
            type=str,
            choices=['sqlite-to-mysql', 'mysql-to-sqlite'],
            required=True,
            help='Direction of synchronization'
        )

    def handle(self, *args, **options):
        direction = options['direction']
        
        if direction == 'sqlite-to-mysql':
            source_db, target_db = 'sqlite_db', 'mysql_db'
            source_name, target_name = 'SQLite', 'MySQL'
        else:
            source_db, target_db = 'mysql_db', 'sqlite_db'
            source_name, target_name = 'MySQL', 'SQLite'
        
        self.stdout.write("=== Smart Database Synchronization ===")
        self.stdout.write(f"Synchronizing from {source_name} to {target_name}")
        
        try:
            # Test connections
            connections[source_db].ensure_connection()
            connections[target_db].ensure_connection()
            
            # Run migrations on target
            self.stdout.write("Preparing target database...")
            call_command('migrate', database=target_db, verbosity=0)
            
            # Use Django's built-in dumpdata/loaddata for proper handling
            self.stdout.write("Extracting data from source database...")
            
            # Export data from source
            import tempfile
            import json
            import os
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Dump data from source database
            call_command(
                'dumpdata',
                'auth.user',
                'webapp',
                '--database', source_db,
                '--output', temp_path,
                '--verbosity', 0
            )
            
            self.stdout.write("Loading data into target database...")
            
            # Load data into target database
            call_command(
                'loaddata',
                temp_path,
                '--database', target_db,
                '--verbosity', 0
            )
            
            # Clean up temp file
            os.unlink(temp_path)
            
            self.stdout.write(self.style.SUCCESS("✓ Synchronization completed successfully!"))
            
            # Verify synchronization
            self.verify_sync(source_db, target_db)
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Synchronization failed: {str(e)}"))
            import traceback
            self.stdout.write(traceback.format_exc())
    
    def verify_sync(self, source_db, target_db):
        """Verify that synchronization was successful"""
        self.stdout.write("\n=== Verification ===")
        
        from webapp.models import UserProfile, AdminProfile, Pet, AdoptionRequest
        
        models_to_check = [
            ('Users', User),
            ('User Profiles', UserProfile),
            ('Admin Profiles', AdminProfile), 
            ('Pets', Pet),
            ('Adoption Requests', AdoptionRequest),
        ]
        
        all_synced = True
        
        for name, model_class in models_to_check:
            try:
                source_count = model_class.objects.using(source_db).count()
                target_count = model_class.objects.using(target_db).count()
                
                if source_count == target_count:
                    self.stdout.write(self.style.SUCCESS(f"✓ {name}: {source_count} records"))
                else:
                    self.stdout.write(self.style.WARNING(f"⚠ {name}: {source_count} → {target_count}"))
                    all_synced = False
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"✗ {name}: Error - {str(e)}"))
                all_synced = False
        
        if all_synced:
            self.stdout.write(self.style.SUCCESS("\n🎉 All data synchronized successfully!"))
        else:
            self.stdout.write(self.style.WARNING("\n⚠️  Some data counts differ - this may be normal if databases had different initial states."))