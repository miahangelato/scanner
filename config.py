"""
Configuration for Kiosk Scanner Application
"""
import os

# Server Configuration
HOST = '0.0.0.0'  # Allow connections from any IP on local network
PORT = 5000  # Changed from 8000 to avoid conflict with Django backend
DEBUG = True

# CORS Configuration - Allow frontend to connect
CORS_ORIGINS = [
    "http://localhost:3000",  # Local development
    "http://localhost:3001", 
    "https://*.vercel.app",   # Your Vercel deployment
    "https://your-app.vercel.app",  # Replace with your actual Vercel domain
    "https://your-thesis-app.vercel.app",  # Add your actual domain here
]

# Allow all origins for kiosk simplicity 
# Tailscale provides network-level security, so this is safer
CORS_ALLOW_ALL = True

# Cloud Backend Configuration
CLOUD_API_URL = "https://your-railway-app.railway.app/api"  # Replace with your Railway URL

# Scanner Configuration
SCANNER_TIMEOUT = 30  # seconds
SCANNER_RETRY_ATTEMPTS = 3

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = "kiosk_scanner.log"
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5

# Security (simple for local kiosk use)
API_KEY = "kiosk-scanner-2025"  # Optional API key for requests

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SDK_DIR = os.path.join(BASE_DIR, "sdk")

# Scanner SDK paths - using the installed SDK
SDK_INSTALLED_PATH = r"C:\Program Files\DigitalPersona\U.are.U SDK\Windows\Lib"
SCANNER_DLLS = {
    "dpfpdd": os.path.join(SDK_INSTALLED_PATH, "x64", "dpfpdd.dll"),
    "dpfj": os.path.join(SDK_INSTALLED_PATH, "x64", "dpfj.dll")
}

# Fallback paths in case system installation fails
SCANNER_DLLS_FALLBACK = {
    "dpfpdd": os.path.join(SDK_DIR, "x64", "dpfpdd.dll"),
    "dpfj": os.path.join(SDK_DIR, "x64", "dpfj.dll")
}

# SDK Installation paths (for runtime)
SDK_RTE_X64 = os.path.join(SDK_DIR, "RTE", "x64")
SDK_RTE_X86 = os.path.join(SDK_DIR, "RTE", "x86")
