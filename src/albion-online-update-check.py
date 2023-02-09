import urllib.request
# from bs4 import BeautifulSoup
import requests
import os
import xmltodict

def getWin32FullInstallFilename():
    url = "https://live.albiononline.com/autoupdate/manifest.xml"
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    xmldata = mybytes.decode("utf8")
    fp.close()

    fullInstallFilename = xmltodict.parse(xmldata)['patchsitemanifest']['albiononline']['win32']['fullinstall']['@file']

    return fullInstallFilename


def sendDiscordWebhook(content):
    data = {"content": content}
    requests.post(os.environ.get('DISCORD_WEBHOOK_URL'), json=data)

def isUpdated():
    # get current title and url of changelogs
    fullInstallFilename = getWin32FullInstallFilename()
    thisUpdate = fullInstallFilename

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

    content = "Albion Online had an update! Win32 Full Installer Filename %s. %s" % (thisUpdate, additionalContent)
    print(content)

    # write the latest changelog url+title to the local file
    f = open(path, "w")
    lastUpdate = f.write(thisUpdate)
    f.close()

    # send a message to discord
    sendDiscordWebhook(content)

if os.environ.get('DISCORD_WEBHOOK_URL') is None or os.environ.get('DISCORD_WEBHOOK_URL') == "":
    print("Environment variable DISCORD_WEBHOOK_URL must be set.")
    exit(1)

isUpdated()
