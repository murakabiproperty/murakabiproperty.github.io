# Airtable Configuration
# Replace these values with your actual Airtable credentials

import os

AIRTABLE_CONFIG = {
    'API_KEY': os.getenv('AIRTABLE_API_KEY', 'pat0cJUQcyOFxDllX.c2421f2ebdfeba1fdf48d662fa60ef05652a4b2deb095f5c5781362aa795c958'),
    'BASE_ID': os.getenv('AIRTABLE_BASE_ID', 'appx1T49Qqh0g3AcF'),
    'TABLE_NAME': os.getenv('AIRTABLE_TABLE_NAME', 'Properties'),
    
    # IMPORTANT: Get your free API key from https://imgbb.com/api
    'IMGBB_API_KEY': os.getenv('IMGBB_API_KEY', 'ad6f1ed7bab66c56adbf91a8a04cd4ec'),
    
    # Column mapping from Property Management App to Airtable
    'COLUMN_MAPPING': {
        # App field -> Airtable field (Indonesian app to English Airtable)
        'nama_properti': 'Name',           # Property name
        'lokasi': 'Location',             # Full location/address (user confirmed column name)
        'tipe_properti': 'Tipe Properti',   # This column does not exist in the user's Airtable
        'kamar_tidur': 'Bedrooms',        # Bedrooms
        'kamar_mandi': 'Bathrooms',       # Bathrooms
        'luas_bangunan': 'Area',          # Building area
        'harga': 'Price',                 # Price
        'deskripsi': 'Description',       # Description (user confirmed column name)
        'link_map': 'MapLink',            # Google Maps link (user confirmed column name)
        'gambar_path': 'Image',           # Image attachment (user confirmed column name)
        'status': 'Sold'                  # Status maps to the 'Sold' checkbox
    },
    
    # Status mapping - no longer needed as we map to a boolean checkbox
    'STATUS_TO_AIRTABLE_MAPPING': {},
    
    # Reverse mapping for syncing from Airtable to app
    'AIRTABLE_TO_APP_MAPPING': {
        'Name': 'nama_properti',
        'Location': 'lokasi', 
        'PropertyType': 'tipe_properti',
        'Bedrooms': 'kamar_tidur',
        'Bathrooms': 'kamar_mandi',
        'Area': 'luas_bangunan',
        'Price': 'harga',
        'Description': 'deskripsi',
        'MapLink': 'link_map',
        'Status': 'status'
    },
    
    # Status mapping from Airtable to app
    'AIRTABLE_TO_STATUS_MAPPING': {
        'Available': 'Tersedia',
        'Sold': 'Terjual',
        'Pending': 'Pending',
        'Rented': 'Disewa'
    }
} 