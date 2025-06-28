# Simple Web Crawler

A lightweight web crawler with a beautiful Streamlit frontend that allows you to crawl multiple URLs and extract clean body content along with all discovered links.

## Features

- 🕷️ **Simple URL Input**: Enter single URLs or multiple URLs at once
- 📄 **Clean Body Content**: Extract main content without scripts, styles, and navigation
- 🔗 **Link Discovery**: Find all internal and external links on each page
- 📊 **Smart Content Extraction**: Intelligently targets main content areas
- 📥 **Export Results**: Download crawl results as JSON or individual text files
- 🎨 **Beautiful UI**: Modern Streamlit interface with real-time statistics
- ⚡ **Fast & Efficient**: Built with requests and BeautifulSoup for optimal performance

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd simple-crawler
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
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

6. **Explore discovered links** in the expandable link sections

7. **Download content** as individual text files or export all results as JSON

## What the Crawler Extracts

For each successfully crawled URL, you'll get:

### Content Information
- **Main Body Content**: Clean text content from the main content area
- **Content Length**: Total number of characters
- **Response Status**: HTTP status code
- **Content Type**: MIME type of the response
- **Encoding**: Character encoding used

### Link Discovery
- **Internal Links**: All links pointing to the same domain
- **External Links**: All links pointing to other domains
- **Total Links**: Complete count of all discovered links
- **Link Lists**: Expandable sections showing the actual URLs

### Error Information
- **Detailed error messages** for failed crawls
- **Network timeout handling**
- **Graceful fallbacks** for parsing issues

## Smart Content Extraction

The crawler intelligently extracts content by:

1. **Removing unwanted elements**: scripts, styles, navigation, headers, footers
2. **Targeting main content areas**: looks for `<main>`, `<article>`, `.content`, etc.
3. **Falling back gracefully**: uses body content if no specific content area is found
4. **Cleaning up text**: removes extra whitespace and formats nicely

## Link Discovery Features

The crawler discovers and categorizes all links:

- **Internal Links**: Links to the same domain (useful for site mapping)
- **External Links**: Links to other domains (useful for backlink analysis)
- **Duplicate Removal**: Automatically removes duplicate links
- **URL Normalization**: Converts relative URLs to absolute URLs
- **Smart Filtering**: Skips javascript:, mailto:, tel:, and other non-HTTP links

## Example Usage

### Input URLs:
```
example.com
https://github.com
https://docs.python.org
```

### Sample Output:
```json
{
  "url": "https://example.com",
  "status_code": 200,
  "content": "Example Domain This domain is for use in illustrative examples...",
  "content_type": "text/html; charset=UTF-8",
  "encoding": "UTF-8",
  "content_length": 1234,
  "links": {
    "internal": ["https://example.com/page1", "https://example.com/page2"],
    "external": ["https://www.iana.org/domains/example"],
    "all": ["https://example.com/page1", "https://example.com/page2", "https://www.iana.org/domains/example"]
  },
  "internal_links_count": 2,
  "external_links_count": 1,
  "total_links_count": 3,
  "success": true
}
```

## Use Cases

- **Content Analysis**: Extract clean text from web pages for analysis
- **Site Mapping**: Discover all pages on a website through internal links
- **Link Research**: Analyze external links and backlinks
- **SEO Analysis**: Understand internal linking patterns
- **Content Monitoring**: Track changes in web page content
- **Data Collection**: Gather text content from multiple sources

## Technical Details

- **Backend**: Python with requests and BeautifulSoup
- **Frontend**: Streamlit for the web interface
- **Content Parsing**: HTML parser (built into Python, no external dependencies)
- **Link Processing**: URL normalization and categorization
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

## Troubleshooting

### Common Issues

1. **Dependency Installation Fails**: 
   - Make sure you're using a virtual environment
   - Try updating pip: `pip install --upgrade pip`

2. **Streamlit Not Starting**:
   - Check if port 8501 is available
   - Try a different port: `streamlit run app.py --server.port 8502`

3. **Crawling Fails**:
   - Check your internet connection
   - Some sites may block automated requests
   - Try with different URLs

## License

This project is open source and available under the MIT License. 