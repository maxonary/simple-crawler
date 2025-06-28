import streamlit as st
import pandas as pd
from crawler import SimpleCrawler
import json
import time

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

if 'selected_links' not in st.session_state:
    st.session_state.selected_links = {}

def main():
    st.title("🕷️ Simple Web Crawler")
    st.markdown("Enter URLs to crawl and get main body content with discovered links for each one.")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        st.markdown("**Crawler Settings**")
        st.info("The crawler will automatically add 'https://' if no protocol is specified.")
        st.info("Auto-discovery for internal links works best in 'Full Page' mode.")
        # Mode selection
        crawl_mode = st.selectbox(
            "Crawl Mode:",
            ["Body Only", "Full Page"],
            help="Body Only: Extract clean main content. Full Page: Get complete HTML page."
        )
        
        st.markdown("---")
        st.markdown("**Features:**")
        st.markdown("• Extract main body content (cleaned)")
        st.markdown("• Remove scripts, styles, and navigation")
        st.markdown("• Discover all internal and external links")
        st.markdown("• Display response status and headers")
        st.markdown("• Show content length and encoding")
        st.markdown("• Export results to JSON")
        
        # LLM Best Practices
        if st.button("📚 Show LLM Best Practices"):
            from llm_utils import get_llm_best_practices
            st.markdown(get_llm_best_practices())
    
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
                placeholder="example.com\nhttps://github.com\nhttps://docs.python.org",
                height=150
            )
            urls = [url.strip() for url in url_text.split('\n') if url.strip()]
        
        # Crawl button
        if st.button("🕷️ Start Crawling", type="primary", disabled=not urls):
            if urls:
                with st.spinner("Crawling URLs..."):
                    # Convert mode selection to crawler parameter
                    mode = "body_only" if crawl_mode == "Body Only" else "full_page"
                    st.session_state.results = st.session_state.crawler.crawl_multiple_urls(urls, mode)
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
                
                total_links = sum(r.get('total_links_count', 0) for r in st.session_state.results if r.get('success', False))
                st.metric("Total Links Found", total_links)
    
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
            
            # LLM-optimized export options
            st.markdown("**LLM Export Options:**")
            
            # Export as structured text for LLMs
            if st.button("🤖 Export for LLM (Text)"):
                llm_text = ""
                for i, result in enumerate(st.session_state.results):
                    if result.get('success', False):
                        llm_text += f"=== URL {i+1}: {result['url']} ===\n"
                        llm_text += f"Mode: {result.get('mode', 'N/A').replace('_', ' ').title()}\n"
                        llm_text += f"Content Length: {result.get('content_length', 0):,} characters\n"
                        llm_text += f"Internal Links: {result.get('internal_links_count', 0)}\n"
                        llm_text += f"External Links: {result.get('external_links_count', 0)}\n"
                        llm_text += f"Status: {result.get('status_code')}\n\n"
                        llm_text += f"CONTENT:\n{result.get('content', '')}\n\n"
                        llm_text += "---\n\n"
                
                st.download_button(
                    label="Download LLM Text",
                    data=llm_text,
                    file_name="crawl_results_for_llm.txt",
                    mime="text/plain"
                )
            
            # Export as markdown for better LLM parsing
            if st.button("📝 Export for LLM (Markdown)"):
                markdown_content = "# Web Crawl Results\n\n"
                for i, result in enumerate(st.session_state.results):
                    if result.get('success', False):
                        markdown_content += f"## {i+1}. {result['url']}\n\n"
                        markdown_content += f"**Mode:** {result.get('mode', 'N/A').replace('_', ' ').title()}\n\n"
                        markdown_content += f"**Stats:**\n"
                        markdown_content += f"- Content Length: {result.get('content_length', 0):,} characters\n"
                        markdown_content += f"- Internal Links: {result.get('internal_links_count', 0)}\n"
                        markdown_content += f"- External Links: {result.get('external_links_count', 0)}\n"
                        markdown_content += f"- Status Code: {result.get('status_code')}\n\n"
                        
                        # Add content
                        markdown_content += f"**Content:**\n\n{result.get('content', '')}\n\n"
                        
                        # Add links if available
                        links = result.get('links', {})
                        if links.get('internal') or links.get('external'):
                            markdown_content += "**Discovered Links:**\n\n"
                            if links.get('internal'):
                                markdown_content += "### Internal Links:\n"
                                for link in links['internal'][:10]:  # Limit to first 10
                                    markdown_content += f"- {link}\n"
                                if len(links['internal']) > 10:
                                    markdown_content += f"- ... and {len(links['internal']) - 10} more\n"
                                markdown_content += "\n"
                            
                            if links.get('external'):
                                markdown_content += "### External Links:\n"
                                for link in links['external'][:10]:  # Limit to first 10
                                    markdown_content += f"- {link}\n"
                                if len(links['external']) > 10:
                                    markdown_content += f"- ... and {len(links['external']) - 10} more\n"
                                markdown_content += "\n"
                        
                        markdown_content += "---\n\n"
                
                st.download_button(
                    label="Download LLM Markdown",
                    data=markdown_content,
                    file_name="crawl_results_for_llm.md",
                    mime="text/markdown"
                )
            
            # Export as structured JSON for LLM APIs
            if st.button("🔧 Export for LLM (Structured JSON)"):
                llm_structured = {
                    "crawl_session": {
                        "total_urls": len(st.session_state.results),
                        "successful_crawls": sum(1 for r in st.session_state.results if r.get('success', False)),
                        "failed_crawls": sum(1 for r in st.session_state.results if not r.get('success', False)),
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    },
                    "pages": []
                }
                
                for result in st.session_state.results:
                    if result.get('success', False):
                        page_data = {
                            "url": result['url'],
                            "mode": result.get('mode', 'N/A'),
                            "status_code": result.get('status_code'),
                            "content_length": result.get('content_length', 0),
                            "content": result.get('content', ''),
                            "metadata": {
                                "content_type": result.get('content_type', ''),
                                "encoding": result.get('encoding', ''),
                                "internal_links_count": result.get('internal_links_count', 0),
                                "external_links_count": result.get('external_links_count', 0),
                                "total_links_count": result.get('total_links_count', 0)
                            }
                        }
                        
                        # Add links if available
                        links = result.get('links', {})
                        if links:
                            page_data["links"] = {
                                "internal": links.get('internal', [])[:20],  # Limit for LLM context
                                "external": links.get('external', [])[:20]
                            }
                        
                        llm_structured["pages"].append(page_data)
                
                structured_json = json.dumps(llm_structured, indent=2)
                st.download_button(
                    label="Download Structured JSON",
                    data=structured_json,
                    file_name="crawl_results_structured.json",
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
                            content_label = "Full Page Content" if result.get('mode') == 'full_page' else "Main Body Content"
                            st.markdown(f"**{content_label}:**")
                            st.text_area(
                                "Content",
                                value=result.get('content', ''),
                                height=300,
                                key=f"content_{i}"
                            )
                        
                        with col2:
                            st.markdown("**Response Details:**")
                            st.write(f"Status: {result.get('status_code')}")
                            st.write(f"Content Type: {result.get('content_type', 'N/A')}")
                            st.write(f"Encoding: {result.get('encoding', 'N/A')}")
                            st.write(f"Content Length: {result.get('content_length', 0):,} characters")
                            st.write(f"Mode: {result.get('mode', 'N/A').replace('_', ' ').title()}")
                            
                            # Download individual content
                            if st.button(f"📥 Download Content {i+1}"):
                                st.download_button(
                                    label="Download",
                                    data=result.get('content', ''),
                                    file_name=f"content_{i+1}.txt",
                                    mime="text/plain",
                                    key=f"download_{i}"
                                )
                    
                    # Display links outside the expander to avoid nesting
                    links = result.get('links', {})
                    if links and result.get('success', False):
                        st.markdown("---")
                        st.markdown("**Discovered Links:**")
                        
                        # Link counts
                        link_col1, link_col2, link_col3 = st.columns(3)
                        with link_col1:
                            st.metric("Internal Links", result.get('internal_links_count', 0))
                        with link_col2:
                            st.metric("External Links", result.get('external_links_count', 0))
                        with link_col3:
                            st.metric("Total Links", result.get('total_links_count', 0))
                        
                        # Auto-crawl section
                        st.markdown("**🚀 Auto-Crawl Discovered Links:**")
                        
                        # Initialize session state for this result
                        result_key = f"result_{i}"
                        if result_key not in st.session_state.selected_links:
                            st.session_state.selected_links[result_key] = []
                        
                        # Collect all links for selection
                        all_links = []
                        if links.get('internal'):
                            all_links.extend(links['internal'])
                        if links.get('external'):
                            all_links.extend(links['external'])
                        
                        if all_links:
                            st.write("Select links to crawl:")
                            
                            # Bulk selection options
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                if st.button("Select All Internal", key=f"select_internal_{i}"):
                                    st.session_state.selected_links[result_key] = links.get('internal', [])
                                    st.rerun()
                            with col2:
                                if st.button("Select All External", key=f"select_external_{i}"):
                                    st.session_state.selected_links[result_key] = links.get('external', [])
                                    st.rerun()
                            with col3:
                                if st.button("Clear All", key=f"clear_all_{i}"):
                                    st.session_state.selected_links[result_key] = []
                                    st.rerun()
                            
                            # Show selected links count
                            selected_count = len(st.session_state.selected_links[result_key])
                            if selected_count > 0:
                                st.markdown(f"**Selected {selected_count} links for crawling:**")
                                
                                # Show first few selected links
                                selected_display = st.session_state.selected_links[result_key][:5]
                                for link in selected_display:
                                    st.write(f"• {link}")
                                if selected_count > 5:
                                    st.caption(f"... and {selected_count - 5} more")
                                
                                # Crawl button
                                if st.button(f"🕷️ Crawl {selected_count} Selected Links", type="primary", key=f"crawl_selected_{i}"):
                                    with st.spinner(f"Crawling {selected_count} selected links..."):
                                        # Add new results to existing results
                                        mode = "body_only" if crawl_mode == "Body Only" else "full_page"
                                        new_results = st.session_state.crawler.crawl_multiple_urls(st.session_state.selected_links[result_key], mode)
                                        st.session_state.results.extend(new_results)
                                    st.success(f"Added {len(new_results)} new crawl results!")
                                    # Clear selections after crawling
                                    st.session_state.selected_links[result_key] = []
                                    st.rerun()
                            
                            # Manual link selection with text input
                            st.markdown("**Or manually enter links to crawl:**")
                            manual_links = st.text_area(
                                "Enter URLs (one per line):",
                                placeholder="https://example.com\nhttps://another-site.com",
                                height=100,
                                key=f"manual_links_{i}"
                            )
                            
                            if manual_links.strip():
                                manual_urls = [url.strip() for url in manual_links.split('\n') if url.strip()]
                                if st.button(f"🕷️ Crawl {len(manual_urls)} Manual Links", key=f"crawl_manual_{i}"):
                                    with st.spinner(f"Crawling {len(manual_urls)} manual links..."):
                                        mode = "body_only" if crawl_mode == "Body Only" else "full_page"
                                        new_results = st.session_state.crawler.crawl_multiple_urls(manual_urls, mode)
                                        st.session_state.results.extend(new_results)
                                    st.success(f"Added {len(new_results)} new crawl results!")
                                    st.rerun()
                    
                    if not result.get('success', False):
                        # Failed crawl
                        st.error(f"❌ Crawl failed: {result.get('error', 'Unknown error')}")
                    
                    # Show internal links
                    if links.get('internal'):
                        st.markdown(f"**🔗 Internal Links ({len(links['internal'])})**")
                        st.caption("💡 You can edit, copy, or modify the links below:")
                        internal_text = "\n".join([f"{j+1}. {link}" for j, link in enumerate(links['internal'][:20])])
                        if len(links['internal']) > 20:
                            internal_text += f"\n... and {len(links['internal']) - 20} more"
                        st.text_area("Internal Links", value=internal_text, height=150, key=f"internal_{i}")
                    
                    # Show external links
                    if links.get('external'):
                        st.markdown(f"**🌐 External Links ({len(links['external'])})**")
                        st.caption("💡 You can edit, copy, or modify the links below:")
                        external_text = "\n".join([f"{j+1}. {link}" for j, link in enumerate(links['external'][:20])])
                        if len(links['external']) > 20:
                            external_text += f"\n... and {len(links['external']) - 20} more"
                        st.text_area("External Links", value=external_text, height=150, key=f"external_{i}")
    
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