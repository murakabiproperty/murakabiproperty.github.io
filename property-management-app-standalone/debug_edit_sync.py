import sqlite3
import sys
from pathlib import Path
from airtable_sync import AirtableSync

def debug_edit_sync():
    """Debug edit property sync issues"""
    print("🔧 Debugging Edit Property Sync Issues")
    print("=" * 60)
    
    # Connect to database
    try:
        db_path = Path("property_management.db")
        if not db_path.exists():
            print("❌ Database file not found!")
            return
        
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Get all properties with Airtable record IDs
        cursor.execute('''
            SELECT id, nama_properti, status, airtable_record_id 
            FROM properties 
            WHERE airtable_record_id IS NOT NULL AND airtable_record_id != ""
        ''')
        properties = cursor.fetchall()
        
        if not properties:
            print("❌ No properties with Airtable record IDs found!")
            return
        
        print(f"✅ Found {len(properties)} properties with Airtable IDs:")
        for prop in properties:
            print(f"  - ID: {prop[0]}, Name: {prop[1]}, Status: {prop[2]}, Airtable ID: {prop[3]}")
        
        # Test Airtable connection
        print("\n🔗 Testing Airtable connection...")
        airtable_sync = AirtableSync()
        if not airtable_sync.test_connection():
            print("❌ Airtable connection failed!")
            return
        print("✅ Airtable connection successful")
        
        # Test updating the first property
        if properties:
            test_property = properties[0]
            property_id = test_property[0]
            airtable_record_id = test_property[3]
            
            print(f"\n🧪 Testing update for property ID {property_id} (Airtable: {airtable_record_id})")
            
            # Get complete property data
            cursor.execute('SELECT * FROM properties WHERE id=?', (property_id,))
            property_row = cursor.fetchone()
            
            if property_row:
                # Prepare test data (simulate edit)
                property_data = {
                    'nama_properti': property_row[1],
                    'lokasi': property_row[2],  
                    'tipe_properti': property_row[3],
                    'kamar_tidur': property_row[4],
                    'kamar_mandi': property_row[5],
                    'luas_bangunan': property_row[6],
                    'harga': property_row[7],
                    'status': 'Terjual',  # Test with Terjual status
                    'deskripsi': property_row[9],
                    'link_map': property_row[11] if len(property_row) > 11 else None
                }
                
                print(f"📝 Test property data: {property_data}")
                
                # Try to update in Airtable
                print("📤 Attempting Airtable update...")
                success, error = airtable_sync.update_property_in_airtable(airtable_record_id, property_data)
                
                if success:
                    print("✅ Update successful!")
                else:
                    print(f"❌ Update failed: {error}")
                    
                    # Try to get the record directly from Airtable to see what's there
                    print("\n🔍 Checking if record exists in Airtable...")
                    record = airtable_sync.get_record_by_id(airtable_record_id)
                    if record:
                        print("✅ Record found in Airtable:")
                        print(f"    Fields: {list(record.get('fields', {}).keys())}")
                    else:
                        print("❌ Record not found in Airtable - this could be the issue!")
                        print("   The record might have been deleted from Airtable.")
                        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    debug_edit_sync() 