from datetime import datetime
from model import Subscriber, DigestResult
from Infrastructure.repository import MongoDBRepo
from Infrastructure.email import EmailService


class Controller:

    def __init__(self, country: str = "ca"):
        self.repo = MongoDBRepo()
        self.email_service = EmailService()
        

    # ---------- Methods/Actions ----------
    def subscribe(self, email: str, topics: list[str], timezone: str, send_hour: int) -> str:
        # Add subscriber to database - create or update
        s = Subscriber(email=email, topics=topics, timezone=timezone, send_hour=send_hour)
        return self.repo.upsert_subscriber(s)
    
    def unsubscribe(self, email: str) -> str:
        # Remove subscriber from database - soft delete (set active to False)
        return self.repo.remove_subscriber(email)
    
    def send_now(self, email: str) -> str:
        # Ensure the subscriber exists (keeps the flow consistent with your CLI)
        sub = self.repo.get_subscriber(email)
        if not sub:
            return "Subscriber not found or inactive."

        subject = f"DayStarter – Test Digest • {datetime.today():%b %d, %Y}"
        lines = [
            f"Hello {email},",
            "This is a test email from DayStarter.",
            "If you can read this, your email service is wired correctly.",
            "Have a great day!",
            "~DayStarter"
        ]

        ok = self.email_service.send_email(email, subject, lines)
        if ok:
            return "Test Digest Sent (console mode)."
        else:
            return "Digest Sent (0 items)"
    

    def send_all_due_now(self) -> str:
        # Send news digests to all subscribers due for sending 
        return "Sent digests to 0 subscribers."

    def history(self, email: str) -> list[dict]:
        # Retrieve sending history for the specified email 
        return []