#!/bin/bash

# Property Management System - Complete Installer Builder (Linux/macOS)
# ====================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================================${NC}"
    echo
}

print_step() {
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}$(echo "$1" | sed 's/./=/g')${NC}"
    echo
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ WARNING: $1${NC}"
}

print_error() {
    echo -e "${RED}✗ ERROR: $1${NC}"
}

# Main script
print_header "Property Management System - Complete Installer Builder"

echo "This script will:"
echo "1. Check system requirements"
echo "2. Install required Python packages"
echo "3. Create application icon"
echo "4. Build standalone executable"
echo "5. Create distributable package"
echo

# Check if Python is installed
print_step "Step 1/5: Checking system requirements..."

if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        print_error "Python is not installed!"
        echo "Please install Python 3.6+ from https://python.org/"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Get Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
print_success "Found Python $PYTHON_VERSION"

# Check if pip is available
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    print_error "pip is not available!"
    echo "Please ensure pip is installed with Python"
    exit 1
fi
print_success "pip is available"

# Check for required system packages
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    print_success "Detected Linux system"
    # Check for tkinter (often separate package on Linux)
    if ! $PYTHON_CMD -c "import tkinter" 2>/dev/null; then
        print_warning "tkinter not found. You may need to install python3-tk"
        echo "On Ubuntu/Debian: sudo apt-get install python3-tk"
        echo "On CentOS/RHEL: sudo yum install tkinter"
        echo "On Fedora: sudo dnf install python3-tkinter"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    print_success "Detected macOS system"
    # Check for tkinter
    if ! $PYTHON_CMD -c "import tkinter" 2>/dev/null; then
        print_warning "tkinter not found. You may need to reinstall Python with tkinter support"
    fi
fi

# Step 2: Install required packages
print_step "Step 2/5: Installing required Python packages..."

PACKAGES=(
    "cx_Freeze"
    "requests"
    "urllib3"
    "certifi"
    "charset-normalizer"
    "idna"
    "Pillow"
)

for package in "${PACKAGES[@]}"; do
    echo "Installing $package..."
    if $PYTHON_CMD -m pip install "$package" --quiet --disable-pip-version-check; then
        print_success "$package installed successfully"
    else
        print_warning "Failed to install $package globally, trying with --user flag..."
        if $PYTHON_CMD -m pip install "$package" --user --quiet --disable-pip-version-check; then
            print_success "$package installed successfully (user mode)"
        else
            print_error "Failed to install $package completely!"
            exit 1
        fi
    fi
done

# Step 3: Create application icon
print_step "Step 3/5: Creating application icon..."

if [[ -f "create_icon.py" ]]; then
    if $PYTHON_CMD create_icon.py; then
        print_success "Application icon created successfully"
    else
        print_warning "Failed to create custom icon, using default..."
    fi
else
    print_warning "create_icon.py not found, skipping icon creation..."
fi

# Step 4: Build executable
print_step "Step 4/5: Building standalone executable..."

# Clean previous builds
for dir in "build" "dist" "installer_files"; do
    if [[ -d "$dir" ]]; then
        rm -rf "$dir"
        print_success "Cleaned $dir directory"
    fi
done

# Build the executable
if $PYTHON_CMD build_installer.py; then
    print_success "Executable built successfully"
else
    print_error "Failed to build executable!"
    echo
    echo "Troubleshooting tips:"
    echo "- Make sure main.py exists"
    echo "- Check that all dependencies are installed"
    echo "- Verify no syntax errors in main.py"
    echo "- Check that tkinter is properly installed"
    exit 1
fi

# Step 5: Create distributable package
print_step "Step 5/5: Creating distributable package..."

if [[ -d "installer_files/app" ]]; then
    # Create a tarball for distribution
    PACKAGE_NAME="PropertyManagementSystem_$(date +%Y%m%d_%H%M%S)"
    
    # Create package directory
    mkdir -p "packages"
    
    # Copy application files
    cp -r "installer_files/app" "packages/$PACKAGE_NAME"
    
    # Copy documentation and scripts
    for file in "AIRTABLE_INTEGRATION_GUIDE.md" "USER_MANUAL.md" "requirements.txt" "README.md"; do
        if [[ -f "$file" ]]; then
            cp "$file" "packages/$PACKAGE_NAME/"
            print_success "Copied $file"
        fi
    done
    
    # Create installation script
    cat > "packages/$PACKAGE_NAME/install.sh" << 'EOF'
