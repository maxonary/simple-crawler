# Simple Web Crawler

A lightweight web crawler with a beautiful Streamlit frontend that allows you to crawl multiple URLs and extract clean body content along with all discovered links.

## Features

- 🕷️ **Simple URL Input**: Enter single URLs or multiple URLs at once
- 📄 **Clean Body Content**: Extract main content without scripts, styles, and navigation
- 🔗 **Link Discovery**: Find all internal and external links on each page
- 📊 **Smart Content Extraction**: Extracts clean main body content by removing scripts, styles, navigation, headers, and footers
- 📥 **Export Results**: Download crawl results as JSON or individual text files
- 🎨 **Beautiful UI**: Modern Streamlit interface with real-time statistics
- ⚡ **Fast & Efficient**: Built with requests and BeautifulSoup for optimal performance
- **Auto-Crawl Links**: Automatically crawl discovered links with bulk selection options
- **Response Details**: Shows HTTP status codes, content types, encoding, and content length
- **Export Options**: Download individual content or export all results as JSON
- **User-Friendly Interface**: Clean Streamlit interface with expandable sections and metrics
- **Error Handling**: Graceful handling of failed requests and invalid URLs
- **Dual Crawl Modes**: Choose between "Body Only" (clean text content) or "Full Page" (complete HTML)
- **LLM-Optimized Exports**: Multiple export formats specifically designed for LLM consumption

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

1. **Start the Application**:
   ```bash
   streamlit run app.py
   ```

2. **Select Crawl Mode**: Choose between "Body Only" (clean text) or "Full Page" (complete HTML) in the sidebar

3. **Enter URLs**: Choose between single URL or multiple URLs input method

4. **Crawl Initial Pages**: Click "Start Crawling" to analyze the pages

5. **Auto-Crawl Discovered Links**: 
   - Use "Select All Internal" to crawl all internal links
   - Use "Select All External" to crawl all external links
   - Or manually enter specific URLs to crawl
   - Click "Crawl Selected Links" to automatically crawl them

6. **View Results**: 
   - Expand each result to see content and links
   - Copy links from the text areas
   - Download individual content or export all results

7. **Export Data**: Use the export button to download all results as JSON

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

## LLM Integration

The crawler includes specialized export options optimized for Large Language Model consumption:

### Export Formats for LLMs

1. **🤖 LLM Text Export**: Clean, structured text format with metadata
2. **📝 LLM Markdown Export**: Markdown-formatted content for better LLM parsing
3. **🔧 Structured JSON Export**: API-ready JSON with cleaned content and metadata

### Best Practices for LLM Usage

- **Content Length**: Most LLMs work best with 4K-8K tokens per context
- **Mode Selection**: Use "Body Only" for analysis tasks, "Full Page" for web scraping
- **Content Cleaning**: Automatically removes scripts, styles, and navigation elements
- **Link Limiting**: Includes only the most relevant links to prevent context overflow
- **Metadata Preservation**: Maintains URL, status, and content type information

### LLM Utilities

The `llm_utils.py` module provides additional utilities:
- Content cleaning and optimization
- Prompt context generation
- Structured data creation
- Best practices documentation

Click "📚 Show LLM Best Practices" in the sidebar for detailed guidelines. 