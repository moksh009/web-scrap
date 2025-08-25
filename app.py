#!/usr/bin/env python3
"""
Flask Web Application for Website Business Information Scraper
Provides a web UI for scraping websites and downloading results as CSV.
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, emit
import os
import json
import threading
import time
from datetime import datetime
import pandas as pd
from scraper import BusinessScraper
import io
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables to store scraping state
scraping_status = {
    'is_running': False,
    'current_url': '',
    'progress': 0,
    'total_urls': 0,
    'completed': 0,
    'results': [],
    'errors': []
}

class WebScraper(BusinessScraper):
    """Extended scraper class with web socket support"""
    
    def __init__(self, socketio):
        super().__init__()
        self.socketio = socketio
        
    def emit_progress(self, message, progress_type='info'):
        """Emit progress updates to the web client"""
        self.socketio.emit('scraping_update', {
            'message': message,
            'type': progress_type,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })
    
    def scrape_website(self, url):
        """Override to add progress updates"""
        try:
            self.emit_progress(f"🔍 Scraping: {url}", 'scraping')
            
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
            
            result = {
                'Business Name': business_name,
                'Website': url,
                'Email': email,
                'Instagram': instagram,
                'Phone': phone
            }
            
            self.emit_progress(f"✅ Found: {business_name}", 'success')
            return result
            
        except requests.exceptions.RequestException as e:
            error_msg = f"❌ Error loading {url}: {str(e)}"
            self.emit_progress(error_msg, 'error')
            return {
                'Business Name': 'N/A',
                'Website': url,
                'Email': 'N/A',
                'Instagram': 'N/A',
                'Phone': 'N/A'
            }
        except Exception as e:
            error_msg = f"❌ Unexpected error with {url}: {str(e)}"
            self.emit_progress(error_msg, 'error')
            return {
                'Business Name': 'N/A',
                'Website': url,
                'Email': 'N/A',
                'Instagram': 'N/A',
                'Phone': 'N/A'
            }
    
    def scrape_websites(self, urls):
        """Override to add progress tracking"""
        results = []
        total_urls = len(urls)
        
        self.emit_progress(f"🚀 Starting to scrape {total_urls} websites...", 'start')
        
        for i, url in enumerate(urls, 1):
            if not scraping_status['is_running']:
                self.emit_progress("⏹️ Scraping stopped by user", 'warning')
                break
                
            url = url.strip()
            if not url:
                continue
                
            # Update progress
            progress = (i / total_urls) * 100
            self.socketio.emit('progress_update', {
                'current': i,
                'total': total_urls,
                'percentage': round(progress, 1),
                'current_url': url
            })
            
            result = self.scrape_website(url)
            results.append(result)
            
            # Small delay to be respectful to servers
            if i < total_urls and scraping_status['is_running']:
                time.sleep(1)
        
        return results

def start_scraping_thread(urls):
    """Start scraping in a separate thread"""
    global scraping_status
    
    scraping_status['is_running'] = True
    scraping_status['results'] = []
    scraping_status['errors'] = []
    scraping_status['completed'] = 0
    scraping_status['total_urls'] = len(urls)
    
    try:
        scraper = WebScraper(socketio)
        results = scraper.scrape_websites(urls)
        scraping_status['results'] = results
        
        # Save to CSV
        if results:
            df = pd.DataFrame(results)
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False, encoding='utf-8')
            csv_buffer.seek(0)
            
            # Save to file
            with open('business_info.csv', 'w', encoding='utf-8') as f:
                f.write(csv_buffer.getvalue())
            
            # Send completion message
            socketio.emit('scraping_complete', {
                'message': f"✅ Scraping complete! Found data for {len(results)} websites.",
                'total_results': len(results),
                'csv_ready': True
            })
            
            # Show summary
            summary = {
                'business_names': len([r for r in results if r['Business Name'] != 'N/A']),
                'emails': len([r for r in results if r['Email'] != 'N/A']),
                'instagram': len([r for r in results if r['Instagram'] != 'N/A']),
                'phones': len([r for r in results if r['Phone'] != 'N/A'])
            }
            socketio.emit('summary_update', summary)
            
    except Exception as e:
        socketio.emit('scraping_error', {
            'message': f"❌ Scraping failed: {str(e)}",
            'type': 'error'
        })
    finally:
        scraping_status['is_running'] = False

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/start_scraping', methods=['POST'])
def start_scraping():
    """Start the scraping process"""
    try:
        data = request.get_json()
        urls_text = data.get('urls', '')
        
        if not urls_text.strip():
            return jsonify({'error': 'No URLs provided'}), 400
        
        # Parse URLs (split by newlines and filter empty lines)
        urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
        
        if not urls:
            return jsonify({'error': 'No valid URLs found'}), 400
        
        # Check if scraping is already running
        if scraping_status['is_running']:
            return jsonify({'error': 'Scraping is already in progress'}), 400
        
        # Start scraping in background thread
        thread = threading.Thread(target=start_scraping_thread, args=(urls,))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'message': f'Started scraping {len(urls)} websites',
            'total_urls': len(urls)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stop_scraping', methods=['POST'])
def stop_scraping():
    """Stop the scraping process"""
    global scraping_status
    scraping_status['is_running'] = False
    return jsonify({'message': 'Scraping stopped'})

@app.route('/download_csv')
def download_csv():
    """Download the CSV file"""
    try:
        if not os.path.exists('business_info.csv'):
            return jsonify({'error': 'CSV file not found'}), 404
        
        return send_file(
            'business_info.csv',
            as_attachment=True,
            download_name='business_info.csv',
            mimetype='text/csv'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_status')
def get_status():
    """Get current scraping status"""
    return jsonify(scraping_status)

if __name__ == '__main__':
    print("🌐 Website Scraper Web App")
    print("=" * 40)
    print("Starting Flask server...")
    
    # Get port from environment variable (for Render) or use default
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"Open your browser and go to: http://localhost:{port}")
    print("=" * 40)
    
    socketio.run(app, host='0.0.0.0', port=port, debug=debug)
