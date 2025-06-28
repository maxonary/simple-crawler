import streamlit as st
import pandas as pd
from crawler import SimpleCrawler
import json

# Page configuration
st.set_page_config(
    page_title="Simple Web Crawler",
    page_icon="🕷️",
    layout="wide"
)

# Initialize session state
if 'crawler' not in st.session_state:
    st.session_state.crawler = SimpleCrawler()

if 'results' not in st.session_state:
    st.session_state.results = []

def main():
    st.title("🕷️ Simple Web Crawler")
    st.markdown("Enter URLs to crawl and get main body content for each one.")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        st.markdown("**Crawler Settings**")
        st.info("The crawler will automatically add 'https://' if no protocol is specified.")
        
        st.markdown("---")
        st.markdown("**Features:**")
        st.markdown("• Extract main body content (cleaned)")
        st.markdown("• Remove scripts, styles, and navigation")
        st.markdown("• Display response status and headers")
        st.markdown("• Show content length and encoding")
        st.markdown("• Export results to JSON")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Input URLs")
        
        # URL input methods
        input_method = st.radio(
            "Choose input method:",
            ["Single URL", "Multiple URLs (one per line)"]
        )
        
        if input_method == "Single URL":
            url_input = st.text_input(
                "Enter URL:",
                placeholder="e.g., example.com or https://example.com"
            )
            urls = [url_input] if url_input else []
        else:
            url_text = st.text_area(
                "Enter URLs (one per line):",
                placeholder="example.com\nhttps://google.com\nhttps://github.com",
                height=150
            )
            urls = [url.strip() for url in url_text.split('\n') if url.strip()]
        
        # Crawl button
        if st.button("🕷️ Start Crawling", type="primary", disabled=not urls):
            if urls:
                with st.spinner("Crawling URLs..."):
                    st.session_state.results = st.session_state.crawler.crawl_multiple_urls(urls)
                st.success(f"Crawled {len(st.session_state.results)} URLs!")
    
    with col2:
        st.header("Quick Stats")
        if st.session_state.results:
            successful = sum(1 for r in st.session_state.results if r.get('success', False))
            failed = len(st.session_state.results) - successful
            
            st.metric("Total URLs", len(st.session_state.results))
            st.metric("Successful", successful)
            st.metric("Failed", failed)
            
            if successful > 0:
                avg_content_length = sum(r.get('content_length', 0) for r in st.session_state.results if r.get('success', False)) / successful
                st.metric("Avg Content Length", f"{avg_content_length:,.0f} chars")
    
    # Display results
    if st.session_state.results:
        st.header("Crawl Results")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            show_successful = st.checkbox("Show Successful", value=True)
        with col2:
            show_failed = st.checkbox("Show Failed", value=True)
        with col3:
            if st.button("📥 Export to JSON"):
                json_str = json.dumps(st.session_state.results, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=json_str,
                    file_name="crawl_results.json",
                    mime="application/json"
                )
        
        # Display each result
        for i, result in enumerate(st.session_state.results):
            if (result.get('success', False) and show_successful) or (not result.get('success', False) and show_failed):
                with st.expander(f"📄 {result['url']}", expanded=True):
                    if result.get('success', False):
                        # Successful crawl
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown("**Main Body Content:**")
                            st.text_area(
                                "Content",
                                value=result.get('content', ''),
                                height=400,
                                key=f"content_{i}",
                                disabled=True
                            )
                        
                        with col2:
                            st.markdown("**Response Details:**")
                            st.write(f"Status: {result.get('status_code')}")
                            st.write(f"Content Type: {result.get('content_type', 'N/A')}")
                            st.write(f"Encoding: {result.get('encoding', 'N/A')}")
                            st.write(f"Content Length: {result.get('content_length', 0):,} characters")
                            
                            # Download individual content
                            if st.button(f"📥 Download Content {i+1}"):
                                st.download_button(
                                    label="Download",
                                    data=result.get('content', ''),
                                    file_name=f"content_{i+1}.txt",
                                    mime="text/plain",
                                    key=f"download_{i}"
                                )
                    else:
                        # Failed crawl
                        st.error(f"❌ Crawl failed: {result.get('error', 'Unknown error')}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        <p>Simple Web Crawler - Built with Streamlit and BeautifulSoup</p>
        <p>⚠️ Please be respectful of websites' robots.txt and rate limiting policies</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 