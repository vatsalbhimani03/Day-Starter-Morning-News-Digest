from typing import List
from config import SEND_HOUR_LOCAL,DEFAULT_TOPICS, TIMEZONE, NEWS_COUNTRY
from controller import Controller

# get user input with prompt and optional default
def user_input(prompt: str, default: str = "") -> str:
    try:
        val = input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nGoodBye!")
        raise SystemExit(0)
    return (val or default).strip()

# set Topics either from user input or default
def parse_topics(raw: str) -> List[str]:
    topics = []
    for part in raw.split(","):
        part = part.strip().lower()
        if part:
            topics.append(part)

    if not topics:
        topics = list(DEFAULT_TOPICS)

    return topics

# UI/CLI for the DayStarter application
def menu() -> str:
    print("""
    ******** DayStarter – Morning News Digest ********
            1) Subscribe
            2) Unsubscribe
            3) Send Now (one subscriber)
            4) Send Now to All Active
            5) History (per subscriber)
            6) Start Minute Scheduler (demo)
            0) Exit
        """)
    return user_input("Choose: ")
 
def main():
    app = Controller(country=NEWS_COUNTRY)  # "us" for USA, "ca" for Canada, etc.
    while True:
        choice = menu() 
        if choice == "1":
            email = user_input("Email: ")
            topics = parse_topics(user_input(f"Topics (write comma saperated) [{', '.join(DEFAULT_TOPICS)}]: "))
            timezone = user_input(f"Timezone [America/Toronto or Asia/Kolkata]: ", TIMEZONE)
            sendhour = int(user_input("Send hour (0-23): ", SEND_HOUR_LOCAL))
            print(app.subscribe(email, topics, timezone, sendhour))
        elif choice == "2":
            print(app.unsubscribe(user_input("Email: ")))
        elif choice == "3":
            print(app.send_now(user_input("Email: ")))
        elif choice == "4":
            print(app.send_all_active(force=True))
        elif choice == "5":
            email = user_input("Email: ")
            for h in app.history(email):
                print(f"{h['created_at']}  status={h['status']}  items={h['count']}")
        elif choice == "6":
            print("Press Ctrl+C to stop. Checking every ~60 seconds...")
            import time
            try:
                while True:
                    print(app.send_all_due_now())
                    time.sleep(60)
            except KeyboardInterrupt:
                print("\nScheduler stopped.")
        elif choice == "0":
            print("GoodBye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodBye!")

