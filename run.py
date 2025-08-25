#!/usr/bin/env python3
"""
Simple startup script for the Website Scraper Web App
"""

import os
import sys

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import flask
        import flask_socketio
        import requests
        import bs4
        import pandas
        print("✅ All required packages are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def main():
    """Main startup function"""
    print("🌐 Website Business Information Scraper")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("🚀 Starting Flask web server...")
    print("📱 Open your browser and go to: http://localhost:5001")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Import and run the app
    try:
        from app import app, socketio
        socketio.run(app, host='0.0.0.0', port=5001, debug=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
