from dotenv import load_dotenv
from firecrawl.firecrawl import FirecrawlApp
from filehandler.fh import Filehandler
import argparse
import os

class FireCrawler:
  def __init__(self, url: str | None = None, limit: int | None = None, formats: list[str] | None = None, interval: int | None = None, api_key_env: str = "FIRECRAWL_API_KEY"):
    load_dotenv()
    self.url = url
    self.api_key = os.getenv(api_key_env)
    self.download_directory = os.getenv("DOWNLOAD_DIRECTORY") or "download"
    self.app = FirecrawlApp(api_key=self.api_key)
    self.limit = limit or 20
    self.formats = formats or ['markdown']
    self.interval = interval or 2
    self.fh = Filehandler()

    if not self.api_key:
      raise ValueError("Firecrawl API key not found as environment variable")

  def main(self) -> None:
    parser = argparse.ArgumentParser(description="What URL are we parsing?")
    parser.add_argument(
       "-u", "--url",
       type=str,
       required=True,
       help="The url you want to crawl, scrape, or map"
       )
    parser.add_argument(
       "-a", "--action",
       type=str,
       required=True,
       choices=["crawl", "scrape", "map"],
       help="Method choices"
    )
    args = parser.parse_args()
    self.url = args.url
    match args.action:
      case "crawl":
          self.crawl()
      case "scrape":
          self.scrape()
      case "map":
          self.map()
      case _:
          print("Invalid action")

    return

  def crawl(self) -> dict[str, str]:
    """
    Recursively crawl through a website using the sitemap or by following links; page content is then mapped to the source url
    with the formats (e.g markdown, html) acting as additional key/value pairs to extract desired information
    result = {
      "source_url": {
        "markdown": "content",
        "html": "content
      }
    }
    """
    if not self.formats:
        raise ValueError("No formats specified for scraping.")

    result = {}
    current_url = self.url

    # limit is based off of pages or '10MB' of data. this might not be needed
    while current_url and len(result) < self.limit:
      try:
        crawl_result = self.app.crawl_url(
          self.url,
          params={
            'limit': self.limit,
            'scrapeOptions': {'formats': self.formats}
          },
          poll_interval=self.interval
        )
      except Exception as e:
        raise RuntimeError(f"Crawling failed for URL {self.url}: {e}")

      for res in crawl_result.get('data', []):
        source_url = res['metadata']['sourceURL']
        result[source_url] = {}

        for fmt in self.formats:
          result[source_url][fmt] = res.get(fmt, None)
          self.fh.crawl_writer(data=result, download_directory=self.download_directory)

      current_url = crawl_result.get('next', None)

    return

  def scrape(self) -> dict[str, str]:
    """
    Functions similarly to crawl, but for a specific URL. Meant to inspect and does not download
    """
    if not self.formats:
        raise ValueError("No formats specified for scraping.")
    try:
      scrape_result = self.app.scrape_url(
        self.url,
        params={'formats': self.formats}
      )
    except Exception as e:
        raise RuntimeError(f"Scraping failed for URL {self.url}: {e}")

    result = {fmt: scrape_result.get(fmt, None) for fmt in self.formats}

    return result

  def map(self) -> list[str]:
    """
    Maps out most urls on a website -- this is not perfect. The ability to search for a specific topic isn't perfect yet, but
    would allow you, at least in the context of the IRS, extract specific documents. For example, many links to downloadable files
    are prefixed with a character like 'i', 'f', 'p' to categorize them as a form or instructions. Alternatively, you could modify
    this to look up a subdomain, such as 'docs' for 'docs.firecrawl.dev'

    This function will download all links mapped
    """
    try:
      map_result = self.app.map_url(self.url)
    except Exception as e:
       raise RuntimeError(f"Mapping failed for URL {self.url}: {e}")

    self.fh.map_writer(links=map_result['links'], download_directory=self.download_directory)

    return

if __name__ == "__main__":
    crawler = FireCrawler()
    crawler.main()
