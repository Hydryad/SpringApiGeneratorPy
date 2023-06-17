# imports

# sourcery skip: ensure-file-closed
import json
import re
import requests
import os
import sys
import pprint
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# get a list of wiki page names

# scrape the wiki pages, and ideally have this data cached locally to minimize calls+

# Create a class to represent each lua function and its args


# needs to have a list of args
# needs to have a description
# needs to identify the module
# have a way to access various data from within, such as friendly name, the full function name

        
    
    

recoilApiUrl = "https://beyond-all-reason.github.io/spring/"

# req = requests.get(recoilApiUrl)
# print(req)

# print(req.content)

# using local copy paste to save hammering the server while testing
# soup = BeautifulSoup(req.content, "html.parser")
soup = BeautifulSoup()

# beautiful soup has a few functions we want to take advantage of here,
# find_all, find, find_next, find_next_sibling, find_parent, find_parents, find_previous, 
# find_previous_sibling and find_all_previous are all useful for navigating the tree
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#navigating-the-tree

sub_URL_pat = r"(?P<suburl>/\w+/\w+/modules/(\w+\.html))"
m = re.compile(sub_URL_pat)
reModule = re.compile(r"(?P<module>\w*)\.\w*$")

print(soup.prettify())

base_URL = 'https://beyond-all-reason.github.io/spring/lua-api'
urlList = []
baseUrlList = []

# regex to extract basic module name


for link in soup.find_all('a'):
    print(urljoin(base_URL, link.get('href')))
    if m.match(link.get('href')):
        urlList.append(urljoin(base_URL, link.get('href')))
        baseUrlList.append(link.get('href'))
        print(link.get('href'))

# once we have parse per page, put a for loop to run it on all pages here


# parse page and extract the function names first.


for urls in urlList:
        thisURL = reModule.search(urls)["module"]
        thisURL += ".html"
        outf = open(thisURL, "+w")
        outf.writelines(BeautifulSoup(requests.get(urls).text, "html").prettify())
        outf.close()
        


# for link in soup.find_all("a", string=re.compile(sub_URL_pat)):
#     print(link.get())
#     print("found something")