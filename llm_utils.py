"""
LLM Utilities for Web Crawler
Best practices for processing crawled content for LLM consumption
"""

import json
import re
from typing import List, Dict, Any
from pathlib import Path

class LLMContentProcessor:
    """
    Utility class for processing crawled content for optimal LLM consumption
    """
    
    def __init__(self):
        self.max_content_length = 8000  # Optimal length for most LLMs
        self.max_links_per_page = 10    # Limit links to prevent context overflow
    
    def clean_content_for_llm(self, content: str, mode: str = "body_only") -> str:
        """
        Clean and optimize content for LLM consumption
        
        Args:
            content: Raw content from crawler
            mode: "body_only" or "full_page"
        
        Returns:
            Cleaned content optimized for LLMs
        """
        if mode == "full_page":
            # For HTML content, extract text while preserving structure
            return self._extract_text_from_html(content)
        else:
            # For body-only content, just clean whitespace
            return self._clean_text_content(content)
    
    def _extract_text_from_html(self, html_content: str) -> str:
        """Extract clean text from HTML while preserving structure"""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text with some structure preservation
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def _clean_text_content(self, text: str) -> str:
        """Clean text content for LLM consumption"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common web artifacts
        text = re.sub(r'Cookie Policy|Privacy Policy|Terms of Service|Contact Us', '', text, flags=re.IGNORECASE)
        
        # Limit length if too long
        if len(text) > self.max_content_length:
            text = text[:self.max_content_length] + "... [Content truncated]"
        
        return text.strip()
    
    def create_llm_prompt_context(self, crawl_results: List[Dict[str, Any]]) -> str:
        """
        Create a well-formatted prompt context from crawl results
        
        Args:
            crawl_results: List of crawl result dictionaries
        
        Returns:
            Formatted string ready for LLM prompt
        """
        context = "## Web Crawl Results\n\n"
        
        for i, result in enumerate(crawl_results, 1):
            if not result.get('success', False):
                continue
                
            context += f"### Page {i}: {result['url']}\n\n"
            
            # Add metadata
            context += f"**Metadata:**\n"
            context += f"- Status: {result.get('status_code', 'N/A')}\n"
            context += f"- Content Length: {result.get('content_length', 0):,} characters\n"
            context += f"- Mode: {result.get('mode', 'N/A').replace('_', ' ').title()}\n\n"
            
            # Add cleaned content
            content = self.clean_content_for_llm(
                result.get('content', ''), 
                result.get('mode', 'body_only')
            )
            context += f"**Content:**\n{content}\n\n"
            
            # Add limited links
            links = result.get('links', {})
            if links.get('internal') or links.get('external'):
                context += "**Key Links:**\n"
                internal_links = links.get('internal', [])[:5]
                external_links = links.get('external', [])[:5]
                
                for link in internal_links:
                    context += f"- Internal: {link}\n"
                for link in external_links:
                    context += f"- External: {link}\n"
                context += "\n"
            
            context += "---\n\n"
        
        return context
    
    def create_structured_llm_data(self, crawl_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create structured data optimized for LLM APIs
        
        Args:
            crawl_results: List of crawl result dictionaries
        
        Returns:
            Structured dictionary for LLM consumption
        """
        structured_data = {
            "session_info": {
                "total_pages": len(crawl_results),
                "successful_crawls": sum(1 for r in crawl_results if r.get('success', False)),
                "failed_crawls": sum(1 for r in crawl_results if not r.get('success', False))
            },
            "pages": []
        }
        
        for result in crawl_results:
            if not result.get('success', False):
                continue
            
            # Clean content for LLM
            cleaned_content = self.clean_content_for_llm(
                result.get('content', ''), 
                result.get('mode', 'body_only')
            )
            
            page_data = {
                "url": result['url'],
                "content": cleaned_content,
                "metadata": {
                    "status_code": result.get('status_code'),
                    "content_length": len(cleaned_content),
                    "mode": result.get('mode', 'body_only'),
                    "content_type": result.get('content_type', ''),
                    "encoding": result.get('encoding', '')
                }
            }
            
            # Add limited links
            links = result.get('links', {})
            if links:
                page_data["links"] = {
                    "internal": links.get('internal', [])[:self.max_links_per_page],
                    "external": links.get('external', [])[:self.max_links_per_page],
                    "total_internal": len(links.get('internal', [])),
                    "total_external": len(links.get('external', []))
                }
            
            structured_data["pages"].append(page_data)
        
        return structured_data
    
    def save_for_llm(self, crawl_results: List[Dict[str, Any]], output_dir: str = "llm_exports"):
        """
        Save crawl results in multiple formats optimized for LLM consumption
        
        Args:
            crawl_results: List of crawl result dictionaries
            output_dir: Directory to save files
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Save as prompt context
        prompt_context = self.create_llm_prompt_context(crawl_results)
        with open(output_path / "llm_prompt_context.txt", "w", encoding="utf-8") as f:
            f.write(prompt_context)
        
        # Save as structured JSON
        structured_data = self.create_structured_llm_data(crawl_results)
        with open(output_path / "llm_structured_data.json", "w", encoding="utf-8") as f:
            json.dump(structured_data, f, indent=2, ensure_ascii=False)
        
        # Save as markdown
        markdown_content = self.create_llm_prompt_context(crawl_results)
        with open(output_path / "llm_content.md", "w", encoding="utf-8") as f:
            f.write(markdown_content)
        
        print(f"LLM-optimized files saved to {output_path}/")
        print(f"- llm_prompt_context.txt (for direct LLM prompts)")
        print(f"- llm_structured_data.json (for API calls)")
        print(f"- llm_content.md (for documentation)")


def get_llm_best_practices() -> str:
    """
    Return best practices for using crawled content with LLMs
    """
    return """
# Best Practices for Using Crawled Content with LLMs

## 1. Content Preparation
- **Clean the content**: Remove scripts, styles, and navigation elements
- **Limit content length**: Most LLMs work best with 4K-8K tokens per context
- **Preserve structure**: Use markdown formatting for better LLM understanding
- **Remove noise**: Filter out common web artifacts (cookies, privacy notices)

## 2. Format Selection
- **For analysis tasks**: Use "Body Only" mode for clean text
- **For web scraping**: Use "Full Page" mode for complete HTML
- **For documentation**: Use markdown format with structured headers
- **For APIs**: Use structured JSON with metadata

## 3. Context Management
- **Chunk large content**: Split long pages into manageable sections
- **Prioritize content**: Focus on main content areas over navigation
- **Include metadata**: Always include URL, status, and content type
- **Limit links**: Include only the most relevant links (5-10 per page)

## 4. LLM-Specific Optimizations
- **GPT models**: Prefer clean text with clear structure
- **Claude models**: Work well with markdown and structured data
- **Local models**: May need shorter content chunks
- **API calls**: Use structured JSON for programmatic access

## 5. Quality Control
- **Verify content**: Check that important information is preserved
- **Test prompts**: Ensure the format works with your specific LLM
- **Monitor length**: Stay within token limits for your model
- **Validate structure**: Ensure links and metadata are accurate
"""


if __name__ == "__main__":
    # Example usage
    processor = LLMContentProcessor()
    print(get_llm_best_practices()) 