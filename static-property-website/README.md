# Property Management System

A desktop application for managing real estate properties with user authentication and comprehensive property management features.

## Features

### 🔐 User Authentication
- Secure login system with password hashing
- Admin and user roles
- Password change functionality
- User creation (admin only)

### 🏠 Property Management
- Add new properties with detailed information
- Edit existing property details
- Update property status (Available, Pending, Sold, Rented, Unavailable)
- Delete properties
- Search and filter properties
- Comprehensive property details including:
  - Address, City, State, ZIP Code
  - Property type (House, Apartment, Condo, etc.)
  - Bedrooms, Bathrooms, Square footage
  - Price and description

### 💻 User Interface
- Modern, intuitive GUI built with Tkinter
- Tabbed interface for easy navigation
- Responsive design with scrollable forms
- Real-time search functionality

### 🗄️ Database
- SQLite database for data storage
- Automatic database initialization
- Data persistence and backup

## Installation

### Prerequisites
- Windows 10 or higher
- Python 3.7 or higher (download from [python.org](https://www.python.org/))
- Make sure to check "Add Python to PATH" during Python installation

### Automatic Installation
1. Download or clone this repository
2. Right-click on `install.bat` and select "Run as administrator"
3. Follow the installation prompts
4. The installer will:
   - Check Python installation
   - Create a virtual environment
   - Install dependencies
   - Create a desktop shortcut

### Manual Installation
If the automatic installer doesn't work:

1. Open Command Prompt or PowerShell
2. Navigate to the project directory
3. Create virtual environment:
   ```
   python -m venv property_manager_env
   ```
4. Activate virtual environment:
   ```
   property_manager_env\Scripts\activate
   ```
5. Run the application:
   ```
   python main.py
   ```

## Usage

### First Time Setup
1. Run the application using the desktop shortcut or `run_property_manager.bat`
2. Login with default credentials:
   - **Username:** admin
   - **Password:** admin123
3. **IMPORTANT:** Change the default password immediately after first login!

### Adding Properties
1. Click on the "Add Property" tab
2. Fill in the property details:
   - Required fields: Address, City, State, ZIP Code, Property Type
   - Optional fields: Bedrooms, Bathrooms, Square footage, Price, Description
3. Click "Add Property" to save

### Managing Properties
1. Go to the "Properties" tab to view all properties
2. Use the search box to find specific properties
3. Select a property and use the buttons to:
   - **Edit Property:** Modify property details
   - **Update Status:** Change property status (available, pending, sold, etc.)
   - **Delete Property:** Remove property from the database

### User Management (Admin Only)
1. Admin users can create new users via the "Users" menu
2. Set username, password, and role (user or admin)
3. Users can change their own passwords via the "Users" menu

### Property Status Options
- **Available:** Property is on the market
- **Pending:** Property has an offer or is under contract
- **Sold:** Property has been sold
- **Rented:** Property is currently rented
- **Unavailable:** Property is temporarily off the market

## File Structure
```
property-management-app-standalone/
├── main.py                    # Main application file
├── install.bat               # Windows installer script
├── uninstall.bat            # Uninstaller script
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── USER_MANUAL.md           # Detailed user guide
└── property_management.db   # SQLite database (created at runtime)
```

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `password_hash`: Hashed password
- `role`: User role (admin/user)
- `created_at`: Account creation timestamp

### Properties Table
- `id`: Primary key
- `address`: Property address
- `city`: City name
- `state`: State/Province
- `zip_code`: ZIP/Postal code
- `property_type`: Type of property
- `bedrooms`: Number of bedrooms
- `bathrooms`: Number of bathrooms
- `sqft`: Square footage
- `price`: Property price
- `status`: Current status
- `description`: Property description
- `added_by`: Username who added the property
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## Security Features
- Passwords are hashed using SHA-256
- User sessions with role-based access control
- Database uses parameterized queries to prevent SQL injection

## Troubleshooting

### Common Issues
1. **"Python is not installed"**
   - Install Python from python.org
   - Make sure to check "Add Python to PATH"

2. **Application won't start**
   - Try running `run_property_manager.bat` as administrator
   - Check if the virtual environment was created properly

3. **Database errors**
   - Delete `property_management.db` to reset the database
   - The application will recreate it with default settings

4. **Permission errors**
   - Run the installer as administrator
   - Make sure you have write permissions in the installation directory

### Getting Help
If you encounter issues:
1. Check the error messages in the command prompt
2. Ensure Python is properly installed and in PATH
3. Try running the application manually: `python main.py`

## System Requirements
- **OS:** Windows 10 or higher
- **Python:** 3.7 or higher
- **RAM:** 512MB minimum
- **Storage:** 50MB for application and database
- **Display:** 1024x768 minimum resolution

## License
This software is provided as-is for educational and commercial use.

## Support
For technical support or feature requests, please refer to the documentation or contact your system administrator. 