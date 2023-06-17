# imports

# sourcery skip: ensure-file-closed
import json
import os
import sys
import pprint
import scrapeLiveAPI
import pathlib
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass, field

@dataclass
class ApiPassedParameter:
    optional: bool # is this parameter optional? Will mark the @param in lua as such
    param_Name: str # name of parameter, i.e unitID
    Param_Types: list = field(default_factory=list) # using a str to represent the Lua expected parameter value(s). TODO: We might need to handle nil special

@dataclass
class APIDocElement:
    apiCategory: str # Is this a constant | function | something else
    functionPrefix: str # optional, if present will be appended to the beginning of the function, i.e Spring will add Spring., GL will add GL.
    func_Arg_Type_Class: list # arguments, pass this ApiPassedParameter dataclass
    # func_Pair_List could be separated into optional and non-optional.
    # optional parameters are typically passed at the end.
    # might be beneficial to have a parameter class indicatin
    func_Pair_List: list = field(default_factory=list["None"]) # might make this a list of tuples

# what logic can I use to parse each argument, and obtain a count?

# Testing code:
paramsTemp = ApiPassedParameter(optional= False, param_Name= "unitDefName",Param_Types=["String", "Number"])
testc = APIDocElement("Function", "Spring", paramsTemp)

print(testc)

localCopyPath = "SyncedCtrl.html" # turn into a list of all
fpath = Path.cwd() # non testing code, gets where our script is running as a path
htmlFilePaths = list(Path(fpath).glob('*.html'))
pprint.pprint(htmlFilePaths)
#fdpath = os.path.join(fpath, localCopyPath) # combine with hardcoded localCopyPath, we can make a list of files and loop perhaps
h3TagsAndCodeExample = {"Foo": "Bar"}

# demo code turning into prod code, was initially to test pulling h3.
# should possibly try to pull a broader scope

with open(htmlFilePaths[21], "r") as inputF2:
    soup = BeautifulSoup(inputF2, 'html.parser')
    strained = soup.select('h3 ~ .code-example')
    
    pprint.pprint(strained, compact=True, width=200)

with open(htmlFilePaths[21], "r") as inputF:
    soup = BeautifulSoup(inputF, 'html.parser')
    h3tags = soup.find_all("h3")
    for thisTag in h3tags:
        if thisTag.get('id'):
            h3TagsAndCodeExample[thisTag['id']] = {"Name": thisTag['id']}
    pprint.pprint(h3TagsAndCodeExample)
    pprint.pprint(h3tags, compact=True, indent=4)
    print(soup.prettify())
    print("Wait!")