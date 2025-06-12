#!/usr/bin/env python3
"""
Convert PNG logo to ICO format for Windows installer
"""

try:
    from PIL import Image
    import os
    
    def create_icon_from_logo():
        """Convert PNG logo to ICO format with multiple sizes"""
        
        if not os.path.exists('app_logo.png'):
            print("❌ app_logo.png not found!")
            return False
        
        try:
            # Open the PNG logo
            with Image.open('app_logo.png') as img:
                print(f"📸 Original logo size: {img.size}")
                
                # Convert to RGBA if not already
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                # Create different sizes for the ICO file
                # Windows ICO files typically contain multiple sizes
                sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
                
                # Resize and save as ICO with multiple sizes
                img.save('app_icon.ico', format='ICO', sizes=sizes)
                print("✅ Created app_icon.ico with multiple sizes")
                
                # Also create a smaller version for the installer wizard
                wizard_img = img.resize((55, 58), Image.Resampling.LANCZOS)
                wizard_img.save('wizard_small.bmp', format='BMP')
                print("✅ Created wizard_small.bmp (55×58)")
                
                # Create a larger wizard image
                wizard_large = img.resize((164, 314), Image.Resampling.LANCZOS)
                wizard_large.save('wizard_image.bmp', format='BMP')
                print("✅ Created wizard_image.bmp (164×314)")
                
                return True
                
        except Exception as e:
            print(f"❌ Error processing image: {str(e)}")
            return False
    
    if __name__ == "__main__":
        print("🎨 Creating Windows icon from logo...")
        if create_icon_from_logo():
            print("🎉 Icon creation successful!")
        else:
            print("💔 Icon creation failed!")
            
except ImportError:
    print("❌ PIL (Pillow) not installed. Installing...")
    import subprocess
    import sys
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Pillow'])
        print("✅ Pillow installed successfully!")
        print("🔄 Please run this script again.")
    except:
        print("❌ Failed to install Pillow automatically.")
        print("Please run: pip install Pillow") 