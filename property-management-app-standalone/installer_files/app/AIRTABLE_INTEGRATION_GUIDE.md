# Airtable Integration Setup Guide

This guide will help you set up automatic synchronization between your Property Management Application and Airtable.

## Prerequisites

1. **Airtable Account**: You need an active Airtable account
2. **Airtable Base**: You should already have your Airtable base configured (as described in the static website's AIRTABLE_SETUP.md)

## Step 1: Install Required Dependencies

The integration requires the `requests` and `Pillow` libraries for API communication and image handling. Install them by running:

```bash
pip install requests Pillow
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

## Step 2: Configure Airtable Credentials

1. **Open** `airtable_config.py`
2. **Update** your Airtable credentials:

```python
AIRTABLE_CONFIG = {
    'API_KEY': 'YOUR_ACTUAL_API_KEY_HERE',  # Replace with your Airtable API key
    'BASE_ID': 'YOUR_ACTUAL_BASE_ID_HERE',  # Replace with your Airtable Base ID
    'TABLE_NAME': 'Properties',  # Your table name in Airtable
    # ... rest of the configuration
}
```

### How to Get Your Credentials:

**API Key:**
1. Go to [airtable.com/account](https://airtable.com/account)
2. Scroll to the "API" section
3. Generate or copy your Personal Access Token

**Base ID:**
1. Go to [airtable.com/api](https://airtable.com/api)
2. Click on your base
3. Copy the Base ID from the URL (starts with "app...")

## Step 3: Airtable Column Mapping

The application automatically maps your property fields to Airtable columns:

| Application Field | Airtable Column | Description |
|------------------|-----------------|-------------|
| Address | Name | Property address becomes the record name |
| City + State | Location | Combined location string |
| Square Feet | Area | Property area in sq ft |
| Bedrooms | Bedrooms | Number of bedrooms |
| Bathrooms | Bathrooms | Number of bathrooms |
| Price | Price | Property price |
| Description | Description | Property description |
| Status | Sold | Converted to boolean (sold/rented = true) |
| Image | Image | Property image automatically uploaded |
| Google Maps Link | MapLink | Google Maps share URL for property location |

### Status Updates
- When you change a property's status, it will:
  1. Update locally
  2. Sync the status to Airtable as a "Sold" boolean
  3. Update your website display

### Google Maps Integration
- **Open Google Maps**: Click to open Google Maps with property address pre-filled
- **Get Share Link**: Follow the guided instructions to get a Google Maps share link
- **Validate Links**: Built-in validation ensures proper Google Maps URLs
- **Auto-Sync**: Map links automatically sync to Airtable's MapLink field

✅ **Automatic Sync**: Properties are automatically synced when added/updated/deleted  
✅ **Image Upload**: Property images are automatically uploaded to Airtable  
✅ **Google Maps Integration**: Easy Google Maps link integration with validation  
✅ **Error Handling**: Application continues working even if Airtable is unavailable  
✅ **Status Feedback**: Clear messages indicate sync success/failure  
✅ **Connection Testing**: Built-in tool to test Airtable connectivity  
✅ **Data Mapping**: Intelligent mapping between app fields and Airtable columns  
✅ **Image Preview**: Live preview of selected images before saving  
✅ **Image Storage**: Local image storage with automatic file management  
✅ **Map Links**: Open Google Maps for property location and validate share links