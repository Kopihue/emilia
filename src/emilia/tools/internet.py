from ddgs import DDGS
from trafilatura import fetch_url, extract

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

    def get_urls(self, queries: list[str]) -> str:
        def search(query: str) -> list[dict[str, Any]]:
            return self.engine.text(
                query,
                safesearch="off",
            )

        results = ""

        with ThreadPoolExecutor() as exec:
            futures = []

            for query in queries:
                futures.append(exec.submit(search, query))

        counter = 1
        for future in futures:
            try:
                result = future.result()
            except Exception as e:
                print(e)
                continue

            for r in result:
                results += f"[{counter}] {r["title"]}\n{r["href"]}\n\n"

                counter += 1

        return results.strip()

    def get_content(self, urls: list[str]) -> str:
        urls = urls[:3]

        def fetch(url: str) -> str | None:
            return extract(
                fetch_url(url),
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
