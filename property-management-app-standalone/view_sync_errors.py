#!/usr/bin/env python3
"""
View recent sync errors from the log files
"""

import sys
from pathlib import Path
from datetime import datetime
from enhanced_logging import property_logger

def view_recent_errors():
    """Display recent sync errors"""
    print("🔍 Recent Airtable Sync Errors")
    print("=" * 50)
    
    # Get recent errors from the last 24 hours
    errors = property_logger.get_recent_sync_errors(hours=24)
    
    if not errors:
        print("✅ No sync errors found in the last 24 hours!")
        return
    
    print(f"Found {len(errors)} recent sync errors:\n")
    
    for i, error in enumerate(errors, 1):
        print(f"{i}. {error}")
        print("-" * 80)
    
    print(f"\nTotal errors: {len(errors)}")
    
    # Also check if log files exist
    logs_dir = Path("logs")
    if logs_dir.exists():
        print(f"\nLog files available:")
        for log_file in sorted(logs_dir.glob("*.log")):
            size = log_file.stat().st_size
            modified = datetime.fromtimestamp(log_file.stat().st_mtime)
            print(f"  - {log_file.name} ({size} bytes, modified: {modified.strftime('%Y-%m-%d %H:%M:%S')})")
    else:
        print("\n⚠️  No logs directory found. Logging may not be working properly.")

def view_app_logs():
    """Display recent app logs"""
    print("\n📱 Recent Application Logs")
    print("=" * 50)
    
    logs_dir = Path("logs")
    today = datetime.now().strftime('%Y%m%d')
    app_log_file = logs_dir / f"app_{today}.log"
    
    if not app_log_file.exists():
        print("No app log file found for today.")
        return
    
    try:
        with open(app_log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Show last 20 lines
        print("Last 20 lines from app log:")
        print("-" * 50)
        
        for line in lines[-20:]:
            print(line.strip())
            
    except Exception as e:
        print(f"Error reading app log: {str(e)}")

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--app":
        view_app_logs()
    else:
        view_recent_errors()
        
        # Ask if user wants to see app logs too
        try:
            response = input("\nDo you want to see recent app logs? (y/n): ").lower()
            if response == 'y':
                view_app_logs()
        except KeyboardInterrupt:
            print("\nBye!")

if __name__ == "__main__":
    main() 