#!/bin/bash

# Property Management System Installation Script
echo "Installing Property Management System..."

# Make executable
chmod +x PropertyManager

# Create desktop shortcut (if running in desktop environment)
if [[ -n "$DESKTOP_SESSION" ]]; then
    DESKTOP_FILE="$HOME/Desktop/Property Management System.desktop"
    cat > "$DESKTOP_FILE" << DESKTOP_EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Property Management System
Comment=Desktop Property Management Application
Exec=$(pwd)/PropertyManager
Icon=$(pwd)/app_icon.ico
Terminal=false
Categories=Office;
DESKTOP_EOF
    chmod +x "$DESKTOP_FILE"
    echo "✓ Desktop shortcut created"
fi

echo "✓ Installation completed!"
echo "Run ./PropertyManager to start the application"
EOF
    
    chmod +x "packages/$PACKAGE_NAME/install.sh"
    
    # Create tarball
    cd packages
    tar -czf "$PACKAGE_NAME.tar.gz" "$PACKAGE_NAME"
    cd ..
    
    print_success "Package created: packages/$PACKAGE_NAME.tar.gz"
    
    # Create simple ZIP for Windows compatibility
    if command -v zip &> /dev/null; then
        cd packages
        zip -r "$PACKAGE_NAME.zip" "$PACKAGE_NAME" > /dev/null
        cd ..
        print_success "ZIP package created: packages/$PACKAGE_NAME.zip"
    fi
    
else
    print_error "Build directory not found!"
    exit 1
fi

# Success message
print_header "SUCCESS! Complete build process finished!"

echo "🎉 Your distributable package is ready!"
echo
echo "📁 Files created:"
echo "   ✓ packages/$PACKAGE_NAME.tar.gz (Linux/macOS)"
if [[ -f "packages/$PACKAGE_NAME.zip" ]]; then
    echo "   ✓ packages/$PACKAGE_NAME.zip (Cross-platform)"
fi
echo "   ✓ installer_files/app/ (executable and support files)"
echo
echo "🚀 Distribution instructions:"
echo
echo "For Linux/macOS users:"
echo "   1. Extract the .tar.gz file"
echo "   2. Run: ./install.sh"
echo "   3. Start with: ./PropertyManager"
echo
echo "For manual installation:"
echo "   1. Copy the entire installer_files/app/ folder to target machines"
echo "   2. Make PropertyManager executable: chmod +x PropertyManager"
echo "   3. Run: ./PropertyManager"
echo
echo "📋 Next steps:"
echo "   1. Test the package on different systems"
echo "   2. Distribute the .tar.gz or .zip file to users"
echo "   3. Provide installation instructions"
echo

# Create a simple README for distribution
cat > "packages/DISTRIBUTION_README.md" << 'EOF'
# Property Management System - Distribution Package

## Installation Instructions

### Linux/macOS
1. Extract the package: `tar -xzf PropertyManagementSystem_*.tar.gz`
2. Navigate to the extracted folder: `cd PropertyManagementSystem_*`
3. Run the installation script: `./install.sh`
4. Start the application: `./PropertyManager`

### Manual Installation
1. Extract the package to your desired location
2. Make the main executable file executable: `chmod +x PropertyManager`
3. Run the application: `./PropertyManager`

## Requirements
- Linux or macOS system
- No additional dependencies required (all bundled)

## Features
- Desktop Property Management Application
- Airtable Integration (optional)
- Standalone executable (no Python installation required)

## Support
Please refer to the included documentation:
- USER_MANUAL.md
- AIRTABLE_INTEGRATION_GUIDE.md
EOF

print_success "Distribution README created"

echo "Build completed successfully! 🎉" 