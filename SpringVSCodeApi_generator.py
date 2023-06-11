# This is a sample Python script.

import json
import urllib.request
import re
import os


# See
# https://studio.zerobrane.com/doc-api-auto-complete

wikiPageNames = [
    "Lua:Callins",
    "Lua_System",
    "Lua_ConstGame",
    "Lua_ConstEngine",
    "Lua_ConstPlatform",
    "Lua_ConstCOB",
    "Lua_SyncedCtrl",
    "Lua_SyncedRead",
    "Lua_UnsyncedCtrl",
    "Lua_UnsyncedRead",
    "Lua_OpenGL_Api",
    "Lua_GLSL_Api",
    "Lua_BitOps",
    "Lua_MathExtra",
]
baseURL = "https://springrts.com/mediawiki/api.php?action=query&prop=revisions&titles=%s&rvprop=content&formatversion=2&format=json"

apis = {}  # type: dict  # list of apis to export,
combinedCallinsDict = {
    "widget": {
        "type": "class",
        "description": "The widget handler, note that UnsyncedCtrl is not available from here",
        "childs": {},
    },
    "gadget": {
        "type": "class",
        "description": "The gadget handler, note that synced or unsynced is not available from here",
        "childs": {},
    },
}  # gonna be a table of addon:callout
prefixedCalloutsDict = {}
combinedConstantsDict = {}
globalfuncs = {}  # type: dict
reLuaCallin = re.compile(r"{{LuaCallin.*}}", re.MULTILINE)

htmlshit = re.compile(r"<.*?>")
typere = re.compile(r"{{type\|(.*?)}}")
bracketre = re.compile(r"{{bracket.*?}}")
rbracketre = re.compile(r"{{rbracket.*?}}")

morebadres = [re.compile(r"")]


def stripwikimarks(line):
    line = line.replace("{{pipe}}", "|")
    line = re.sub(typere, r"\1", line)  # r"\foo" is raw string notation, does not parse escape chars
    line = re.sub(bracketre, " [", line)
    line = re.sub(rbracketre, "] ", line)
    line = line.replace("[[", "[ [")
    line = line.replace("]]", "] ]")
    return line


def getFields(lines, pos):
    fields = {}
    lastkey = ""
    while pos < len(lines) and lines[pos].startswith("}}") == False:
        line = lines[pos]
        if line.startswith("|"):
            if "=" in line:
                kv = line.strip().strip("|").partition("=")
                lastkey = kv[0].strip().lower()
                if lastkey not in fields:
                    fields[lastkey] = kv[2].strip()
                else:
                    if lastkey == "info":
                        fields[lastkey] += "\n" + kv[2]
                    else:
                        fields[lastkey] += " " + kv[2]
            else:
                fields["info"] = line if "info" not in fields else fields["info"] + line
                print("unmarked | line:", line)
        elif lastkey == "info":
            fields[lastkey] += "\n" + line.strip()
        pos = pos + 1
    for key in fields.keys():
        fields[key] = re.sub(htmlshit, "", fields[key])
    return fields


