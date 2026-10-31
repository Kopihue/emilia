from ddgs import DDGS
from ddgs.exceptions import DDGSException
from trafilatura import fetch_url, extract

from kopitools import log

from concurrent.futures import ThreadPoolExecutor
from typing import Any
import socket

class Internet:
    def __init__(self):
        try:
            socket.setdefaulttimeout(3)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(("8.8.8.8", 53))

        except socket.error:
            raise RuntimeError("No internet connection for the moment.")

        self.engine = DDGS()

    def get_urls_from_search_queries(self, queries: list[str]) -> str:
        """
        This tool scraps a lot of URLs from search queries.

        Args:
            queries: A list containing the search queries

        Returns:
            Formatted string containing the website's title and URL
        """
        log("Getting URLs from!: ").success()

        def search(query: str) -> list[dict[str, Any]]:
            return self.engine.text(
                query,
                safesearch="off",
            )

        results = ""

        with ThreadPoolExecutor() as exec:
            futures = []

            for query in queries:
                log(f"\tQuery: {query}").success()
                futures.append(exec.submit(search, query))

        counter = 1
        for future in futures:
            try:
                result = future.result()
            except DDGSException:
                continue

            for r in result:
                results += f"[{counter}] {r["title"]}\n{r["href"]}\n\n"

                counter += 1

        return results.strip()

    def get_content_from_urls(self, urls: list[str]) -> str:
        """
        This tool scraps the most relevant information from a URL

        Args:
            queries: A list containing the URLs to scrap

        Returns:
            Formatted string containing the page's content
        """
        log("Getting content!:").success()
        urls = urls[:3]

        def fetch(url: str) -> str | None:
            fetched = fetch_url(url)

            if fetched is not None:
                return extract(
                    fetched,
                    include_comments=True,
                    include_images=False,
                    include_tables=False,
                    include_links=False,
                    fast=True,
                    deduplicate=True,
                )

        results = ""

        with ThreadPoolExecutor() as exec:
            futures = []

            for url in urls:
                log(f"\tURL: {url}").success()
                futures.append(exec.submit(fetch, url))

        for future in futures:
            try:
                result = future.result()
            except Exception as e:
                print(e)
                continue

            if result is not None:
                results += result

        return results.strip()
