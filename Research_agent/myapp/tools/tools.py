"""
Tools for the Multi-Agent Research System.

Provides two LangChain tools:
  - web_search : search the web via Tavily
  - scrape_url : extract readable text from a URL
"""

import os
import re

import requests
import trafilatura
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_core.tools import tool
from readability import Document
from tavily import TavilyClient

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# ── Web Search ───────────────────────────────────────────────────────────────
@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic.
    Returns Titles, URLs and snippets."""

    results = tavily.search(query=query, max_results=4)
    out = []
    for r in results["results"]:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\n"
            f"Snippet: {r['content'][:300]}\n"
        )
    return "\n----\n".join(out)

# ── URL Scraper ──────────────────────────────────────────────────────────────
def _clean_text(text: str) -> str:
    """Remove excessive whitespace while keeping paragraph breaks."""
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def _scrape_with_trafilatura(html: str) -> str | None:
    """Strategy 1 - trafilatura (best for articles)."""
    extracted = trafilatura.extract(html, include_comments=False)
    if extracted and len(extracted) > 100:
        return _clean_text(extracted)
    return None

def _scrape_with_readability(html: str) -> str | None:
    """Strategy 2 - readability-lxml (good fallback for complex pages)."""
    try:
        doc = Document(html)
        summary_html = doc.summary()
        soup = BeautifulSoup(summary_html, "lxml")
        text = soup.get_text(separator="\n")
        if text and len(text) > 100:
            return _clean_text(text)
    except Exception:
        pass
    return None

def _scrape_with_beautifulsoup(html: str) -> str | None:
    """Strategy 3 - BeautifulSoup raw text (last resort)."""
    try:
        soup = BeautifulSoup(html, "lxml")
        # Remove script/style tags
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator="\n")
        if text and len(text) > 50:
            return _clean_text(text)
    except Exception:
        pass
    return None


@tool
def scrape_url(url: str) -> str:
    """Fetch a URL and extract its main readable text content.
    Uses multiple fallback strategies for reliable extraction."""

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.RequestException as exc:
        return f"Error fetching {url}: {exc}"

    html = response.text

    # Try each strategy in order
    for strategy in [
        _scrape_with_trafilatura,
        _scrape_with_readability,
        _scrape_with_beautifulsoup,
    ]:
        result = strategy(html)
        if result:
            # Limit to ~4000 chars to stay within LLM context limits
            return result[:4000]

    return f"Could not extract readable content from {url}"
