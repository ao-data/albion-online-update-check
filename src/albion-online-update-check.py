import urllib.request
from bs4 import BeautifulSoup
import requests
import os

def getVersionAndLink():
    url = "https://albiononline.com/en/changelog"
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()

    soup = BeautifulSoup(mystr, 'html.parser')

    changelog_title_path = ".content__body--updates h2"
    changelog_title = soup.select(changelog_title_path)[0].text

    changelog_link_path = ".sidebar-item--active a"
    changelog_link = "https://albiononline.com%s" % soup.select(changelog_link_path)[0]['href']

    return [changelog_title, changelog_link]


def sendDiscordWebhook(content):
    data = {"content": content}
    requests.post(os.environ.get('DISCORD_WEBHOOK_URL'), json=data)

def isUpdated():
    # get current title and url of changelogs
    title, url = getVersionAndLink()
    thisUpdate = "%s - %s" % (title, url)

    # local file to keep track of the last changelog title and url
    path = "%s/config/lastupdate.txt" % os.path.dirname(__file__)
    
    # does the local file exist?
    if os.path.exists(path):
        # read the file
        f = open(path, "r")
        lastUpdate = f.read()
        f.close()
    else:
        # file doesn't exist, so we suggest this is the first run
        lastUpdate = "First Run"


    # bail if there's no difference, we don't want to send any messages.
    if thisUpdate == lastUpdate:
        print("There has not been an update to Albion Online since the last check.")
        return

    additionalContent = os.environ.get('ADDITIONAL_MESSAGE_CONTENT')
    if additionalContent == None:
        additionalContent = ""

    content = "Albion Online had an update! %s. %s" % (thisUpdate, additionalContent)
    print(content)

    # write the latest changelog url+title to the local file
    f = open(path, "w")
    lastUpdate = f.write(thisUpdate)
    f.close()

    # send a message to discord
    sendDiscordWebhook(content)

isUpdated()
