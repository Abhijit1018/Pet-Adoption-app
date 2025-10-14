"""
Database status and synchronization checker
"""

from django.core.management.base import BaseCommand
from django.db import connections
from django.contrib.auth.models import User
from webapp.models import UserProfile, AdminProfile, Pet, AdoptionRequest
import pymysql

class Command(BaseCommand):
    help = 'Check database status and synchronization'

    def handle(self, *args, **options):
        self.stdout.write("=== Database Status Check ===")
        
        # Check database availability
        sqlite_available = self.check_database('sqlite_db', 'SQLite')
        mysql_available = self.check_database('mysql_db', 'MySQL')
        
        if not sqlite_available and not mysql_available:
            self.stdout.write(self.style.ERROR("No databases available!"))
            return
        
        # Show current default database
        from django.conf import settings
        default_engine = settings.DATABASES['default']['ENGINE']
        if 'mysql' in default_engine:
            current_db = 'MySQL'
        else:
            current_db = 'SQLite'
        
        self.stdout.write(f"\n🔹 Current default database: {current_db}")
        
        # Compare data if both are available
        if sqlite_available and mysql_available:
            self.compare_databases()
        
        # Show recommendations
        self.show_recommendations(sqlite_available, mysql_available)
    
    def check_database(self, db_alias, name):
        """Check if database is available and show stats"""
        try:
            conn = connections[db_alias]
            conn.ensure_connection()
            
            # Get record counts
            models = [
                ('Users', User),
                ('User Profiles', UserProfile),
                ('Admin Profiles', AdminProfile),
                ('Pets', Pet),
                ('Adoption Requests', AdoptionRequest),
            ]
            
            self.stdout.write(f"\n✅ {name} Database:")
            total_records = 0
            
            for model_name, model_class in models:
                try:
                    count = model_class.objects.using(db_alias).count()
                    total_records += count
                    self.stdout.write(f"   {model_name}: {count}")
                except Exception as e:
                    self.stdout.write(f"   {model_name}: Error - {str(e)}")
            
            self.stdout.write(f"   Total: {total_records} records")
            return True
            
        except Exception as e:
            self.stdout.write(f"\n❌ {name} Database: Unavailable ({str(e)})")
            return False
    
    def compare_databases(self):
        """Compare data between SQLite and MySQL"""
        self.stdout.write(f"\n=== Data Comparison ===")
        
        models = [
            ('Users', User),
            ('User Profiles', UserProfile),
            ('Admin Profiles', AdminProfile),
            ('Pets', Pet),
            ('Adoption Requests', AdoptionRequest),
        ]
        
        self.stdout.write(f"{'Model':<20} {'SQLite':<10} {'MySQL':<10} {'Status':<15}")
        self.stdout.write("-" * 60)
        
        all_synced = True
        
        for model_name, model_class in models:
            try:
                sqlite_count = model_class.objects.using('sqlite_db').count()
                mysql_count = model_class.objects.using('mysql_db').count()
                
                if sqlite_count == mysql_count:
                    status = "✅ SYNCED"
                    style = self.style.SUCCESS
                elif abs(sqlite_count - mysql_count) <= 1:
                    status = "⚠️ MINOR DIFF"
                    style = self.style.WARNING
                    all_synced = False
                else:
                    status = "❌ OUT OF SYNC"
                    style = self.style.ERROR
                    all_synced = False
                
                line = f"{model_name:<20} {sqlite_count:<10} {mysql_count:<10} {status:<15}"
                self.stdout.write(style(line))
                
            except Exception as e:
                line = f"{model_name:<20} {'Error':<10} {'Error':<10} {'❌ ERROR':<15}"
                self.stdout.write(self.style.ERROR(line))
                all_synced = False
        
        if all_synced:
            self.stdout.write(self.style.SUCCESS("\n🎉 Databases are fully synchronized!"))
        else:
            self.stdout.write(self.style.WARNING("\n⚠️ Databases need synchronization"))
    
    def show_recommendations(self, sqlite_available, mysql_available):
        """Show recommendations based on database status"""
        self.stdout.write(f"\n=== Recommendations ===")
        
        if sqlite_available and mysql_available:
            self.stdout.write("✅ Both databases are available")
            self.stdout.write("💡 Run 'python manage.py smart_sync --direction=sqlite-to-mysql' to sync data")
            self.stdout.write("💡 Run 'python manage.py smart_sync --direction=mysql-to-sqlite' to sync backwards")
        elif sqlite_available and not mysql_available:
            self.stdout.write("⚠️ Only SQLite is available")
            self.stdout.write("💡 Install and configure MySQL server to enable dual database setup")
        elif mysql_available and not sqlite_available:
            self.stdout.write("⚠️ Only MySQL is available") 
            self.stdout.write("💡 SQLite should always be available as fallback")
        else:
            self.stdout.write("❌ No databases available")
            self.stdout.write("💡 Check your database configuration")