from abc import ABC, abstractmethod
import requests

from model import Article
from config import NEWS_API

class INewsProvider(ABC):
    @abstractmethod
    def fetch_top_headlines(self, topics: list[str], country, page_size) -> list[Article]:
        pass
    
# Adapter Pattern - wraps NewsAPI and implements INewsProvider by converting its JSON responses into Article models.
class NewsApiClientAdapter(INewsProvider):
    BASE_TOP = "https://newsapi.org/v2/top-headlines"

    # Mapping of common topics to NewsAPI categories
    CATEGORY_MAP = {
        "tech": "technology", "technology": "technology", "ai": "technology",
        "finance": "business", "business": "business", "stocks": "business", "stock market": "business",
        "sports": "sports",
        "world": "general", "international": "general",
    }

    # implements INewsProvider method using NewsAPI
    def fetch_top_headlines(self, topics: list[str], country, page_size) -> list[Article]:
        if not NEWS_API:
            print("NEWS_API_KEY is missing (returning empty set)")
            return []

        headers = {"X-Api-Key": NEWS_API}
        target_count = max(1, int(page_size))
        results: list[Article] = []

        # converts raw NewsAPI article JSON to Article dataclass (Adapter pattern).
        def adapt(items):
            out = [] # list[Article]
            for a in items or []:
                out.append(Article(
                    title=a.get("title") or "(no title)",
                    url=a.get("url") or "",
                    source=(a.get("source") or {}).get("name") or "NewsAPI",
                    description=a.get("description"),
                    published_at=a.get("publishedAt"),
                ))
            return out

        # removes duplicates by URL/title so overlapping queries don’t repeat items.
        def deduplication(arts: list[Article]) -> list[Article]:
            seen_titles, seen_urls, unique = set(), set(), [] # list[Article]
            for a in arts:
                if (a.url and a.url in seen_urls) or (a.title and a.title in seen_titles):
                    continue
                unique.append(a)
                if a.url: seen_urls.add(a.url)
                if a.title: seen_titles.add(a.title)
            return unique

        # Per-topic queries (category first, else keyword in top-headlines)
        for raw in topics:
            if len(results) >= target_count: 
                break
            t = (raw or "").strip().lower()
            params = {"country": country, "pageSize": min(5, target_count - len(results))}
            cat = self.CATEGORY_MAP.get(t)
            if cat:
                params["category"] = cat
            else:
                params["q"] = t

            try:
                r = requests.get(self.BASE_TOP, params=params, headers=headers, timeout=10)
                data = r.json()
                r.raise_for_status()
                results = deduplication(results + adapt(data.get("articles")))
            except Exception:
                pass

        return results[:target_count]
    

# Factory Pattern - creates new provider instances based on the requested provider name.
class ProviderFactory:
    @staticmethod
    def create(provider_name: str) -> INewsProvider:
        if provider_name.lower() == "newsapi":
            return NewsApiClientAdapter()
        else:
            raise ValueError(f"Unknown news provider: {provider_name}")