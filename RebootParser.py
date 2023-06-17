# imports

import json
import re
import requests
import os
import pprint
from bs4 import BeautifulSoup



# get a list of wiki page names

# scrape the wiki pages, and ideally have this data cached locally to minimize calls+

# Create a class to represent each lua function and its args


# needs to have a list of args
# needs to have a description
# needs to identify the module
# have a way to access various data from within, such as friendly name, the full function name

recoilApiUrl = "https://beyond-all-reason.github.io/spring/"

req = requests.get(recoilApiUrl)
print(req)

print(req.content)

soup = BeautifulSoup(req.content, "html.parser")

# beautiful soup has a few functions we want to take advantage of here,
# find_all, find, find_next, find_next_sibling, find_parent, find_parents, find_previous, 
# find_previous_sibling and find_all_previous are all useful for navigating the tree
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#navigating-the-tree

sub_URL_pat = r"(?P<suburl>/\w+/\w+/modules/(\w+\.html))"

print(soup.prettify())

# for link in soup.find_all('a'):
#     print(link.get('href'))

for link in soup.find_all("a", string=re.compile(sub_URL_pat)):
    print(link.get())
    print("found something")
