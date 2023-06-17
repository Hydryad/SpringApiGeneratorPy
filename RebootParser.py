# imports

# sourcery skip: ensure-file-closed
import json
import os
import sys
import pprint
import scrapeLiveAPI
from dataclasses import dataclass

# for link in soup.find_all("a", string=re.compile(sub_URL_pat)):
#     print(link.get())
#     print("found something")



# scrapeLiveAPI.scrapeLiveAPI() # uncomment to pull a fresh copy of the website

# we now have html files cached locally, we need to start parsing the functions.
# I am currently thinking I want to directly output the functions as the text I neec
# I could also possibly make a class to represent the functions
type.

@dataclass
class ApiPassedParameter:
    optional: bool # is this parameter optional? Will mark the @param in lua as such
    param_Name: str # name of parameter, i.e unitID
    return_Param_Types: list = ["Nil"] # using a str to represent the Lua expected parameter value(s). TODO: We need to handle nil
    
    

@dataclass
class APIDocElement:
    apiCategory: str # Is this a constant | function | something else
    functionPrefix: str # optional, if present will be appended to the beginning of the function, i.e Spring will add Spring., GL will add GL.
    func_Arg_Type_Pair: dict # pairs of arguments, will be collated
    # func_Pair_List could be separated into optional and non-optional.
    # optional parameters are typically passed at the end.
    # might be beneficial to have a parameter class indicatin
    func_Pair_List: list # might make this a list of tuples
    
    