#!/usr/bin/env python3
"""
Website Business Information Scraper
Scrapes business contact information from a list of websites and saves to CSV.
"""

import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import csv

class BusinessScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def extract_business_name(self, soup, url):
        """Extract business name from title tag or other sources"""
        # Try to get from title tag first
        title_tag = soup.find('title')
        if title_tag and title_tag.text.strip():
            title = title_tag.text.strip()
            # Clean up common title suffixes
            title = re.sub(r'\s*[-|]\s*(Home|Welcome|Official Site|Website).*$', '', title, flags=re.IGNORECASE)
            return title if title else "N/A"
        
        # Try to get from h1 tag
        h1_tag = soup.find('h1')
        if h1_tag and h1_tag.text.strip():
            return h1_tag.text.strip()
        
        # Try to get from domain name
        domain = urlparse(url).netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain.replace('.com', '').replace('.org', '').replace('.net', '').title()
    
    def extract_email(self, soup, url):
        """Extract email addresses using regex"""
        # Look for emails in text content
        text_content = soup.get_text()
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text_content)
        
        # Also look for emails in href attributes
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('mailto:'):
                email = href.replace('mailto:', '').split('?')[0]
                if email not in emails:
                    emails.append(email)
        
        # Return first valid email found
        for email in emails:
            if '@' in email and '.' in email.split('@')[1]:
                return email
        
        return "N/A"
    
    def extract_instagram(self, soup, url):
        """Extract Instagram profile URLs"""
        instagram_patterns = [
            r'https?://(?:www\.)?instagram\.com/[A-Za-z0-9._]+/?',
            r'https?://instagram\.com/[A-Za-z0-9._]+/?'
        ]
        
        # Look for Instagram links in href attributes
        for link in soup.find_all('a', href=True):
            href = link['href']
            for pattern in instagram_patterns:
                match = re.search(pattern, href)
                if match:
                    return match.group(0)
        
        # Look for Instagram URLs in text content
        text_content = soup.get_text()
        for pattern in instagram_patterns:
            match = re.search(pattern, text_content)
            if match:
                return match.group(0)
        
        return "N/A"
    
    def extract_phone(self, soup, url):
        """Extract phone numbers using regex"""
        # Common phone number patterns
        phone_patterns = [
            r'\+?1?\s*\(?[0-9]{3}\)?[\s.-]?[0-9]{3}[\s.-]?[0-9]{4}',  # US format
            r'\+?[0-9]{1,4}[\s.-]?[0-9]{1,4}[\s.-]?[0-9]{1,4}[\s.-]?[0-9]{1,4}',  # International
            r'\([0-9]{3}\)\s*[0-9]{3}-[0-9]{4}',  # (123) 456-7890
            r'[0-9]{3}-[0-9]{3}-[0-9]{4}',  # 123-456-7890
            r'[0-9]{3}\s[0-9]{3}\s[0-9]{4}',  # 123 456 7890
        ]
        
        text_content = soup.get_text()
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, text_content)
            if matches:
                # Return first valid phone number
                phone = matches[0].strip()
                # Clean up the phone number
                phone = re.sub(r'\s+', ' ', phone)
                return phone
        
        return "N/A"
    
    def scrape_website(self, url):
        """Scrape a single website for business information"""
        try:
            print(f"🔍 Scraping: {url}")
            
            # Add http:// if no protocol specified
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            business_name = self.extract_business_name(soup, url)
            email = self.extract_email(soup, url)
            instagram = self.extract_instagram(soup, url)
            phone = self.extract_phone(soup, url)
            
            print(f"   ✅ Found: {business_name}")
            
            return {
                'Business Name': business_name,
                'Website': url,
                'Email': email,
                'Instagram': instagram,
                'Phone': phone
            }
            
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error loading {url}: {str(e)}")
            return {
                'Business Name': 'N/A',
                'Website': url,
                'Email': 'N/A',
                'Instagram': 'N/A',
                'Phone': 'N/A'
            }
        except Exception as e:
            print(f"   ❌ Unexpected error with {url}: {str(e)}")
            return {
                'Business Name': 'N/A',
                'Website': url,
                'Email': 'N/A',
                'Instagram': 'N/A',
                'Phone': 'N/A'
            }
    
    def scrape_websites(self, urls):
        """Scrape multiple websites and return results"""
        results = []
        total_urls = len(urls)
        
        print(f"🚀 Starting to scrape {total_urls} websites...")
        print("=" * 50)
        
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{total_urls}] ", end="")
            result = self.scrape_website(url.strip())
            results.append(result)
            
            # Small delay to be respectful to servers
            if i < total_urls:
                time.sleep(1)
        
        return results
    
    def save_to_csv(self, data, filename='business_info.csv'):
        """Save scraped data to CSV file"""
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"\n💾 Data saved to {filename}")
        print(f"📊 Total records: {len(data)}")
        
        # Display summary
        print("\n📋 Summary:")
        print(f"   • Websites with business names: {len([r for r in data if r['Business Name'] != 'N/A'])}")
        print(f"   • Websites with emails: {len([r for r in data if r['Email'] != 'N/A'])}")
        print(f"   • Websites with Instagram: {len([r for r in data if r['Instagram'] != 'N/A'])}")
        print(f"   • Websites with phone numbers: {len([r for r in data if r['Phone'] != 'N/A'])}")

def main():
    """Main function to run the scraper"""
    print("🌐 Website Business Information Scraper")
    print("=" * 50)
    
    # List of websites to scrape - ADD YOUR WEBSITES HERE
    websites = [
        # Example websites (replace with your actual list)
        "example.com",
        "business-website.org",
        "company-site.net"
    ]
    
    # Alternative: Load from a text file
    # with open('websites.txt', 'r') as f:
    #     websites = [line.strip() for line in f if line.strip()]
    
    if not websites:
        print("❌ No websites provided. Please add websites to the script or create a websites.txt file.")
        return
    
    # Create scraper instance
    scraper = BusinessScraper()
    
    # Scrape all websites
    results = scraper.scrape_websites(websites)
    
    # Save results to CSV
    scraper.save_to_csv(results)
    
    print("\n" + "=" * 50)
    print("✅ Scraping complete! Data saved to business_info.csv")
    
    # Show first few results
    if results:
        print("\n📋 First few results:")
        df = pd.DataFrame(results)
        print(df.head().to_string(index=False))

if __name__ == "__main__":
    main()
