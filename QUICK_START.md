# 🚀 Quick Start Guide

## 🌐 Website Business Information Scraper - Web Interface

### ⚡ Get Started in 3 Steps:

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Web Server:**
   ```bash
   python run.py
   ```

3. **Open Your Browser:**
   Go to: `http://localhost:5000`

### 🎯 How to Use:

1. **Paste Your Website URLs** in the text area (one per line)
2. **Click "Start Scraping"** to begin
3. **Watch Real-Time Progress** with live logs and progress bars
4. **Download CSV** when complete

### 📋 Example URLs to Test:
```
example.com
httpbin.org
business-website.org
```

### 🎨 Features:
- ✅ **Beautiful Modern UI** with gradient design
- ✅ **Real-Time Progress** tracking and live logs
- ✅ **Live Updates** via WebSocket
- ✅ **Progress Bars** showing completion percentage
- ✅ **Color-Coded Logs** for different message types
- ✅ **Summary Statistics** with data counts
- ✅ **Responsive Design** works on all devices
- ✅ **Start/Stop Controls** for long scraping jobs
- ✅ **CSV Download** when scraping completes

### 🔧 Technical Details:
- **Backend**: Flask + Flask-SocketIO
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Real-time**: WebSocket communication
- **Threading**: Background processing
- **Error Handling**: Graceful fallbacks

### 📁 Files Created:
- `business_info.csv` - Your scraped data
- `app.py` - Flask web application
- `scraper.py` - Core scraping engine
- `templates/index.html` - Beautiful web interface

### 🚨 Troubleshooting:
- **Port 5000 busy**: Change port in `app.py`
- **Import errors**: Run `pip install -r requirements.txt`
- **No data**: Some sites may block scraping

### 💡 Pro Tips:
- Use realistic delays between requests
- Handle errors gracefully
- Monitor progress in real-time
- Download CSV when complete

---

**Ready to scrape? Run `python run.py` and open `http://localhost:5000`! 🎉**
