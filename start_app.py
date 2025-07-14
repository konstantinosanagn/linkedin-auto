#!/usr/bin/env python3
"""
Startup script for LinkedIn Automation System
Runs both the backend API and frontend development server
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

def run_backend():
    """Run the Flask backend API"""
    print("🚀 Starting backend API server...")
    try:
        subprocess.run([sys.executable, "api.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
    except Exception as e:
        print(f"❌ Backend error: {e}")

def run_frontend():
    """Run the React frontend development server"""
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found. Please run 'npm install' in the frontend directory first.")
        return
    
    print("🎨 Starting frontend development server...")
    try:
        # Change to frontend directory and start npm
        os.chdir(frontend_dir)
        subprocess.run(["npm", "start"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
    except FileNotFoundError:
        print("❌ npm not found. Please install Node.js and npm first.")
    except Exception as e:
        print(f"❌ Frontend error: {e}")

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python dependencies
    try:
        import flask
        import flask_cors
        print("✅ Python dependencies OK")
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    # Check Node.js and npm
    try:
        result = subprocess.run(["node", "--version"], check=True, capture_output=True, text=True)
        result = subprocess.run(["npm", "--version"], check=True, capture_output=True, text=True)
        print("✅ Node.js and npm OK")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"❌ Node.js or npm not found: {e}")
        print("Please install Node.js first.")
        return False
    
    # Check frontend dependencies
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    node_modules = frontend_dir / "node_modules"
    if not node_modules.exists():
        print("❌ Frontend dependencies not installed")
        print("Please run: cd frontend && npm install")
        return False
    
    print("✅ Frontend dependencies OK")
    return True

def main():
    """Main startup function"""
    print("=" * 50)
    print("🔗 LinkedIn Automation System")
    print("=" * 50)
    
    if not check_dependencies():
        print("\n❌ Dependencies check failed. Please fix the issues above.")
        sys.exit(1)
    
    print("\n✅ All dependencies OK!")
    print("\n📋 Starting services...")
    print("   Backend API: http://localhost:5000")
    print("   Frontend UI: http://localhost:3000")
    print("\nPress Ctrl+C to stop all services")
    print("-" * 50)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Give backend time to start
    time.sleep(2)
    
    # Start frontend in main thread
    try:
        run_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
    finally:
        print("👋 Goodbye!")

if __name__ == "__main__":
    main() 