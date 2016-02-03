import os
import requests
import urllib.parse
from xml.etree import ElementTree
from Module import Command

save_subdir = 'define'
module_name = 'define'

api_key = ""

def command_define(cmd, bot, args, msg, event):
    if len(args) != 1:
        return "1 argument expected"
    if api_key is None or api_key == "":
        return "No API key found. Contact the bot owner."
    word = args[0]
    xml_response = requests.get("http://www.dictionaryapi.com/api/v1/references/sd4/xml/" + urllib.parse.quote_plus(word) + "?key=" + api_key).text
    root = ElementTree.fromstring(xml_response)
    entries = []
    for entry in root.iter('entry'):
        if entry.attrib['id'].split('[')[0] == word:
            entries.append(entry)
    if len(entries) == 0:
        return "No entries found for that word."
    output = ["Definition from Merriam-Webster:"]
    for entry in entries:
        fl = entry.find('fl').text
        hw = entry.find('hw')
        if 'hindex' in hw.attrib:
            hindex = hw.attrib['hindex']
        else:
            hindex = '1'
        output.append(u"{}. {}".format(hindex, fl))
        for dt in entry.iter('dt'):
            definition = dt.text[1:].strip()
            if definition != "":
                output.append(u"- {}".format(definition))
    return os.linesep.join(output)


def on_bot_load(bot):
    global api_key
    if not os.path.isfile("botdata/define/dictionaryapi_key.txt"):
        print("[define] WARNING: No Merriam-Webster API Key found for the definition module. Put one in botdata/define/dictionaryapi_key.txt")
        return
    with open("botdata/define/dictionaryapi_key.txt") as f:
        api_key = f.read().strip()
    resp_text = requests.get("http://www.dictionaryapi.com/api/v1/references/sd4/xml/test?key=" + api_key).text
    if resp_text.startswith("Invalid"):
        print("[define] WARNING: Merriam-Webster API Key is invalid.")
        api_key = ""

commands = [
    Command('define', command_define, 'Looks up a word in the Merriam-Webster dictionary API.', False, False, None, None)
]