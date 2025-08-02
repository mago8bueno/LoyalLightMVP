#!/usr/bin/env python3
"""
Local development server launcher for LoyalLight MVP.
"""
import os
import sys
import subprocess
import time
from pathlib import Path


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import uvicorn
        import fastapi
        import motor
        print("✓ Backend dependencies found")
    except ImportError as e:
        print(f"✗ Missing backend dependency: {e}")
        print("Installing backend dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"])


def setup_environment():
    """Setup environment variables."""
    env_file = Path("backend/.env")
    env_example = Path("backend/.env.example")
    
    if not env_file.exists() and env_example.exists():
        print("Creating .env file from .env.example...")
        with open(env_example) as f:
            content = f.read()
        
        # Set default values for local development
        content = content.replace("OPENAI_API_KEY=", f"OPENAI_API_KEY={os.getenv('OPENAI_API_KEY', '')}")
        content = content.replace("DEBUG=false", "DEBUG=true")
        
        with open(env_file, "w") as f:
            f.write(content)
        
        print("✓ Environment file created")


def start_backend():
    """Start the backend server."""
    print("Starting backend server...")
    backend_dir = Path("backend")
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Start uvicorn server
    cmd = [
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", "8001",
        "--reload"
    ]
    
    return subprocess.Popen(cmd)


def main():
    """Main function to start the local development environment."""
    print("🚀 Starting LoyalLight MVP Local Development Server")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("backend").exists():
        print("✗ Error: backend directory not found")
        print("Please run this script from the LoyalLight project root directory")
        sys.exit(1)
    
    # Check dependencies
    check_dependencies()
    
    # Setup environment
    setup_environment()
    
    # Start backend
    backend_process = start_backend()
    
    print("\n" + "=" * 50)
    print("🎉 LoyalLight MVP is now running!")
    print("=" * 50)
    print("Backend API: http://localhost:8001")
    print("API Documentation: http://localhost:8001/api/docs")
    print("Health Check: http://localhost:8001/api/health")
    print("\nDefault Users:")
    print("- admin / Admin2024!Secure")
    print("- cliente1 / Client1@2024")
    print("- cliente2 / Client2@2024")
    print("- ... (cliente3-cliente10)")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Wait for backend process
        backend_process.wait()
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping servers...")
        backend_process.terminate()
        backend_process.wait()
        print("✓ Servers stopped")


if __name__ == "__main__":
    main()

