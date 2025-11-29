from model import Subscriber
from Infrastructure.repository import MongoDBRepo

class Controller:

    def __init__(self, country: str = "ca"):
        self.repo = MongoDBRepo()
        

    # ---------- Methods/Actions ----------
    def subscribe(self, email: str, topics: list[str], timezone: str, send_hour: int) -> str:
        # Add subscriber to database - create or update
        s = Subscriber(email=email, topics=topics, timezone=timezone, send_hour=send_hour)
        return self.repo.upsert_subscriber(s)
    
    def unsubscribe(self, email: str) -> str:
        # Remove subscriber from database - soft delete (set active to False)
        return self.repo.remove_subscriber(email)

    def send_now(self, email: str) -> str:
        # Send news digest to the specified email 
        sub = self.repo.get_subscriber(email)
        if not sub:
            return "Subscriber not found or inactive."
        
        # implementation to fetch news and send email

        return "Digest Sent (0 items)"

    def send_all_due_now(self) -> str:
        # Send news digests to all subscribers due for sending 
        return "Sent digests to 0 subscribers."

    def history(self, email: str) -> list[dict]:
        # Retrieve sending history for the specified email 
        return []