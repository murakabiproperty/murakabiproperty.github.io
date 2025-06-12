#!/usr/bin/env python3
"""
Airtable Synchronization Module
Handles syncing properties between the Property Management App and Airtable
"""

import requests
import json
import mimetypes
from pathlib import Path
from airtable_config import AIRTABLE_CONFIG

class AirtableSync:
    def __init__(self):
        self.api_key = AIRTABLE_CONFIG['API_KEY']
        self.base_id = AIRTABLE_CONFIG['BASE_ID']
        self.table_name = AIRTABLE_CONFIG['TABLE_NAME']
        self.base_url = f"https://api.airtable.com/v0/{self.base_id}/{self.table_name}"
        
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def format_property_for_airtable(self, property_data):
        """
        Convert property data from Indonesian app format to English Airtable format
        """
        mapping = AIRTABLE_CONFIG['COLUMN_MAPPING'] 
        
        airtable_data = {}
        
        # Map all fields using the new Indonesian field names
        for app_field, airtable_field in mapping.items():
            if property_data.get(app_field) is not None:
                value = property_data[app_field]

                # Special handling for the 'Sold' checkbox field
                if app_field == 'status':
                    # The 'Sold' column in Airtable is a checkbox.
                    # It expects True if the status is 'terjual', otherwise False.
                    is_sold = (str(value).lower() == 'terjual')
                    airtable_data[airtable_field] = is_sold
                    print(f"🔄 Status mapping: '{value}' -> Sold checkbox: {is_sold}")
                elif value and str(value).strip():
                    airtable_data[airtable_field] = value
                    print(f"📝 Field mapping: {app_field} = '{value}' -> {airtable_field}")
                else:
                    print(f"⚠️  Skipping empty field: {app_field}")
        
        # Handle image upload if image_path is provided
        if property_data.get('gambar_path'):
            print(f"Attempting to upload image: {property_data['gambar_path']}")
            public_image_url = self.upload_image_to_imgbb(property_data['gambar_path'])
            if public_image_url:
                print(f"Image upload successful, URL: {public_image_url}")
                # Airtable expects an array of attachment objects, each with a URL
                airtable_data['Image'] = [{'url': public_image_url}]
            else:
                print("Image upload failed, skipping image field")
                # Don't include Image field if upload failed
        
        print(f"Final Airtable data: {airtable_data}")
        return airtable_data
    
    def add_property_to_airtable(self, property_data):
        """
        Add a new property to Airtable
        Returns a tuple (Airtable record ID, error message)
        """
        try:
            airtable_data = self.format_property_for_airtable(property_data)
            
            if not airtable_data:
                error_msg = "No data to send to Airtable after formatting."
                print(error_msg)
                return None, error_msg

            payload = {
                "fields": airtable_data
            }
            
            print(f"Sending to Airtable - Payload: {json.dumps(payload, indent=2)}")
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                data=json.dumps(payload)
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('id'), None
            else:
                error_msg = f"Error: {response.status_code} - {response.text}"
                print(f"Error adding to Airtable: {error_msg}")
                return None, error_msg
                
        except Exception as e:
            error_msg = f"Exception: {str(e)}"
            print(f"Exception adding to Airtable: {error_msg}")
            return None, error_msg
    
    def update_property_in_airtable(self, airtable_record_id, property_data):
        """
        Update an existing property in Airtable
        Returns a tuple (success_boolean, error_message)
        """
        try:
            print(f"🔄 Updating Airtable record: {airtable_record_id}")
            print(f"📝 Property data to update: {property_data}")
            
            airtable_data = self.format_property_for_airtable(property_data)
            
            if not airtable_data:
                error_msg = "No data to send to Airtable after formatting."
                print(f"❌ {error_msg}")
                return False, error_msg

            payload = {
                "fields": airtable_data
            }
            
            print(f"📤 Sending to Airtable - Payload: {json.dumps(payload, indent=2)}")
            
            url = f"{self.base_url}/{airtable_record_id}"
            response = requests.patch(
                url,
                headers=self.headers,
                data=json.dumps(payload)
            )
            
            print(f"📨 Airtable response status: {response.status_code}")
            print(f"📨 Airtable response text: {response.text}")
            
            if response.status_code == 200:
                print("✅ Successfully updated Airtable record")
                return True, None
            else:
                error_msg = f"Error: {response.status_code} - {response.text}"
                print(f"❌ Error updating Airtable record: {error_msg}")
                return False, error_msg
                
        except Exception as e:
            error_msg = f"Exception: {str(e)}"
            print(f"❌ Exception updating Airtable record: {error_msg}")
            return False, error_msg
    
    def delete_property_from_airtable(self, airtable_record_id):
        """
        Delete a property from Airtable
        Returns a tuple (success_boolean, error_message)
        """
        try:
            url = f"{self.base_url}/{airtable_record_id}"
            response = requests.delete(url, headers=self.headers)
            
            if response.status_code == 200:
                return True, None
            else:
                error_msg = f"Error: {response.status_code} - {response.text}"
                print(f"Error deleting from Airtable: {error_msg}")
                return False, error_msg
                
        except Exception as e:
            error_msg = f"Exception: {str(e)}"
            print(f"Exception deleting from Airtable: {error_msg}")
            return False, error_msg
    
    def test_connection(self):
        """
        Test connection to Airtable
        Returns True if connection is successful, False otherwise
        """
        try:
            # Try to get records (limit to 1 to minimize data transfer)
            url = f"{self.base_url}?maxRecords=1"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                return True
            else:
                print(f"Airtable connection test failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Exception testing Airtable connection: {str(e)}")
            return False
    
    def upload_image_to_imgbb(self, image_path):
        """
        Uploads an image to ImgBB and returns the public URL.
        """
        imgbb_api_key = AIRTABLE_CONFIG.get('IMGBB_API_KEY')
        if not imgbb_api_key or imgbb_api_key == 'YOUR_IMGBB_API_KEY':
            print("ERROR: ImgBB API key is not configured. Please get a free key from https://imgbb.com/api and add it to airtable_config.py")
            return None

        try:
            image_path = Path(image_path)
            if not image_path.exists():
                print(f"Image file not found: {image_path}")
                return None

            with open(image_path, "rb") as file:
                url = "https://api.imgbb.com/1/upload"
                payload = {
                    "key": imgbb_api_key,
                }
                files = {"image": file}
                response = requests.post(url, params=payload, files=files)
                
                print(f"ImgBB upload response status: {response.status_code}")
                print(f"ImgBB upload response text: {response.text}")

                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        # Return the direct URL for the image
                        return result["data"]["url"]
                    else:
                        print(f"ImgBB API returned an error: {result}")
                        return None
                else:
                    print(f"ImgBB upload failed with status code: {response.status_code}")
                    return None
        except Exception as e:
            print(f"An exception occurred during image upload to ImgBB: {e}")
            return None

    def upload_image_to_airtable(self, image_path):
        """
        DEPRECATED: This function is no longer used. Image are now uploaded to a third-party
        service to get a public URL before being sent to Airtable.
        """
        print("DEPRECATED: upload_image_to_airtable should not be called.")
        return None
    
    def get_all_records(self):
        """
        Get all records from Airtable
        Returns list of records if successful, empty list if failed
        """
        try:
            all_records = []
            offset = None
            
            while True:
                # Build URL with pagination
                url = self.base_url
                params = {'pageSize': 100}  # Maximum page size for Airtable
                
                if offset:
                    params['offset'] = offset
                
                # Make request
                response = requests.get(url, headers=self.headers, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    records = data.get('records', [])
                    all_records.extend(records)
                    
                    # Check if there are more records
                    offset = data.get('offset')
                    if not offset:
                        break
                else:
                    print(f"Error fetching records from Airtable: {response.status_code} - {response.text}")
                    return []
            
            print(f"Successfully fetched {len(all_records)} records from Airtable")
            return all_records
            
        except Exception as e:
            print(f"Exception fetching records from Airtable: {str(e)}")
            return []
    
    def get_record_by_id(self, record_id):
        """
        Get a specific record from Airtable by its ID
        Returns record data if successful, None if failed
        """
        try:
            url = f"{self.base_url}/{record_id}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching record from Airtable: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Exception fetching record from Airtable: {str(e)}")
            return None 