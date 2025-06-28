import requests
import time
from typing import Dict, Optional
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class SimpleCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def extract_links(self, soup, base_url: str) -> Dict[str, list]:
        """
        Extract all links from the page and categorize them
        """
        links = {
            'internal': [],
            'external': [],
            'all': []
        }
        
        try:
            # Find all anchor tags with href
            for link in soup.find_all('a', href=True):
                href = link['href'].strip()
                
                # Skip empty links, javascript, mailto, etc.
                if not href or href.startswith(('javascript:', 'mailto:', 'tel:', '#', 'data:')):
                    continue
                
                # Make relative URLs absolute
                absolute_url = urljoin(base_url, href)
                
                # Categorize as internal or external
                base_domain = urlparse(base_url).netloc
                link_domain = urlparse(absolute_url).netloc
                
                if link_domain == base_domain:
                    links['internal'].append(absolute_url)
                else:
                    links['external'].append(absolute_url)
                
                links['all'].append(absolute_url)
            
            # Remove duplicates while preserving order
            links['internal'] = list(dict.fromkeys(links['internal']))
            links['external'] = list(dict.fromkeys(links['external']))
            links['all'] = list(dict.fromkeys(links['all']))
            
        except Exception as e:
            print(f"Error extracting links: {e}")
        
        return links
    
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
            
            return text_content, soup
            
        except Exception as e:
            # Fallback: return raw HTML if parsing fails
            return html_content, None
    
    def crawl_url(self, url: str) -> Dict[str, any]:
        """
        Crawl a single URL and return main body content with links
        """
        try:
            # Add http:// if no protocol specified
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # Fetch the page
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Extract body content and get soup object
            body_content, soup = self.extract_body_content(response.text)
            
            # Extract links if soup is available
            links = {'internal': [], 'external': [], 'all': []}
            if soup:
                links = self.extract_links(soup, url)
            
            # Return main body content with links
            return {
                'url': url,
                'status_code': response.status_code,
                'content': body_content,
                'content_type': response.headers.get('content-type', ''),
                'encoding': response.encoding,
                'content_length': len(body_content),
                'links': links,
                'internal_links_count': len(links['internal']),
                'external_links_count': len(links['external']),
                'total_links_count': len(links['all']),
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