# Property Management System - User Manual

## Table of Contents
1. [Getting Started](#getting-started)
2. [Login and Authentication](#login-and-authentication)
3. [Managing Properties](#managing-properties)
4. [User Management](#user-management)
5. [Tips and Best Practices](#tips-and-best-practices)

## Getting Started

### Installation
1. Download the Property Management System folder
2. Right-click on `install.bat` and select "Run as administrator"
3. Follow the installation prompts
4. A desktop shortcut will be created

### First Launch
1. Double-click the "Property Manager" shortcut on your desktop
2. The application will open with a login screen
3. Use the default credentials:
   - Username: `admin`
   - Password: `admin123`
4. **IMPORTANT:** Change this password immediately after login!

## Login and Authentication

### Logging In
- Enter your username and password
- Press Enter or click "Login"
- The system will verify your credentials and log you in

### User Roles
- **Admin:** Can manage users, properties, and all system features
- **User:** Can manage properties but cannot create/manage other users

### Changing Your Password
1. Go to "Users" menu → "Change Password"
2. Enter your current password
3. Enter your new password (minimum 6 characters)
4. Click "Change Password"

## Managing Properties

### Adding a New Property

1. **Navigate to Add Property Tab**
   - Click on the "Add Property" tab at the top

2. **Fill in Property Details**
   - **Required Fields:**
     - Address: Full street address
     - City: City name
     - State: State or province
     - ZIP Code: Postal code
     - Property Type: Select from dropdown (House, Apartment, Condo, etc.)
   
   - **Optional Fields:**
     - Bedrooms: Number of bedrooms
     - Bathrooms: Number of bathrooms
     - Square Feet: Total square footage
     - Price: Property price in dollars
     - Description: Additional details about the property

3. **Save the Property**
   - Click "Add Property" to save
   - Click "Clear Form" to reset all fields

### Viewing Properties

1. **Properties Tab**
   - Click on the "Properties" tab to view all properties
   - Properties are displayed in a table format

2. **Search Properties**
   - Use the search box to find specific properties
   - Search works on address, city, state, and property type
   - Click "Search" or press Enter
   - Click "Refresh" to show all properties again

### Editing Properties

1. **Select a Property**
   - Click on a property row in the table
   - The row will be highlighted

2. **Edit Property**
   - Click "Edit Property" button
   - A new window will open with current property details
   - Modify any fields as needed
   - Click "Save Changes" to update
   - Click "Cancel" to discard changes

### Updating Property Status

1. **Select a Property**
   - Click on a property row in the table

2. **Update Status**
   - Click "Update Status" button
   - Choose from available statuses:
     - **Available:** Property is on the market
     - **Pending:** Under contract or has an offer
     - **Sold:** Property has been sold
     - **Rented:** Property is currently rented
     - **Unavailable:** Temporarily off the market
   - Click "Update" to save the new status

### Deleting Properties

1. **Select a Property**
   - Click on a property row in the table

2. **Delete Property**
   - Click "Delete Property" button
   - Confirm the deletion when prompted
   - **Warning:** This action cannot be undone!

## User Management (Admin Only)

### Creating New Users

1. **Access User Menu**
   - Go to "Users" menu → "Create User"

2. **Enter User Details**
   - Username: Must be unique
   - Password: Minimum 6 characters
   - Role: Select "user" or "admin"

3. **Create User**
   - Click "Create User" to save
   - The new user can now log in with these credentials

### User Roles Explained

- **Admin Users Can:**
  - Create and manage other users
  - Add, edit, and delete properties
  - Update property statuses
  - Change their own password
  - Access all system features

- **Regular Users Can:**
  - Add, edit, and delete properties
  - Update property statuses
  - Change their own password
  - View and search properties

## Tips and Best Practices

### Data Entry Tips
- **Be Consistent:** Use consistent formatting for addresses and city names
- **Complete Information:** Fill in as many fields as possible for better tracking
- **Regular Updates:** Keep property statuses current
- **Backup Data:** Regularly backup your `property_management.db` file

### Security Best Practices
- **Change Default Password:** Always change the default admin password
- **Strong Passwords:** Use passwords with at least 8 characters
- **Limit Admin Access:** Only give admin privileges to trusted users
- **Regular Password Changes:** Update passwords periodically

### Property Status Guidelines
- Update status immediately when property circumstances change
- Use "Pending" for properties with accepted offers
- Use "Unavailable" for properties temporarily off the market
- Mark as "Sold" or "Rented" only when deals are complete

### Search Tips
- Use partial words for broader searches
- Search by city to find all properties in an area
- Search by property type to filter specific kinds of properties
- Use the "Refresh" button to clear search filters

### Troubleshooting

#### Application Won't Start
- Check that Python is installed and in PATH
- Try running `run_property_manager.bat` as administrator
- Restart your computer and try again

#### Login Issues
- Verify username and password are correct
- Check that Caps Lock is not on
- Try the default admin credentials if you're locked out

#### Data Issues
- If data appears corrupted, check the `property_management.db` file
- Contact your administrator for database recovery
- Regular backups prevent data loss

#### Performance Issues
- Close other applications to free up memory
- Restart the application if it becomes slow
- Consider archiving old properties if database becomes large

### Keyboard Shortcuts
- **Enter:** Submit login or search
- **Tab:** Navigate between form fields
- **Escape:** Close dialog windows
- **F5:** Refresh property list

### Database Location
Your property data is stored in: `property_management.db`
- This file contains all your property and user data
- Back up this file regularly
- Do not delete or modify this file manually

### Getting Help
- Check this manual for common questions
- Review error messages for specific issues
- Contact your system administrator for technical support
- Keep the README.md file for installation and setup help

## Maintenance

### Regular Tasks
- Update property statuses weekly
- Review and clean up old or duplicate entries monthly
- Change passwords every 3-6 months
- Backup database file weekly

### Data Backup
1. Close the Property Management System
2. Copy the `property_management.db` file to a safe location
3. Store backups in multiple locations (cloud storage, external drive)
4. Test backups periodically by restoring to a test environment

This completes the user manual. For technical support or additional features, contact your system administrator. 