def parseContents(parsedLines_f, wikiPageName):
    i = 0
    while i < len(parsedLines_f):
        activeParsedLine = parsedLines_f[i]
        if activeParsedLine.startswith("{{LuaCallout"):
            springLuaCallout = getFields(parsedLines_f, i + 1)
            # print('LuaCallout',callout)
            if "prefix" in springLuaCallout and len(springLuaCallout["prefix"]) > 0:
                apiStartPlusPeriod = springLuaCallout["prefix"].strip().strip(".")
                if apiStartPlusPeriod not in prefixedCalloutsDict:
                    prefixedCalloutsDict[apiStartPlusPeriod] = {"type": "lib", "description": apiStartPlusPeriod,
                                                                "childs": {}}
                combinedLuaCalloutDict = {"type": "function"}
                parsedSpringApiArgs = []
                for j in range(1, 10):  # j is iterating up to 10 args and placing them into the list or dict
                    argSelectedFromList = "arg%d" % j
                    if argSelectedFromList in springLuaCallout and len(springLuaCallout[argSelectedFromList]) > 0:
                        parsedSpringApiArgs.append(stripwikimarks(springLuaCallout[argSelectedFromList]))
                # args = ', '.join(args)
                # args = stripwikimarks(args)
                if len(parsedSpringApiArgs) > 0:
                    combinedLuaCalloutDict["args"] = parsedSpringApiArgs
                if "return" in springLuaCallout and len(springLuaCallout["return"]) > 0:
                    combinedLuaCalloutDict["returns"] = stripwikimarks(springLuaCallout["return"])
                parsedDescription = wikiPageName + "; "
                if "info" in springLuaCallout and len(springLuaCallout["info"]) > 0:
                    parsedDescription = parsedDescription + springLuaCallout["info"]
                combinedLuaCalloutDict["description"] = stripwikimarks(parsedDescription)
                if "returns" not in combinedLuaCalloutDict:
                    combinedLuaCalloutDict["returns"] = "nil"
                if "args" not in combinedLuaCalloutDict:
                    combinedLuaCalloutDict["args"] = ""
                prefixedCalloutsDict[apiStartPlusPeriod]["childs"][springLuaCallout["name"]] = combinedLuaCalloutDict
            else:
                print("no prefix for callout", springLuaCallout)
        if activeParsedLine.startswith("{{LuaConstant"):
            workingConstDict = getFields(parsedLines_f, i + 1)
            # print('LuaConstant',constant)
            if "." in workingConstDict["name"]:
                workingPrefix, _, curConstSuffix = workingConstDict["name"].partition(".")
                if workingPrefix not in combinedConstantsDict:
                    combinedConstantsDict[workingPrefix] = {
                        "type": "lib",
                        "Description": (workingPrefix + " from " + wikiPageName),
                        "childs": {},
                    }
                combinedConstantsDict[workingPrefix]["childs"][curConstSuffix] = {"type": "value"}
                if "info" in workingConstDict and len(workingConstDict["info"]) > 0:
                    combinedConstantsDict[workingPrefix]["childs"][curConstSuffix]["description"] = stripwikimarks(
                        workingConstDict["info"]
                    )
                if "type" in workingConstDict and len(workingConstDict["type"]) > 0:
                    combinedConstantsDict[workingPrefix]["childs"][curConstSuffix]["valuetype"] = stripwikimarks(
                        workingConstDict["type"]
                    )
        if activeParsedLine.startswith("{{LuaCallin"):
            workingCallinDict = getFields(parsedLines_f, i + 1)
            workingLuaCallin = {"type": "method"}
            if "info" in workingCallinDict and len(workingCallinDict["info"]) > 0:
                workingLuaCallin["description"] = stripwikimarks(workingCallinDict["info"])
            if "args" in workingCallinDict and len(workingCallinDict["args"]) > 0:
                workingLuaCallin["args"] = stripwikimarks(workingCallinDict["args"])
            else:
                workingLuaCallin["args"] = ""
            if "return" in workingCallinDict and len(workingCallinDict["return"]) > 0:
                workingLuaCallin["returns"] = stripwikimarks(workingCallinDict["return"])
            else:
                workingLuaCallin["returns"] = "nil"
            # print('LuaCallin',callin)
            combinedCallinsDict["widget"]["childs"][workingCallinDict["name"]] = workingLuaCallin
            combinedCallinsDict["gadget"]["childs"][workingCallinDict["name"]] = workingLuaCallin
        i = i + 1


def get_pageContents(wikiFunctionScopePrefix):  # passed wikiPageNames here
    if os.path.exists(wikiFunctionScopePrefix.replace(":", "_") + ".json"):
        print("Found cache for ", wikiFunctionScopePrefix)
        content = open(wikiFunctionScopePrefix.replace(":", "_") + ".json").read()

    else:
        with urllib.request.urlopen(baseURL % wikiFunctionScopePrefix) as response:
            jayson = response.read()
            jayson = json.loads(jayson)
            print(jayson)
            content = jayson["query"]["pages"][0]["revisions"][0]["content"]
            outf = open(wikiFunctionScopePrefix.replace(":", "_") + ".json", "w")
            outf.write(content)
            outf.close()
            print(content)
    parsedLines = content.splitlines()
    parseContents(parsedLines, wikiFunctionScopePrefix)


# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f"Hi, {name}")  # Press Ctrl+F8 to toggle the breakpoint.


