#!/usr/bin/env python3
"""
Test script untuk debugging sinkronisasi status Airtable
"""

from airtable_sync import AirtableSync
import json

def test_status_sync():
    """Test fungsi sinkronisasi status ke Airtable"""
    
    print("🔧 Testing Airtable Status Sync")
    print("=" * 50)
    
    # Inisialisasi AirtableSync
    airtable_sync = AirtableSync()
    
    # Test koneksi
    print("1. Testing connection to Airtable...")
    if airtable_sync.test_connection():
        print("✅ Connection successful")
    else:
        print("❌ Connection failed")
        return
    
    # Ambil semua records untuk melihat data yang ada
    print("\n2. Fetching all records from Airtable...")
    records = airtable_sync.get_all_records()
    
    if not records:
        print("❌ No records found or failed to fetch")
        return
    
    print(f"✅ Found {len(records)} records")
    
    # Tampilkan record pertama untuk debugging
    if records:
        print("\n3. First record structure:")
        first_record = records[0]
        print(f"Record ID: {first_record['id']}")
        print(f"Fields: {json.dumps(first_record.get('fields', {}), indent=2)}")
    
    # Test format status untuk berbagai nilai
    print("\n4. Testing status mapping...")
    test_data_sets = [
        {'status': 'Terjual'},
        {'status': 'terjual'},
        {'status': 'TERJUAL'},
        {'status': 'Tersedia'},
        {'status': 'tersedia'},
    ]
    
    for test_data in test_data_sets:
        formatted = airtable_sync.format_property_for_airtable(test_data)
        sold_value = formatted.get('Sold', 'NOT_FOUND')
        print(f"  Status '{test_data['status']}' -> Sold: {sold_value}")
    
    # Test update actual record jika ada
    if records:
        print(f"\n5. Testing actual update for record: {records[0]['id']}")
        
        # Test data dengan status Terjual
        test_property_data = {
            'nama_properti': 'Test Property',
            'lokasi': 'Test Location',
            'status': 'Terjual',  # Status yang harus mengset Sold = True
            'harga': 100000000
        }
        
        print("Testing update with status 'Terjual':")
        success, error = airtable_sync.update_property_in_airtable(
            records[0]['id'], 
            test_property_data
        )
        
        if success:
            print("✅ Update successful!")
            
            # Verifikasi hasil update
            updated_record = airtable_sync.get_record_by_id(records[0]['id'])
            if updated_record:
                sold_field = updated_record.get('fields', {}).get('Sold', 'NOT_FOUND')
                print(f"✅ Verified: Sold field is now: {sold_field}")
            
        else:
            print(f"❌ Update failed: {error}")
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!")

if __name__ == "__main__":
    test_status_sync() 