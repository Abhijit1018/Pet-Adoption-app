"""
Management command to synchronize data between SQLite and MySQL databases
"""

from django.core.management.base import BaseCommand
from django.db import connections
from django.apps import apps
from django.core.management import call_command
import json
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Synchronize data between SQLite and MySQL databases'

    def add_arguments(self, parser):
        parser.add_argument(
            '--source', 
            type=str,
            choices=['sqlite', 'mysql', 'auto'],
            default='auto',
            help='Source database to copy from'
        )
        parser.add_argument(
            '--target',
            type=str, 
            choices=['sqlite', 'mysql', 'auto'],
            default='auto',
            help='Target database to copy to'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be synchronized without making changes'
        )

    def handle(self, *args, **options):
        source = options['source']
        target = options['target']
        dry_run = options['dry_run']
        
        self.stdout.write("=== Database Synchronization Tool ===")
        
        # Determine available databases
        available_dbs = self.check_database_availability()
        
        if source == 'auto':
            source = self.determine_source_database(available_dbs)
        if target == 'auto':
            target = self.determine_target_database(available_dbs, source)
            
        if not source or not target:
            self.stdout.write(self.style.ERROR("Could not determine source and target databases"))
            return
            
        self.stdout.write(f"Source Database: {source}")
        self.stdout.write(f"Target Database: {target}")
        
        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN MODE - No changes will be made"))
        
        # Get data counts
        source_counts = self.get_data_counts(f"{source}_db")
        target_counts = self.get_data_counts(f"{target}_db")
        
        self.display_data_comparison(source_counts, target_counts, source, target)
        
        if not dry_run:
            self.perform_synchronization(source, target, source_counts, target_counts)
    
    def check_database_availability(self):
        """Check which databases are available"""
        available = {}
        
        # Check SQLite
        try:
            conn = connections['sqlite_db']
            conn.ensure_connection()
            available['sqlite'] = True
            self.stdout.write(self.style.SUCCESS("✓ SQLite database available"))
        except Exception as e:
            available['sqlite'] = False
            self.stdout.write(self.style.ERROR(f"✗ SQLite database unavailable: {str(e)}"))
        
        # Check MySQL
        try:
            conn = connections['mysql_db']
            conn.ensure_connection()
            available['mysql'] = True
            self.stdout.write(self.style.SUCCESS("✓ MySQL database available"))
        except Exception as e:
            available['mysql'] = False
            self.stdout.write(self.style.ERROR(f"✗ MySQL database unavailable: {str(e)}"))
            
        return available
    
    def determine_source_database(self, available_dbs):
        """Determine which database has more data (likely the source)"""
        if not available_dbs['sqlite'] and not available_dbs['mysql']:
            return None
            
        if available_dbs['sqlite'] and not available_dbs['mysql']:
            return 'sqlite'
        elif available_dbs['mysql'] and not available_dbs['sqlite']:
            return 'mysql'
        else:
            # Both available, check which has more data
            sqlite_total = sum(self.get_data_counts('sqlite_db').values())
            mysql_total = sum(self.get_data_counts('mysql_db').values())
            
            return 'sqlite' if sqlite_total >= mysql_total else 'mysql'
    
    def determine_target_database(self, available_dbs, source):
        """Determine target database (opposite of source)"""
        if source == 'sqlite' and available_dbs['mysql']:
            return 'mysql'
        elif source == 'mysql' and available_dbs['sqlite']:
            return 'sqlite'
        return None
    
    def get_data_counts(self, db_alias):
        """Get record counts for all models"""
        counts = {}
        
        try:
            # Get all models from webapp app
            webapp_models = apps.get_app_config('webapp').get_models()
            
            for model in webapp_models:
                model_name = model._meta.model_name
                try:
                    count = model.objects.using(db_alias).count()
                    counts[model_name] = count
                except Exception as e:
                    counts[model_name] = f"Error: {str(e)}"
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error getting counts for {db_alias}: {str(e)}"))
            
        return counts
    
    def display_data_comparison(self, source_counts, target_counts, source, target):
        """Display comparison of data between databases"""
        self.stdout.write("\n=== Data Comparison ===")
        self.stdout.write(f"{'Model':<20} {source.upper():<10} {target.upper():<10} {'Status':<15}")
        self.stdout.write("-" * 60)
        
        all_models = set(source_counts.keys()) | set(target_counts.keys())
        
        for model in sorted(all_models):
            source_count = source_counts.get(model, 0)
            target_count = target_counts.get(model, 0)
            
            if isinstance(source_count, str) or isinstance(target_count, str):
                status = "ERROR"
                style = self.style.ERROR
            elif source_count == target_count:
                status = "SYNCED"
                style = self.style.SUCCESS
            elif source_count > target_count:
                status = "NEEDS SYNC"
                style = self.style.WARNING
            else:
                status = "TARGET > SRC"
                style = self.style.NOTICE
                
            line = f"{model:<20} {str(source_count):<10} {str(target_count):<10} {status:<15}"
            self.stdout.write(style(line))
    
    def perform_synchronization(self, source, target, source_counts, target_counts):
        """Perform actual data synchronization"""
        self.stdout.write(f"\n=== Synchronizing from {source} to {target} ===")
        
        # This is a simplified version. In production, you'd want to:
        # 1. Handle foreign key dependencies
        # 2. Use transactions
        # 3. Handle conflicts (update vs insert)
        # 4. Backup before sync
        
        try:
            # Run migrations on target database first
            self.stdout.write("Running migrations on target database...")
            call_command('migrate', database=f"{target}_db", verbosity=0)
            
            # Get webapp models in dependency order
            webapp_models = apps.get_app_config('webapp').get_models()
            
            for model in webapp_models:
                model_name = model._meta.model_name
                source_count = source_counts.get(model_name, 0)
                target_count = target_counts.get(model_name, 0)
                
                if isinstance(source_count, int) and source_count > target_count:
                    self.sync_model_data(model, f"{source}_db", f"{target}_db")
                    
            self.stdout.write(self.style.SUCCESS("Synchronization completed!"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Synchronization failed: {str(e)}"))
    
    def sync_model_data(self, model, source_db, target_db):
        """Synchronize data for a specific model"""
        model_name = model._meta.model_name
        
        try:
            # Get all records from source
            source_records = model.objects.using(source_db).all()
            
            # Clear target (simple approach - in production, use smarter merging)
            model.objects.using(target_db).all().delete()
            
            # Bulk create in target
            if source_records.exists():
                records_to_create = []
                for record in source_records:
                    # Reset primary key to allow insertion
                    record.pk = None
                    records_to_create.append(record)
                
                model.objects.using(target_db).bulk_create(records_to_create)
                self.stdout.write(f"Synced {len(records_to_create)} {model_name} records")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to sync {model_name}: {str(e)}"))