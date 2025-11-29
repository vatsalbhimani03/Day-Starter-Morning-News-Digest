from abc import ABC, abstractmethod
from model import Article

# Strategy Pattern - defines interface for ranking strategies and summarization strategies
class IRankingStrategy(ABC):
    @abstractmethod
    def rank_articles(self, topics: list[str], articles: list[Article]) -> list[Article]:
        pass
class ISummarizationStrategy(ABC):
    @abstractmethod
    def summarize_articles(self, topics: list[str], articles: list[Article]) -> list[str]:
        pass

class KeywordRankingStrategy(IRankingStrategy):
    # Ranks articles based on keyword matches in title/description
    def rank_articles(self, topics: list[str], articles: list[Article]) -> list[Article]:
        keys = {k.lower() for t in topics for k in t.split()}  # "stock market" -> {"stock","market"}

        def score(a: Article) -> int:
            text = f"{a.title} {a.description or ''}".lower()
            return sum(1 for k in keys if k in text)

        return sorted(articles, key=score, reverse=True)

class BulletSummarizationStrategy(ISummarizationStrategy):
    # Summarizes articles into bullet points
    def summarize_articles(self, topics: list[str], articles: list[Article]) -> list[str]:
        prefix = f"Top {', '.join(topics)} picks"
        bullets = [f"• {a.title} — {a.source}" for a in articles]
        
        return [prefix] + bullets[:10]  # first line is a header