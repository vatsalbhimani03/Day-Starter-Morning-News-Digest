from datetime import datetime, date
from zoneinfo import ZoneInfo

from model import Subscriber, DigestResult
from Infrastructure.repository import MongoDBRepo
from Infrastructure.email import EmailService
from news.news_facade import NewsFacade
from news.strategies import KeywordRankingStrategy, BulletSummarizationStrategy


class Controller:

    def __init__(self, country: str):
        self.repo = MongoDBRepo()
        self.email_service = EmailService()
        self.facade = NewsFacade("newsapi", country=country)
        self.ranker = KeywordRankingStrategy()
        self.summarizer = BulletSummarizationStrategy()

    # ---------- Methods/Actions ----------
    def subscribe(self, email: str, topics: list[str], timezone: str, send_hour: int) -> str:
        # Add subscriber to database - create or update
        s = Subscriber(email=email, topics=topics, timezone=timezone, send_hour=send_hour)
        return self.repo.upsert_subscriber(s)
    
    def unsubscribe(self, email: str) -> str:
        # Remove subscriber from database - soft delete (set active to False)
        return self.repo.remove_subscriber(email)
    
    def send_now(self, email: str) -> str:
        # 1) Look up subscriber (dict or dataclass) - Ensure the subscriber exists
        sub = self.repo.get_subscriber(email)
        if not sub:
            return "Subscriber not found or inactive."

        topics = sub["topics"] or sub.topics

        # 2) Fetch + Rank + Summarize 
        # Facade+Adapater & Factory Pattern - Fetch Articles from NewsAPI
        articles = self.facade.get_top_headlines(topics)

        # Strategy Pattern - Rank and Summarize Articles
        ranked = self.ranker.rank_articles(topics, articles)
        summary = self.summarizer.summarize_articles(topics, ranked)

        print(f"\n\nFetched Articles: {articles}") # [list of Article]
        print(f"\n\nRanked Articles: {ranked}") 
        print(f"\n\nSummarized Articles: {summary}") 

        # 3) Subject (single line)
        topics_display = ", ".join(t.title() for t in topics) or "Top Stories"
        today_str = date.today().strftime("%b %d, %Y")
        subject = f"DayStarter – Morning Digest • {topics_display} • {today_str}"

        # 4) Body (simple HTML-friendly lines)
        header_lines = [
            f"Good morning, here is your news digest for {today_str}.",
            "Curated headlines from trusted sources and ranked for you.\n",
            (summary[0] if summary else f"Top {topics_display} picks"),
            ""
        ]

        if ranked:
            item_lines = [f"• <a href=\"{a.url}\">{a.title}</a> — {a.source}" for a in ranked[:10]]
        else:
            item_lines = ["No matching items today. Try broader topics like Tech or Finance or Health."]

        footer_lines = [
            "",
            "~ DayStarter",
            "<span style='font-size:12px;color:#888'>Update your topics/time by choosing “Subscribe” again in the app.</span>"
        ]

        # 5) Send
        ok = self.email_service.send_email(email, subject, header_lines + item_lines + footer_lines)

        status = "sent" if ok and ranked else ("no_items" if ok else "error")
        return f"Digest: {status} (items={len(ranked)})"

    def send_all_active(self, force: bool) -> str:
        # force=True - manual mode: push now to everyone.
        sent = 0
        today = date.today().isoformat()

        # Send news digests to all active subscribers
        for sub in self.repo.get_active_subscribers():

            msg = self.send_now(sub["email"])
            if msg.startswith(("Digest: sent", "Digest: no_items")):
                sent += 1

        return f"Processed {sent} subscriber(s)."

    def send_all_due_now(self) -> str:
        # Send news digests to all subscribers due for sending 
        return "Sent digests to 0 subscribers."

    def history(self, email: str) -> list[dict]:
        # Retrieve sending history for the specified email 
        return []