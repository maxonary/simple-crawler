import requests
import time
from typing import Dict, Optional
import re

class SimpleCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def crawl_url(self, url: str) -> Dict[str, any]:
        """
        Crawl a single URL and return full page contents
        """
        try:
            # Add http:// if no protocol specified
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # Fetch the page
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Return full page contents
            return {
                'url': url,
                'status_code': response.status_code,
                'content': response.text,
                'content_type': response.headers.get('content-type', ''),
                'encoding': response.encoding,
                'content_length': len(response.text),
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