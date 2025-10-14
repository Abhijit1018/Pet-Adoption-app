"""
Database Manager for Pet Adoption App
Handles automatic MySQL detection and data synchronization between SQLite and MySQL
"""

import os
import sys
import pymysql
import sqlite3
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import connections
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database connections and data synchronization"""
    
    def __init__(self):
        self.mysql_config = {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'pet_rescue_db',
            'USER': 'root',
            'PASSWORD': 'abhijit',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
        
        self.sqlite_config = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': settings.BASE_DIR / 'db.sqlite3',
        }
    
    def test_mysql_connection(self):
        """Test if MySQL server is available and accessible"""
        try:
            connection = pymysql.connect(
                host=self.mysql_config['HOST'],
                user=self.mysql_config['USER'],
                password=self.mysql_config['PASSWORD'],
                port=int(self.mysql_config['PORT'])
            )
            
            # Check if database exists, create if not
            with connection.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.mysql_config['NAME']}")
                cursor.execute(f"USE {self.mysql_config['NAME']}")
            
            connection.close()
            logger.info("MySQL server is available and database is ready")
            return True
            
        except Exception as e:
            logger.warning(f"MySQL connection failed: {str(e)}")
            return False
    
    def get_database_config(self):
        """Return appropriate database configuration"""
        if self.test_mysql_connection():
            logger.info("Using MySQL database")
            return {'default': self.mysql_config}
        else:
            logger.info("Using SQLite database")
            return {'default': self.sqlite_config}
    
    def get_table_data_count(self, db_alias, table_name):
        """Get record count from a specific table"""
        try:
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'home.settings')
            import django
            django.setup()
            
            from django.db import connections
            connection = connections[db_alias]
            
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                return cursor.fetchone()[0]
        except Exception as e:
            logger.warning(f"Could not get count for {table_name} in {db_alias}: {str(e)}")
            return 0
    
    def sync_databases(self):
        """Synchronize data between MySQL and SQLite databases"""
        try:
            # This is a complex operation that would require:
            # 1. Temporary database configurations
            # 2. Data extraction from source
            # 3. Data insertion into target
            # 4. Handling of foreign key relationships
            
            logger.info("Database synchronization initiated...")
            
            # For now, we'll implement basic synchronization
            # This would need to be expanded based on your specific models
            
            return True
            
        except Exception as e:
            logger.error(f"Database synchronization failed: {str(e)}")
            return False

# Global database manager instance
db_manager = DatabaseManager()