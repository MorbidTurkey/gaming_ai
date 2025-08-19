"""
Startup script for Gaming AI Chatbot

This script helps set up the environment and start the application.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'dash', 'plotly', 'openai', 'requests', 
        'pandas', 'numpy', 'python-dotenv', 'dash-bootstrap-components'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            # Special case for python-dotenv which imports as 'dotenv'
            if package == 'python-dotenv':
                __import__('dotenv')
            else:
                __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - Missing")
    
    return missing_packages

def install_dependencies():
    """Install missing dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("⚠️  .env file not found")
        print("   Creating .env from template...")
        
        # Copy from .env.example
        example_path = Path(".env.example")
        if example_path.exists():
            with open(example_path) as f:
                content = f.read()
            
            with open(env_path, 'w') as f:
                f.write(content)
            
            print("✅ .env file created from template")
            print("⚠️  Please edit .env and add your API keys:")
            print("   - OPENAI_API_KEY (required for AI responses)")
            print("   - STEAM_API_KEY (optional, for enhanced Steam data)")
        else:
            print("❌ .env.example not found")
            return False
    else:
        print("✅ .env file exists")
    
    return True

def start_application():
    """Start the Dash application"""
    print("\n🚀 Starting Gaming AI Chatbot...")
    print("   Access the app at: http://localhost:8050")
    print("   Press Ctrl+C to stop the server\n")
    
    try:
        # Import and run the app
        from app import app
        app.run(debug=True, port=8050, host='127.0.0.1')
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("   Make sure all dependencies are installed and .env is configured")

def main():
    """Main setup and startup function"""
    print("🎮 Gaming AI Chatbot - Setup & Startup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check dependencies
    print("\n📋 Checking dependencies...")
    missing = check_dependencies()
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        install_deps = input("Install missing dependencies? (y/n): ").lower().strip()
        
        if install_deps in ['y', 'yes']:
            if not install_dependencies():
                return
        else:
            print("❌ Cannot start without required dependencies")
            return
    
    # Check environment file
    print("\n🔧 Checking environment configuration...")
    if not check_env_file():
        return
    
    # Start the application
    start_application()

if __name__ == "__main__":
    main()
