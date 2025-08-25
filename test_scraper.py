#!/usr/bin/env python3
"""
Test script to verify the WebScraper class works correctly
"""

import sys
import os

# Add current directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_webscraper():
    """Test the WebScraper class"""
    try:
        print("🧪 Testing WebScraper class...")
        
        # Import the WebScraper class
        from app import WebScraper
        
        print("✅ WebScraper class imported successfully")
        
        # Create a mock socketio object
        class MockSocketIO:
            def emit(self, event, data):
                print(f"📡 Socket.IO event: {event} - {data}")
        
        # Create WebScraper instance
        scraper = WebScraper(MockSocketIO())
        print("✅ WebScraper instance created successfully")
        
        # Test a simple website
        test_url = "httpbin.org"
        print(f"🔍 Testing with URL: {test_url}")
        
        # Test the scrape_website method
        result = scraper.scrape_website(test_url)
        print(f"✅ Scraping result: {result}")
        
        # Verify the result structure
        required_keys = ['Business Name', 'Website', 'Email', 'Instagram', 'Phone']
        for key in required_keys:
            if key in result:
                print(f"✅ Found key: {key} = {result[key]}")
            else:
                print(f"❌ Missing key: {key}")
        
        print("\n🎉 All tests passed! WebScraper is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_webscraper()
    sys.exit(0 if success else 1)
