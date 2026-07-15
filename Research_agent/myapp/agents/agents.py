"""
Multi-Agent Research System.

Four components:
  - Search Agent  : finds relevant web sources
  - Reader Agent  : extracts content from URLs
  - Writer Chain  : synthesizes a structured research report
  - Critic Chain  : evaluates report quality and gives scores
"""

import os

from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openrouter import ChatOpenRouter

from myapp.tools.tools import scrape_url, web_search

load_dotenv()

# ── Shared LLM ───────────────────────────────────────────────────────────────

def _get_llm(temperature: float = 0.3) -> ChatOpenRouter:
    """Return a ChatOpenRouter instance backed by gpt-4o-mini."""
    return ChatOpenRouter(
        model="openai/gpt-4o-mini",
        temperature=temperature,
    )


# ── Search Agent ─────────────────────────────────────────────────────────────

def create_search_agent():
    """Create a search agent that uses Tavily to find relevant sources."""
    llm = _get_llm(temperature=0.2)
    tools = [web_search]
    return create_react_agent(llm, tools)


# ── Reader Agent ─────────────────────────────────────────────────────────────

def create_reader_agent():
    """Create a reader agent that scrapes URLs for full content."""
    llm = _get_llm(temperature=0.1)
    tools = [scrape_url]
    return create_react_agent(llm, tools)


# ── Writer Chain ─────────────────────────────────────────────────────────────

WRITER_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research report writer. You write clear, "
        "well-structured, and comprehensive research reports based on "
        "provided source material. Always cite your sources.",
    ),
    (
        "human",
        "Write a comprehensive research report on the following topic.\n\n"
        "## Topic\n{topic}\n\n"
        "## Source Material\n{sources}\n\n"
        "## Instructions\n"
        "1. Start with a clear title and introduction\n"
        "2. Organize findings into logical sections with headings\n"
        "3. Include key data points, statistics, and quotes\n"
        "4. Provide a conclusion that summarizes the main insights\n"
        "5. List all sources used at the end\n"
        "6. Aim for a thorough, professional report\n",
    ),
])


def create_writer_chain():
    """Create a chain that writes structured research reports."""
    llm = _get_llm(temperature=0.5)
    return WRITER_PROMPT | llm


# ── Critic Chain ─────────────────────────────────────────────────────────────

CRITIC_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a research report critic. You evaluate reports for "
        "quality, accuracy, depth, and completeness. Be constructive.",
    ),
    (
        "human",
        "Evaluate the following research report.\n\n"
        "## Topic\n{topic}\n\n"
        "## Report\n{report}\n\n"
        "## Evaluation Criteria\n"
        "Score each criterion from 1-10 and provide brief feedback:\n"
        "1. **Accuracy** – Are the facts correct and well-sourced?\n"
        "2. **Depth** – Does it cover the topic thoroughly?\n"
        "3. **Clarity** – Is it well-written and easy to understand?\n"
        "4. **Structure** – Is it well-organized with clear sections?\n"
        "5. **Sources** – Are sources properly cited?\n\n"
        "Provide an **Overall Score** (1-10) and a short summary of "
        "strengths and areas for improvement.\n",
    ),
])


def create_critic_chain():
    """Create a chain that evaluates research report quality."""
    llm = _get_llm(temperature=0.3)
    return CRITIC_PROMPT | llm
