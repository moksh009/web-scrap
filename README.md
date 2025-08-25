# Website Business Information Scraper

A Python application that scrapes business contact information from a list of websites and saves the results to a CSV file. Available in both **command-line** and **web interface** versions.

## 🌟 Features

- ✅ Extracts business names from title tags or domain names
- ✅ Finds email addresses using regex patterns
- ✅ Discovers Instagram profile URLs
- ✅ Extracts phone numbers in various formats (US and international)
- ✅ Handles errors gracefully and continues processing
- ✅ Saves results to a clean CSV file
- ✅ **NEW**: Beautiful web interface with real-time progress tracking
- ✅ **NEW**: Live scraping logs and progress updates
- ✅ **NEW**: Summary statistics and data visualization

## 🚀 Quick Start

### Option 1: Web Interface (Recommended)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the web server:**
   ```bash
   python run.py
   ```

3. **Open your browser:**
   Go to `http://localhost:5000`

4. **Use the interface:**
   - Paste your website URLs in the text area
   - Click "Start Scraping"
   - Watch real-time progress and logs
   - Download the CSV when complete

### Option 2: Command Line

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Edit the script:**
   Open `scraper.py` and add your URLs to the `websites` list

3. **Run the script:**
   ```bash
   python scraper.py
   ```

## 🎯 Web Interface Features

### ✨ Modern UI
- Beautiful gradient design with smooth animations
- Responsive layout that works on all devices
- Real-time progress bars and status updates

### 📊 Live Progress Tracking
- See which website is currently being scraped
- Progress bar showing completion percentage
- Real-time logs with color-coded messages

### 📋 Comprehensive Results
- Summary cards showing extracted data counts
- Detailed logs for each scraping operation
- Easy CSV download when complete

### 🛠️ User Controls
- Start/stop scraping at any time
- Clear logs and reset the interface
- Handle large lists of websites efficiently

## 📁 File Structure

```
website-extractor/
├── app.py              # Flask web application
├── scraper.py          # Core scraping logic
├── run.py              # Simple startup script
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   └── index.html     # Main web interface
├── websites.txt        # Sample URL list
└── README.md          # This file
```

## 🔧 Technical Details

### Web Application
- **Backend**: Flask + Flask-SocketIO
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Real-time**: WebSocket communication for live updates
- **Threading**: Background processing to keep UI responsive

### Scraping Engine
- **HTTP Client**: Requests with custom User-Agent
- **HTML Parser**: BeautifulSoup4 for content extraction
- **Pattern Matching**: Python regex for data extraction
- **Error Handling**: Graceful fallbacks for failed requests

### Data Extraction
- **Business Names**: Title tags, H1 tags, domain names
- **Emails**: Regex patterns + mailto: links
- **Instagram**: URL pattern matching for instagram.com
- **Phone Numbers**: Multiple format support (US + international)

## 📖 Usage Examples

### Web Interface
1. Open `http://localhost:5000` in your browser
2. Paste your website URLs (one per line):
   ```
   example.com
   business-website.org
   company-site.net
   ```
3. Click "Start Scraping"
4. Watch the progress in real-time
5. Download the CSV when complete

### Command Line
1. Edit `scraper.py` and add your URLs:
   ```python
   websites = [
       "your-website1.com",
       "your-website2.org",
       "your-website3.net"
   ]
   ```
2. Run: `python scraper.py`

## 🎨 Customization

### Adding New Data Fields
Edit the `extract_*` methods in `scraper.py` to add new extraction logic.

### Changing UI Styles
Modify the CSS in `templates/index.html` to customize the appearance.

### Adjusting Scraping Behavior
- Change delays between requests in `scraper.py`
- Modify regex patterns for better matching
- Add new data extraction methods

## 🚨 Error Handling

The application handles various errors gracefully:
- **Network Issues**: Continues with next website
- **Invalid URLs**: Skips and logs errors
- **Missing Data**: Shows "N/A" in results
- **Server Errors**: Graceful fallbacks

## 📊 Output Format

The CSV file contains these columns:
- **Business Name**: Extracted business name
- **Website**: Original URL
- **Email**: Found email addresses
- **Instagram**: Instagram profile URLs
- **Phone**: Phone numbers in various formats

## 🔒 Security & Best Practices

- Uses realistic User-Agent headers
- Includes delays between requests
- Handles rate limiting gracefully
- No external API dependencies
- Local processing only

## 🐛 Troubleshooting

### Common Issues
- **Import errors**: Run `pip install -r requirements.txt`
- **Port conflicts**: Change port in `app.py` if 5000 is busy
- **No data extracted**: Some sites may use JavaScript or anti-scraping measures
- **Slow performance**: Built-in delays respect server resources

### Getting Help
1. Check the console output for error messages
2. Verify all dependencies are installed
3. Ensure websites are accessible from your network
4. Check firewall/antivirus settings

## 📝 Legal Notice

**Important**: Please ensure you have permission to scrape the websites you're targeting. Some websites may have terms of service that prohibit scraping. This tool is for educational and legitimate business purposes only.

## 🤝 Contributing

Feel free to:
- Report bugs or issues
- Suggest new features
- Improve the UI/UX
- Add new data extraction methods
- Optimize performance

## 📄 License

This project is open source and available under the MIT License.
# web-scrap
