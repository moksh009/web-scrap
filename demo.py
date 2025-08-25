#!/usr/bin/env python3
"""
Demo script to show how the website scraper works
"""

from scraper import BusinessScraper

def demo_scraping():
    """Demonstrate the scraping functionality"""
    print("🌐 Website Business Information Scraper - Demo")
    print("=" * 60)
    
    # Example websites for demonstration
    demo_websites = [
        "httpbin.org",  # Simple test site
        "example.com",  # Basic example site
        "httpstat.us/200"  # HTTP status test
    ]
    
    print(f"📋 Demo websites: {', '.join(demo_websites)}")
    print("\n🚀 Starting demo scraping...")
    print("-" * 60)
    
    # Create scraper instance
    scraper = BusinessScraper()
    
    # Scrape each website
    results = []
    for i, url in enumerate(demo_websites, 1):
        print(f"\n[{i}/{len(demo_websites)}] Scraping: {url}")
        try:
            result = scraper.scrape_website(url)
            results.append(result)
            
            # Show what was found
            print(f"   ✅ Business Name: {result['Business Name']}")
            print(f"   📧 Email: {result['Email']}")
            print(f"   📱 Instagram: {result['Instagram']}")
            print(f"   📞 Phone: {result['Phone']}")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            results.append({
                'Business Name': 'N/A',
                'Website': url,
                'Email': 'N/A',
                'Instagram': 'N/A',
                'Phone': 'N/A'
            })
    
    # Show summary
    print("\n" + "=" * 60)
    print("📊 Demo Results Summary:")
    print(f"   • Total websites: {len(results)}")
    print(f"   • With business names: {len([r for r in results if r['Business Name'] != 'N/A'])}")
    print(f"   • With emails: {len([r for r in results if r['Email'] != 'N/A'])}")
    print(f"   • With Instagram: {len([r for r in results if r['Instagram'] != 'N/A'])}")
    print(f"   • With phone numbers: {len([r for r in results if r['Phone'] != 'N/A'])}")
    
    print("\n💡 This is just a demo with test websites.")
    print("💡 For real scraping, use the web interface: python run.py")
    print("💡 Or edit scraper.py with your actual website URLs.")

if __name__ == "__main__":
    demo_scraping()
