import requests
import time
from typing import Dict, Optional
import re
from bs4 import BeautifulSoup

class SimpleCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def extract_body_content(self, html_content: str) -> str:
        """
        Extract only the main body content from HTML, removing scripts, styles, etc.
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'meta', 'link', 'noscript']):
                element.decompose()
            
            # Try to find main content areas
            main_content = None
            
            # Look for common content containers
            selectors = [
                'main',
                'article',
                '.content',
                '.main-content',
                '#content',
                '#main',
                '.post-content',
                '.entry-content',
                '.article-content'
            ]
            
            for selector in selectors:
                found = soup.select_one(selector)
                if found:
                    main_content = found
                    break
            
            # If no specific content area found, use body
            if not main_content:
                main_content = soup.find('body') or soup
            
            # Get text content
            text_content = main_content.get_text(separator=' ', strip=True)
            
            # Clean up whitespace
            lines = (line.strip() for line in text_content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text_content = ' '.join(chunk for chunk in chunks if chunk)
            
            return text_content
            
        except Exception as e:
            # Fallback: return raw HTML if parsing fails
            return html_content
    
    def crawl_url(self, url: str) -> Dict[str, any]:
        """
        Crawl a single URL and return main body content
        """
        try:
            # Add http:// if no protocol specified
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # Fetch the page
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Extract body content
            body_content = self.extract_body_content(response.text)
            
            # Return main body content
            return {
                'url': url,
                'status_code': response.status_code,
                'content': body_content,
                'content_type': response.headers.get('content-type', ''),
                'encoding': response.encoding,
                'content_length': len(body_content),
                'success': True
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'url': url,
                'error': str(e),
                'success': False
            }
        except Exception as e:
            return {
                'url': url,
                'error': f"Unexpected error: {str(e)}",
                'success': False
            }
    
    def crawl_multiple_urls(self, urls: list) -> list:
        """
        Crawl multiple URLs with a small delay between requests
        """
        results = []
        for url in urls:
            url = url.strip()
            if url:  # Skip empty URLs
                result = self.crawl_url(url)
                results.append(result)
                time.sleep(1)  # Be polite to servers
        return results 