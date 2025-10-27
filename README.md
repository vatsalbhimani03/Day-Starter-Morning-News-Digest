# Day-Starter-Morning-News-Digest
Day Starter is a small console application that emails (or prints to console) a one-page morning digest of headlines tailored to a user’s topics at chosen hour. The goal is to showcase clear architecture and design patterns in a tiny and real-world tool. 

1. Set up & Activate virtual environment.
python3 -m venv .venv
source .venv/bin/activate

2. Upgrade pip & Install required versions from requirements.txt
python -m pip install --upgrade pip
pip install -r requirements.txt

3. Run check_MongoDB_conn.py file to check DB connection
python3 check_MongoDB_conn.py