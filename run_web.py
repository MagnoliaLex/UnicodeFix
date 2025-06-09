#!/usr/bin/env python3

"""
UnicodeFix Web Application Launcher

Simple launcher script that starts the FastAPI web server.
This script can be run directly or used with the batch/PowerShell launchers.
"""

import sys
import webbrowser
from pathlib import Path
import time
import threading

def open_browser():
    """Open the web browser after a short delay."""
    time.sleep(2)  # Give the server time to start
    webbrowser.open('http://localhost:8000')

def main():
    """Main function to start the web application."""
    print("🚀 UnicodeFix Web Interface")
    print("=" * 40)
    
    # Check if we can import the required modules
    try:
        import uvicorn
        from fastapi import FastAPI
    except ImportError as e:
        print(f"❌ Missing required dependencies: {e}")
        print("\n💡 Please install dependencies:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Start browser in background thread
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    print("\n📱 Starting web server...")
    print("🌐 Access URL: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("\n⏹️  Press Ctrl+C to stop the server")
    print("-" * 40)
    
    try:
        # Import and run the web app
        from web_app import app
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            access_log=False  # Reduce log verbosity
        )
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down UnicodeFix Web Interface")
        print("Thank you for using UnicodeFix!")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 