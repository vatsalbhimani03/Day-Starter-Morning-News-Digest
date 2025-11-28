from typing import List, Dict

class Controller:

    def __init__(self, country: str = "ca"):
        pass

    # ---------- Methods/Actions ----------
    def subscribe(self, email: str, topics: List[str], timezone: str, send_hour: int) -> str:
        # Add subscriber to database (implementation)
        return "Subscribed."

    def unsubscribe(self, email: str) -> str:
        # Remove subscriber from database (implementation)
        return "Unsubscribed."

    def send_now(self, email: str) -> str:
        # Send news digest to the specified email (implementation)
        return "Digest: sent 0 items."

    def send_all_due_now(self) -> str:
        # Send news digests to all subscribers due for sending (implementation)
        return "Sent digests to 0 subscribers."

    def history(self, email: str) -> List[Dict]:
        # Retrieve sending history for the specified email (implementation)
        return []