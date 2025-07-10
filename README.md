📚 SectionTallyBot

A Python script designed to monitor course availability at Rowan University using their public Section Tally interface. This tool helped me secure a seat in the Online Calculus II course after weeks of watching for openings — and it can help you too!

🚀 Overview

SectionTallyBot automatically:

    Checks Rowan’s Section Tally for open spots in a specific course (using CRN).

    Sends email notifications when a seat becomes available.

    Sends daily update emails if no spot opens (optional heartbeat).

    Runs on a timed interval (every minute by default).

🛠 Requirements

    Python 3

    requests

    schedule

    A Mailgun account for sending email alerts.

Install required packages using:

pip install -r requirements.txt

🔧 Setup

    Clone the repository or download the script files.

    Edit the config.ini file:

[PARAMs]
termcode = 202540          ; You can find this in the URL on SectionTally.
dept = MATH                ; Department code (MATH, CS, etc.)
crn = 41162                ; CRN Number (The most important)

api = YOUR_MAILGUN_API_KEY
domain = YOUR_MAILGUN_DOMAIN
email = your_email@example.com

Use the full list of department codes provided in the config file comments for reference.

    Run the script:

python3 SectionTallyBot.py

📬 How It Works

    The script polls Rowan's section tally every minute.

    It scrapes the HTML for the configured CRN.

    It extracts:

    --  Open seats

    --  Total seats

    --  Instructor name

    If any seats are available, it sends an update email through mailgun.

    Otherwise, it sends a daily status update.

I personally used this script for 2 months after missing out on a Calculus II opening during the registration period. I ran it on an Raspberry Pi 4 24/7 however you can just use this in the background on a personal laptop/PC.

THIS README WAS GENERATED WITH AI, AND EDITED BY MYSELF.
(README's are boring...)
