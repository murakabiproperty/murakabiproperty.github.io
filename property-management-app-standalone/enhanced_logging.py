"""
Enhanced logging module for Property Management System
Provides detailed logging for debugging sync issues
"""

import logging
import os
from datetime import datetime
from pathlib import Path

class PropertyLogger:
    def __init__(self):
        # Create logs directory if it doesn't exist
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)
        
        # Setup loggers
        self.setup_loggers()
    
    def setup_loggers(self):
        """Setup different loggers for different purposes"""
        
        # Main application logger
        self.app_logger = logging.getLogger('PropertyApp')
        self.app_logger.setLevel(logging.DEBUG)
        
        # Airtable sync logger
        self.sync_logger = logging.getLogger('AirtableSync')
        self.sync_logger.setLevel(logging.DEBUG)
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # File handlers
        app_file_handler = logging.FileHandler(
            self.logs_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log",
            encoding='utf-8'
        )
        app_file_handler.setLevel(logging.DEBUG)
        app_file_handler.setFormatter(detailed_formatter)
        
        sync_file_handler = logging.FileHandler(
            self.logs_dir / f"airtable_sync_{datetime.now().strftime('%Y%m%d')}.log",
            encoding='utf-8'
        )
        sync_file_handler.setLevel(logging.DEBUG)
        sync_file_handler.setFormatter(detailed_formatter)
        
        # Console handler (only for errors and warnings)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(simple_formatter)
        
        # Add handlers to loggers
        if not self.app_logger.handlers:
            self.app_logger.addHandler(app_file_handler)
            self.app_logger.addHandler(console_handler)
        
        if not self.sync_logger.handlers:
            self.sync_logger.addHandler(sync_file_handler)
            self.sync_logger.addHandler(console_handler)
    
    def log_property_edit(self, property_id, property_data, airtable_record_id=None):
        """Log property edit attempt"""
        self.app_logger.info(f"🔄 Starting property edit for ID: {property_id}")
        self.app_logger.debug(f"Property data: {property_data}")
        if airtable_record_id:
            self.app_logger.info(f"Airtable record ID: {airtable_record_id}")
        else:
            self.app_logger.warning("No Airtable record ID found for this property")
    
    def log_sync_attempt(self, airtable_record_id, property_data):
        """Log Airtable sync attempt"""
        self.sync_logger.info(f"🔄 Attempting sync for Airtable record: {airtable_record_id}")
        self.sync_logger.debug(f"Data to sync: {property_data}")
    
    def log_sync_success(self, airtable_record_id):
        """Log successful sync"""
        self.sync_logger.info(f"✅ Sync successful for record: {airtable_record_id}")
    
    def log_sync_failure(self, airtable_record_id, error_message):
        """Log sync failure with detailed error"""
        self.sync_logger.error(f"❌ Sync failed for record: {airtable_record_id}")
        self.sync_logger.error(f"Error details: {error_message}")
    
    def log_http_request(self, method, url, status_code, response_text=None):
        """Log HTTP request details"""
        self.sync_logger.debug(f"HTTP {method} {url} - Status: {status_code}")
        if response_text:
            self.sync_logger.debug(f"Response: {response_text[:500]}...")  # First 500 chars
    
    def log_database_operation(self, operation, table, record_id=None):
        """Log database operations"""
        if record_id:
            self.app_logger.debug(f"Database {operation} on {table} - Record ID: {record_id}")
        else:
            self.app_logger.debug(f"Database {operation} on {table}")
    
    def get_recent_sync_errors(self, hours=24):
        """Get recent sync errors from log file"""
        sync_log_file = self.logs_dir / f"airtable_sync_{datetime.now().strftime('%Y%m%d')}.log"
        
        if not sync_log_file.exists():
            return []
        
        errors = []
        try:
            with open(sync_log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            # Look for ERROR lines in the last 24 hours
            cutoff_time = datetime.now().timestamp() - (hours * 3600)
            
            for line in lines:
                if 'ERROR' in line and '❌' in line:
                    try:
                        # Parse timestamp from log line
                        timestamp_str = line.split(' - ')[0]
                        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                        
                        if timestamp.timestamp() > cutoff_time:
                            errors.append(line.strip())
                    except:
                        # If parsing fails, include the line anyway
                        errors.append(line.strip())
                        
        except Exception as e:
            self.app_logger.error(f"Failed to read sync error log: {str(e)}")
        
        return errors[-10:]  # Return last 10 errors

# Global logger instance
property_logger = PropertyLogger() 