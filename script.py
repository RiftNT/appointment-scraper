from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from pynotifier import Notification
import time

# Refer locations here: https://dfacalendar.netpinoy.com/philippines/
location =  [
                "cebu", 
                "08-temp-offsite-sm-seaside-cebu",
            ]

def access_html_content(location):
    req = Request(
            url = f'https://dfacalendar.netpinoy.com/philippines/{location}',
            headers = {'User-Agent': 'Mozilla/5.0'}
        )
    content = urlopen(req).read()
    return content

def availability_to_bool(availability):
    if availability == " Available":
        return True
    else:
        return False
    
def availability_result(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    schedWrapper = soup.find_all("div", {"aria-label": "schedule-results-wrapper"})
    for tag in schedWrapper:
        tags = tag.find_all("p")
    availability = tags[0].contents[0].text
    
    if (availability_to_bool(availability) == True):
        slots_found = tags[1].contents[1].text
        earliest_date = tags[2].contents[1].text
        details = [availability, slots_found, earliest_date]
    else:
        details = [availability]
    return details

def notif_if_available(location, is_avail, details):
    if (is_avail == True):
        Notification(
            title       = location,
            description = f"Slots Found: {details[1]}\nEarliest Date: {details[2]}",
            duration    = 5
        ).send()

def log_results(location, result):
    with open('.\\appointment-scraper\\log.txt', 'a') as f:
        f.write(location.upper() + ": " + result + "\n")

def execute(location):
    content = access_html_content(location)
    result = availability_result(content)
    availability = availability_to_bool(result[0])
    notif_if_available(location, availability, result)
    log_results(location, result[0])

if __name__ == "__main__":
    while True: # To end the script, press CTRL + C
        for index in range(len(location)):
            execute(location[index])
        time.sleep(300)