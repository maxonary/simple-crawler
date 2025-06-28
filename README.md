# Simple Web Crawler

A lightweight web crawler with a beautiful Streamlit frontend that allows you to crawl multiple URLs and get full page contents.

## Features

- 🕷️ **Simple URL Input**: Enter single URLs or multiple URLs at once
- 📄 **Full Page Contents**: Get complete HTML/text content from each page
- 📊 **Response Details**: View status codes, content types, and encoding information
- 📥 **Export Results**: Download crawl results as JSON or individual HTML files
- 🎨 **Beautiful UI**: Modern Streamlit interface with real-time statistics
- ⚡ **Fast & Efficient**: Built with requests for optimal performance

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd simple-crawler
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the application:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** and navigate to the URL shown in the terminal (usually `http://localhost:8501`)

3. **Enter URLs** to crawl:
   - **Single URL**: Enter one URL at a time
   - **Multiple URLs**: Enter multiple URLs, one per line
   - URLs without protocols (e.g., `example.com`) will automatically use `https://`

4. **Click "Start Crawling"** to begin the crawl process

5. **View results** in the expandable sections below

6. **Download content** as individual HTML files or export all results as JSON

## What the Crawler Returns

For each successfully crawled URL, you'll get:

- **Full Page Content**: Complete HTML/text content of the page
- **Response Status**: HTTP status code
- **Content Type**: MIME type of the response
- **Encoding**: Character encoding used
- **Content Length**: Total number of characters
- **Error Information**: Detailed error messages for failed crawls

## Example Usage

### Input URLs:
```
example.com
https://google.com
https://github.com
```

### Sample Output:
```json
{
  "url": "https://example.com",
  "status_code": 200,
  "content": "<!DOCTYPE html><html><head><title>Example Domain</title>...</html>",
  "content_type": "text/html; charset=UTF-8",
  "encoding": "UTF-8",
  "content_length": 1234,
  "success": true
}
```

## Technical Details

- **Backend**: Python with requests library
- **Frontend**: Streamlit for the web interface
- **Content Handling**: Raw HTML/text content without parsing
- **Rate Limiting**: 1-second delay between requests to be respectful to servers

## Important Notes

⚠️ **Please be respectful when crawling websites:**
- Check the website's `robots.txt` file
- Don't overwhelm servers with too many requests
- Consider the website's terms of service
- The crawler includes a 1-second delay between requests by default

## Requirements

- Python 3.7+
- See `requirements.txt` for specific package versions

## License

This project is open source and available under the MIT License. 