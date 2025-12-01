# Day-Starter-Morning-News-Digest
Day Starter is a small console application that emails (or prints to console) a one-page morning digest of headlines tailored to a user’s topics at chosen hour. The goal is to showcase clear architecture and design patterns in a tiny and real-world tool. 

1. Set up & Activate virtual environment.
python3 -m venv .venv
source .venv/bin/activate

2. Upgrade pip & Install required versions from requirements.txt
python -m pip install --upgrade pip
pip install -r requirements.txt

Optional:
3. Run check_MongoDB_conn.py file to check DB connection (TEST)
python3 check_MongoDB_conn.py
4. Run check_NewsAPI_conn.py file to check NewsAPI connection (TEST)
python3 check_NewsAPI_conn.py

Mandatory:
5. Run main.py file & enter input
python3 main.py
You will see these options:
****** DayStarter - Morning News Digest ******
1) Subscribe
2) Unsubscribe
3) Send Now (one subscriber)
4) Send Now to All Active
5) History (per subscriber)
6) Start Daily Scheduler (minute/hourly tick - demo)
0) Exit

NOTE:
All configurations are done via config.py, and all API_KEY are defined in .env.



Detailed Description of Each Options:

1) Subscribe
What it does: Creates or updates a subscriber in MongoDB.
DB: writes/updates a document in the subscribers collection.

2) Unsubscribe
What it does: Marks the email inactive.
DB: sets active=false in subscribers.

3) Send Now (one subscriber)
What it does: Fetches latest headlines for that user’s topics, ranks & summarizes them, and sends a one-off digest now to user's email (Ignores the scheduled hour & the daily guard).
DB: logs a row in history collection.

4) Send Now to All Active
What it does: sends 1 digest email to every active subscriber. (Ignores the scheduled hour & the daily guard)
DB: logs each attempt in history collection.

5) History (per subscriber)
What it does: Shows recent send attempts for that email from the history collection (status, timestamp, item count).

6) Start Daily Scheduler
What it does: Starts a loop that, every tick, checks each active subscriber’s local time.
If current local hour equals their configured send_hour and if they haven’t received a digest today, it sends 1 email to user.
DB: records the date in sent_guard collection.
Stop: press Ctrl+C to interrupt/exit

0) Exit
What it does: Quits the app.