def recursecreatetable(tableRCC, subTable, depth=0):
    for subtableKey, subtableValue in subTable.items():
        if type(subtableValue) is dict:
            tableRCC.append("\t" * depth + subtableKey + " = {")
            recursecreatetable(tableRCC, subtableValue, depth + 1)
            tableRCC.append("\t" * depth + "},")
        elif type(subtableValue) is list:
            tableRCC.append(
                "\t" * depth + subtableKey + " = " + "'" + ", ".join([str(v2) for v2 in subtableValue]) + "',"
            )
        else:
            if subtableKey == "description":
                tableRCC.append("\t" * depth + subtableKey + " = " + "[[" + subtableValue + " ]],")
            else:
                tableRCC.append("\t" * depth + subtableKey + " = " + "'" + subtableValue + "',")
    return tableRCC


# ----- Hydryad working defs begin


def VSCodeAnnoSplitLines(filename):
    content = open(filename).read()
    # jstest = content
    # jstest = json.loads(jstest)
    # content = jstest["query"]["pages"][0]["revisions"][0]["content"]
    lines = content.splitlines(keepends=True)
    outf = open("RawJsonSplitlineTestOutputBeforeStrip.txt", "w")
    print("Line length in testSplitLines: " + str(len(lines)))
    outf.writelines(lines)
    outf.close()
    for i, x in enumerate(lines, start=0):
        lines[i] = stripwikimarks(x)

    outf = open("RawJsonSplitlineTestOutput.txt", "w")
    print("Line length in testSplitLines: " + str(len(lines)))
    outf.writelines(lines)
    outf.close()


# ----- End of Hydryad Working Defs
# ----- Begin main below
# Press the green button in the gutter to run the script.
if True:  # __name__ == '__main__':
    # print_hi("PyCharm")
    get_pageContents(wikiPageNames[0])
    # exit(1)
    for pn in wikiPageNames:
        get_pageContents(pn)
        # time.sleep(1)
    del combinedConstantsDict["Spring"]
    # Testing Code
    
    
    
    
    # End testing code
    # For all the callouts, add the shorthand versions too!
    tableWithAllData = ["return {"]
    tableWithAllData = recursecreatetable(tableWithAllData, prefixedCalloutsDict, 1)
    tableWithAllData = recursecreatetable(tableWithAllData, combinedCallinsDict, 1)
    tableWithAllData = recursecreatetable(tableWithAllData, combinedConstantsDict, 1)
    for membername, value in prefixedCalloutsDict["Spring"]["childs"].items():
        recursecreatetable(tableWithAllData, {"sp" + membername: value}, 1)
    for membername, value in prefixedCalloutsDict["gl"]["childs"].items():
        recursecreatetable(tableWithAllData, {"gl" + membername: value}, 1)
    tableWithAllData.append("}")
    # print('\n'.join(mytable))
    VSCodeAnnoSplitLines(r"C:\Users\Matthew\Python Learnin\Lua_SyncedCtrl.json")
    outf = open("springVSCodeapi.lua", "w")
    outf.write("\n".join(tableWithAllData))
    outf.close()
    





# if True:  # __name__ == '__main__':
#     # print_hi("PyCharm")
#     get_pageContents(wikiPageNames[0])
#     # exit(1)
#     for pn in wikiPageNames:
#         get_pageContents(pn)
#         # time.sleep(1)
#     del constants["Spring"]

#     # For all the callouts, add the shorthand versions too!
#     mytable = ["return {"]
#     mytable = recursecreatetable(mytable, callouts, 1)
#     mytable = recursecreatetable(mytable, callins, 1)
#     mytable = recursecreatetable(mytable, constants, 1)
#     for membername, value in callouts["Spring"]["childs"].items():
#         recursecreatetable(mytable, {"sp" + membername: value}, 1)
#     for membername, value in callouts["gl"]["childs"].items():
#         recursecreatetable(mytable, {"gl" + membername: value}, 1)
#     mytable.append("}")
#     # print('\n'.join(mytable))
#     VSCodeAnnoSplitLines(r"C:\Users\Matthew\Python Learnin\Lua_SyncedCtrl.json")
#     outf = open("springVSCodeapi.lua", "w")
#     outf.write("\n".join(mytable))
#     outf.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
