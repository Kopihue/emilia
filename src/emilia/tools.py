from ddgs import DDGS
from ddgs.exceptions import DDGSException
from trafilatura import (
    fetch_url,
    extract,
)

from kopilogs.paint import paint

from concurrent.futures import ThreadPoolExecutor
import sys 
import textwrap
import datetime

def what_time_is_it() -> str:
    """
    Use this tool whenever you want to know what time it is right now.

    Args:
        None

    Returns:
        str -> Formatted string containing the exact datetime
    """
    paint(f"Getting datetime...").bold().magenta().show()

    return datetime.datetime.now().strftime(r"%a | %Y/%m/%d -- %H:%M:%S")

def search_internet(search_query: str) -> str:
    """
    Use this tool when Peter need up-to-date accurate facts about something.

    Args:
        str -> Search query

    Returns:
        str -> Formatted str containing webpages: [title, href, information]

    Use the information retrieved to answer Peter
    """
    paint(f"Searching the internet... {search_query}").bold().magenta().show()

    def fetch(result: dict[str, str]) -> str | None:
        extracted = extract(fetch_url(result["href"]))
        return extracted

    results = list(DDGS().text(search_query, max_results=3))
    with ThreadPoolExecutor() as exec:
        threads = []

        for result in results:
            thread = exec.submit(fetch, result)
            threads.append(thread)

    formatted_results = ""
    for i, thread in enumerate(threads):
        try:
            result = thread.result()
        except Exception:
            continue

        if result is not None:
            formatted_results += textwrap.dedent(
                f"""

                RESULT {i}

                {result[:5000]}

                """
            )

    return formatted_results
