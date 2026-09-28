from emilia.tools.internet import Internet
from emilia.tools.dates import Dates

def get_urls_from_search_queries(queries: list[str]) -> str:
    """
    This tool scraps a lot of URLs from search queries.

    Args:
        queries: A list containing the search queries

    Returns:
        Formatted string containing the website's title and URL
    """

    try:
        client = Internet()
    except RuntimeError as e:
        return str(e)

    return client.get_urls(queries)

def get_content_from_urls(urls: list[str]) -> str:
    """
    This tool scraps the most relevant information from a URL

    Args:
        queries: A list containing the URLs to scrap

    Returns:
        Formatted string containing the page's content
    """

    try:
        client = Internet()
    except RuntimeError as e:
        return str(e)

    return client.get_urls(urls)

def get_current_datetime() -> str:
    """
    Use this tool whenever you want to know what time it is right now.

    Args:
        None

    Returns:
        str -> Formatted string containing the exact datetime
    """

    client = Dates()
    return client.get_current_datetime()

