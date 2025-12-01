# Day Starter - Morning News Digest

Day Starter is a small console application that emails (or prints to the console) a one-page morning digest of headlines tailored to a user’s topics at chosen hour. The goal is to showcase clear architecture and design patterns in a tiny and real-world tool.

---

## Setup (mandatory)

### 1. Set up & Activate virtual environment

~~~bash
python3 -m venv .venv
source .venv/bin/activate
~~~

### 2. Upgrade pip & install dependencies from requirements.txt

~~~bash
python -m pip install --upgrade pip
pip install -r requirements.txt
~~~

---

## Run the application (mandatory)

### 3. Start the CLI and follow the prompts

~~~bash
python3 main.py
~~~

You’ll see a menu like this:

~~~text
****** DayStarter - Morning News Digest ******
1) Subscribe
2) Unsubscribe
3) Send Now (one subscriber)
4) Send Now to All Active
5) History (per subscriber)
6) Start Daily Scheduler (minute/hourly tick - demo)
0) Exit
~~~

---

## Configuration

All configuration is handled via `config.py`, and all API keys are defined in the `.env` file.

- Ensure your `.env` contains all required keys (NEWS_API_KEY, MONGODB_CONNECTION_STRING, SENDGRID_API_KEY, SENDER_EMAIL).
- `config.py` reads from `.env` and centralizes application settings (API keys, DB CONN, scheduler defaults, etc.).

---

## Technology used

- **Backend:** Python 3.12 (CLI)
- **Cloud Database:** MongoDB Atlas
- **Third-Party Web Service:** NewsAPI (for headlines)
- **Email Provider:** SendGrid

---

## Detailed Description of Each Menu Options:

### 1) Subscribe

**What it does**

- Creates a new subscriber or updates an existing one in MongoDB.

**Database**

- Writes/updates a document in the `subscribers` collection.
- Stores the subscriber’s email, topics, preferred send hour, timezone, active, and created_at.

---

### 2) Unsubscribe

**What it does**

- Marks a subscriber’s email as inactive so they no longer receive digests.

**Database**

- Sets `active = false` in the `subscribers` collection for that email.

---

### 3) Send Now (one subscriber)

**What it does**

- Fetches the latest headlines for that user’s topics.
- Ranks and summarizes them.
- Sends a one-off digest immediately to that user’s email.  
- **Ignores** the scheduled hour & the daily guard.

**Database**

- Logs a send attempt as a new document in the `history` collection.
- Stores the subscriber’s email, status, count, and created_at.

---

### 4) Send Now to All Active

**What it does**

- Sends 1 digest email to **every** active subscriber.
- **Ignores** the scheduled hour & the daily guard.

**Database**

- Logs each send attempt as a separate document in the `history` collection.
- Stores the subscriber’s email, status, count, and created_at.

---

### 5) History (per subscriber)

**What it does**

- Displays recent send attempts for a given email.
- Shows status, timestamp, and item count for each attempt.

**Database**

- Reads from the `history` collection filtered by subscriber email.

---

### 6) Start Daily Scheduler

**What it does**

- Starts a loop that runs every tick (minute/hour – demo mode).
- For each active subscriber:
  - Checks their local time.
  - If the current local hour equals their configured `send_hour`,
  - And they **haven’t** received a digest today,
  - Then sends exactly one email digest to that user.

**Database**

- Records the send date in the `sent_guard` collection so each subscriber gets at most one digest per day.

**How to stop**

- Press `Ctrl + C` to interrupt and exit the scheduler loop.

---

### 0) Exit

**What it does**

- Quits the application.


---

## Optional checks (NOT NECESSARY AT ALL)

These help you verify the DB & NEWS API connections 

### Check MongoDB connection (TEST)

~~~bash
python3 check_MongoDB_conn.py
~~~

### Check NewsAPI connection (TEST)

~~~bash
python3 check_NewsAPI_conn.py
~~~


