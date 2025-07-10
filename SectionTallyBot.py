import requests
import re
import configparser
import time
import schedule

cfg = configparser.ConfigParser()
cfg.read('config.ini')

mailgunAPI = cfg['PARAMs']['api']
mailgunDomain = cfg['PARAMs']['domain']
emailAddr = cfg['PARAMs']['email']

global counter 
counter = 0
def getSectionDetails():
    url = "https://banner.rowan.edu/reports/reports.pl"
    
    package = {
        "term": cfg['PARAMs']['termcode'],
        "task": "Section_Tally",
        "dept": cfg['PARAMs']['dept'],
        "Search": "Search"
    }
    browser = {
        "User-Agent": "Mozilla/5.0"
    }

    CRN = cfg['PARAMs']['crn']

    try:
        response = requests.post(url, data=package, headers=browser)
        response.raise_for_status()
        html = response.text
        
        row_regex = re.compile(
            fr"<tr[^>]*>\s*<td[^>]*>\s*<a[^>]*>\s*{CRN}\s*</a>\s*</td>[\s\S]*?</tr>", re.IGNORECASE
        )
        row_match = row_regex.search(html)
        if not row_match:
            print("CRN not found")
            return None
        
        # Scrape the course
        row = row_match.group(0)
        cell_regex = re.compile(r"<td[^>]*>(.*?)<\/td>", re.IGNORECASE)
        cells = [re.sub(r"<[^>]+>", "", cell).replace("&nbsp;", " ").strip() for cell in cell_regex.findall(row)]
        
        openSpots = int(cells[16]) if cells[16].isdigit() else 0
        totalSpots = (int(cells[15]) if cells[15].isdigit() else 0) + openSpots
        prof = cells[7] # ROLL PROFS

        result = f"Professor: {prof}\nSpots: {openSpots}/{totalSpots}"
        print(result)
        return {
            "professor": prof,
            "openSpots": openSpots,
            "totalSpots": totalSpots
        }

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

    
def sendEmail(openSpots, totalSpots):
    global counter
    url = f"https://api.mailgun.net/v3/{mailgunDomain}/messages"

    if counter > 2:
        counter = 0

    if openSpots >= 1:
        subject = "COURSE SPOT HAS OPENED UP"
        message = f"SectionTally UPDATE\nSpots: {openSpots}/{totalSpots}"
    else:
        subject = "SectionTally Monitor (Daily Update)"
        message = f"Course Monitor\nSpots: {openSpots}/{totalSpots}"

    emailContents = {
        "from": f"SectionTally Bot <mailgun@{mailgunDomain}>",
        "to": emailAddr,
        "subject": subject,
        "text": message
    }
    auth = ("api", mailgunAPI)
    try:
        response = requests.post(url, auth=auth, data=emailContents)

        if response.status_code == 200:
            print("Email sent!")
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except requests.RequestException as e:
        print(f"Error: {e}")

def spotCheck():
    global counter
    counter += 1
    section_data = getSectionDetails()
    if section_data:
        openSpots = section_data['openSpots']
        totalSpots = section_data['totalSpots']
        
        if openSpots > 0:
            sendEmail(openSpots, totalSpots)
        elif counter > (60 * 24) or counter == 1:
            sendEmail(openSpots, totalSpots)

    print("Total Count: ", counter)

schedule.every(1).minute.do(spotCheck)

while True:
    schedule.run_pending()
    time.sleep(1)
