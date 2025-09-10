"""
Deployment script for Kiosk Scanner Application
Installs and configures the app as a Windows service
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path
import winreg

def copy_dlls():
    """Copy scanner DLLs to the app directory"""
    print("📦 Setting up scanner DLLs...")
    
    dll_dir = Path("dlls")
    dll_dir.mkdir(exist_ok=True)
    
    # You'll need to copy your DLLs here manually or from the backend project
    print("⚠️  Please copy the following DLLs to the 'dlls' directory:")
    print("   - dpfpdd.dll")
    print("   - dpfj.dll")
    print("   (Copy from your backend/core directory)")
    
    return dll_dir

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_batch_file():
    """Create batch file to run the application"""
    print("📝 Creating startup batch file...")
    
    batch_content = f"""@echo off
cd /d "{Path.cwd()}"
"{sys.executable}" app.py
pause
"""
    
    batch_path = Path("start_kiosk_scanner.bat")
    with open(batch_path, 'w') as f:
        f.write(batch_content)
    
    print(f"✅ Batch file created: {batch_path}")
    return batch_path

def add_to_startup():
    """Add application to Windows startup"""
    print("🔧 Adding to Windows startup...")
    
    try:
        batch_path = create_batch_file()
        
        # Add to Windows registry for auto-start
        reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE)
        
        startup_cmd = str(batch_path.absolute())
        winreg.SetValueEx(reg_key, "KioskScannerAPI", 0, winreg.REG_SZ, startup_cmd)
        winreg.CloseKey(reg_key)
        
        print("✅ Added to Windows startup")
        return True
        
    except Exception as e:
        print(f"❌ Failed to add to startup: {e}")
        return False

def create_desktop_shortcut():
    """Create desktop shortcut"""
    print("🖥️ Creating desktop shortcut...")
    
    try:
        import win32com.client
        
        desktop = Path.home() / "Desktop"
        shortcut_path = desktop / "Kiosk Scanner API.lnk"
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.Targetpath = str(Path("start_kiosk_scanner.bat").absolute())
        shortcut.WorkingDirectory = str(Path.cwd())
        shortcut.IconLocation = sys.executable
        shortcut.save()
        
        print(f"✅ Desktop shortcut created: {shortcut_path}")
        return True
        
    except ImportError:
        print("⚠️  pywin32 not available, skipping desktop shortcut")
        return False
    except Exception as e:
        print(f"❌ Shortcut creation failed: {e}")
        return False

def test_installation():
    """Test the installation"""
    print("🧪 Testing installation...")
    
    try:
        # Test import
        from scanner import FingerprintScanner
        from app import app
        
        print("✅ Application imports successful")
        
        # Test Flask app creation
        with app.test_client() as client:
            response = client.get('/api/health')
            if response.status_code == 200:
                print("✅ API health check successful")
                return True
            else:
                print(f"❌ API health check failed: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False

def main():
    """Main deployment function"""
    print("🚀 Kiosk Scanner Application Deployment")
    print("=" * 50)
    
    if os.name != 'nt':
        print("❌ This application is for Windows only")
        sys.exit(1)
    
    # Step 1: Install dependencies
    if not install_dependencies():
        print("❌ Deployment failed at dependency installation")
        sys.exit(1)
    
    # Step 2: Setup DLLs
    copy_dlls()
    
    # Step 3: Test installation
    if not test_installation():
        print("⚠️  Installation test failed, but continuing...")
    
    # Step 4: Deployment options
    print("\nChoose deployment option:")
    print("1. Add to Windows startup (recommended)")
    print("2. Desktop shortcut only")
    print("3. Manual setup only")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        add_to_startup()
        create_desktop_shortcut()
    elif choice == "2":
        create_desktop_shortcut()
    elif choice == "3":
        create_batch_file()
    else:
        print("❌ Invalid choice")
        sys.exit(1)
    
    print("\n🎉 Deployment completed!")
    print("\n📋 Next Steps:")
    print("1. Copy your scanner DLLs to the 'dlls' directory")
    print("2. Edit config.py to set your cloud API URL")
    print("3. Test the application by running: python app.py")
    print("4. The API will be available at: http://localhost:8000")
    print("\n💡 Frontend Integration:")
    print("Configure your Vercel frontend to use:")
    print("- Local API: http://localhost:8000/api")
    print("- Cloud API: https://your-railway-app.railway.app/api")

if __name__ == "__main__":
    main()
