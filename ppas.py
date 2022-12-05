from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import plyer.platforms.win.notification
from plyer import notification
from time import strftime
import time
import os

location =  [
                "cebu", 
                "08-temp-offsite-sm-seaside-cebu"
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

def current_time():
    return strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())

def notif_if_available(location, is_avail, details):
    if (is_avail == True):
        notification.notify(
            title     = location,
            message   = f"Slots Found: {details[1]}\nEarliest Date: {details[2]}"
        )
        print(current_time() + "Available in " + location)

def log_results(location):
    log_path = os.path.expanduser('~/Documents') + "\\ppas.log"
    
    with open(log_path, 'a') as f:
        f.write(current_time() + location.upper() + ": Available" + "\n")
        
def display_error_once(error):
    if error == False:
        print("ERROR: Attempting to reconnect..")
    return True
    
def execute(location):
    content = access_html_content(location)
    result = availability_result(content)
    availability = availability_to_bool(result[0])
    notif_if_available(location, availability, result)
    if availability == True:
        log_results(location)

if __name__ == "__main__":
    error = False
    while True:
        try:
            urlopen('https://google.com') # checks internet connection
            error = False
            print("Script is running..")
            while True:
                for index in range(len(location)):
                    execute(location[index])
                time.sleep(5)
        except KeyboardInterrupt:
            print("Stopping script..")
            break
        except Exception:
            error = display_error_once(error)
            time.sleep(300)