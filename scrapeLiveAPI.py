# get a list of wiki page names

# scrape the wiki pages, and ideally have this data cached locally to minimize calls+

# Create a class to represent each lua function and its args


# needs to have a list of args
# needs to have a description
# needs to identify the module
# have a way to access various data from within, such as friendly name, the full function name
import requests
from bs4 import BeautifulSoup


import re
from urllib.parse import urljoin


def scrapeLiveAPI():
    recoilApiUrl = "https://beyond-all-reason.github.io/spring/"
    req = requests.get(recoilApiUrl)
    soup = BeautifulSoup(req.content, "html.parser")
    sub_URL_pat = r"(?P<suburl>/\w+/\w+/modules/(\w+\.html))"
    m = re.compile(sub_URL_pat)
    reModule = re.compile(r"(?P<module>\w*)\.\w*$")

    print(soup.prettify())

    base_URL = 'https://beyond-all-reason.github.io/spring/lua-api'
    urlList = []
    baseUrlList = []

    for link in soup.find_all('a'):
        print(urljoin(base_URL, link.get('href'))) # appends hardcoded base_URL to the parsed relative path
        if m.match(link.get('href')): # if we match sub_URL_pat, add to list baseUrlList
            urlList.append(urljoin(base_URL, link.get('href')))
            baseUrlList.append(link.get('href'))
            print(link.get('href'))

    # once we have parse per page, put a for loop to run it on all pages here


    # parse page and extract the function names first.
    def getThisUrl(reModule, url):
        thisURL = reModule.search(url)["module"]
        thisURL += ".html"
        return thisURL

    for urls in urlList:
        thisURL = getThisUrl(reModule, urls)
        with open(thisURL, "+w") as outf:
            outf.writelines(BeautifulSoup(requests.get(urls).text, "html").prettify())