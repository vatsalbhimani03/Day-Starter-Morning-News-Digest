from model import Article
from news.providers import ProviderFactory

# Facade Pattern - provides a simplified interface to fetch news from various providers(Adapaters) - Wrapper Pattern
class NewsFacade:
    def __init__(self, provider_name: str, country: str):
        self.provider = ProviderFactory.create(provider_name)
        self.contry = country
        
    def get_top_headlines(self, topics: list[str], page_size: int = 10) -> list[Article]:
        return self.provider.fetch_top_headlines(topics, country=self.contry, page_size=page_size)

