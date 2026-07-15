"""
Research Pipeline — orchestrates the multi-agent workflow.

Flow: Search → Read → Write → Critique
"""

import re
from typing import Any, Dict

from myapp.agents.agents import (
    create_critic_chain,
    create_reader_agent,
    create_search_agent,
    create_writer_chain,
)


def _extract_urls(search_output: str) -> list[str]:
    """Pull URLs from the search agent's output."""
    return re.findall(r"https?://[^\s\"\'\)\]]+", search_output)


def run_research_pipeline(topic: str) -> Dict[str, Any]:
    """Run the full research pipeline for a given topic.

    Returns a dict with keys:
        topic, search_results, sources, report, critique, status
    """
    result: Dict[str, Any] = {
        "topic": topic,
        "search_results": "",
        "sources": [],
        "report": "",
        "critique": "",
        "status": "error",
    }

    # ── 1. Search Phase ──────────────────────────────────────────────────
    try:
        search_agent = create_search_agent()
        search_query = (
            f"Search for the most recent and reliable information about: {topic}. "
            f"Find at least 5 relevant sources with different perspectives."
        )
        search_output = search_agent.invoke({"messages": [("user", search_query)]})
        search_text = search_output["messages"][-1].content
        result["search_results"] = search_text
    except Exception as exc:
        result["search_results"] = f"Search failed: {exc}"
        result["status"] = "partial"
        return result

    # ── 2. Reading Phase ─────────────────────────────────────────────────
    urls = _extract_urls(search_text)
    urls = urls[:5]  # Limit to top 5 URLs
    result["sources"] = urls

    scraped_content = []
    if urls:
        try:
            reader_agent = create_reader_agent()
            url_list = "\n".join(f"- {u}" for u in urls)
            read_query = (
                f"Extract the main content from these URLs about '{topic}':\n"
                f"{url_list}\n\n"
                f"Use the scrape_url tool on each URL and summarize the key "
                f"information found."
            )
            reader_output = reader_agent.invoke({"messages": [("user", read_query)]})
            scraped_content.append(reader_output["messages"][-1].content)
        except Exception as exc:
            scraped_content.append(f"Reading failed: {exc}")

    # Combine search snippets and scraped content as source material
    all_sources = search_text
    if scraped_content:
        all_sources += "\n\n--- Detailed Content ---\n\n" + "\n\n".join(scraped_content)

    # ── 3. Writing Phase ─────────────────────────────────────────────────
    try:
        writer = create_writer_chain()
        report_msg = writer.invoke({"topic": topic, "sources": all_sources})
        report_text = report_msg.content if hasattr(report_msg, "content") else str(report_msg)
        result["report"] = report_text
    except Exception as exc:
        result["report"] = f"Report generation failed: {exc}"
        result["status"] = "partial"
        return result

    # ── 4. Critique Phase ────────────────────────────────────────────────
    try:
        critic = create_critic_chain()
        critique_msg = critic.invoke({"topic": topic, "report": report_text})
        critique_text = critique_msg.content if hasattr(critique_msg, "content") else str(critique_msg)
        result["critique"] = critique_text
    except Exception as exc:
        result["critique"] = f"Critique failed: {exc}"

    result["status"] = "completed"
    return result
