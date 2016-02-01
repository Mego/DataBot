# The commands listed in this file can be read and loaded as a Module into a MetaModule by the load_module() function

# Add necessary import to this file, including:
# from Module import Command
from Module import Command
import urllib.parse, requests, re, multiprocessing

# import SaveIO # For if you want to save and load objects for this module.
# save_subdir = '<subdir_name>' # Define a save subdirectory for this Module, must be unique in the project. If this is not set, saves and loads will fail.
# SaveIO.save(<object>, save_subdir, <filename>)  # Saves an object, filename does not need an extension.
# SaveIO.load(save_subdir, <filename>)  # Loads and returns an object, filename does not need an extension.

# def on_bot_load(bot): # This will get called when the bot loads (after your module has been loaded in), use to perform additional setup for this module.
#     pass

# def on_bot_stop(bot): # This will get called when the bot is stopping.
#     pass

# def on_event(event, client, bot): # This will get called on any event (messages, new user entering the room, etc.)
#     pass

pool = None

def on_bot_load(bot):
    pass
    #global pool
    #pool = multiprocessing.Pool()

# Logic for the commands goes here.
#
# def <command exec name>(cmd, bot, args, msg, event): # cmd refers to the Command you assign this function to
#     return "I'm in test1"
#
# def <command exec name>(cmd, bot, args, msg, event): # cmd refers to the Command you assign this function to
#     return "I'm in test1"
#
# ...

def cmd_eval(cmd, bot, args, msg, event):
    if len(args) < 2:
        return 'Syntax: !eval <language name> "<code>" "[input]": Error: not enough arguments: got {}'.format(args)
    lang = args[0].lower()
    # http://stackoverflow.com/a/1177542/2508324
    # args = list(map(lambda x: x.encode('raw_unicode_escape').decode('utf-8'), args))
    print(args)
    #if lang.lower() == 'python':
    #    code = args[1]
    #    return eval(code)
    # Causes dangerous code.
    code = ''
    cinput = ''
    cargs = '+'
    # args support?
    #av = ''
    av = ' '.join(args[1:]).replace(r'\\', '\ufff8').replace(r'\"', '\ufff7').replace(r"\'", '\uffff')
    res = re.findall(r'"([^"]*)"', av)
    print(res)
    if res:
        code = res[0].replace('\ufff7', '"').replace("\uffff", "'").replace('\ufff8', r'\\')
        cinput = res[1].replace('\ufff7', '"').replace("\uffff", "'").replace('\ufff8', r'\\') if len(res)>1 else ''
        cargs = "+".join(list(map(lambda a : urllib.parse.quote(a, safe="'/"), res[2:])))
    print(code, cinput, cargs)
    url = "http://{}.tryitonline.net/cgi-bin/backend".format(lang)
    req = "code={}&input={}&args={}&debug=on".format(urllib.parse.quote(code, safe="'/"), urllib.parse.quote(cinput, safe="'/"), cargs)
    print(req)
    #pool.apply_async(sub_eval, (bot, msg, url, req))
    try:
        return requests.post(url, data=req).text[33:]
    except:
        return "Something went wrong with your request, sorry! Are you sure that language is on Try It Online?"


def sub_eval(bot, msg, url, req):
    res = requests.post(url, data=req).text[33:]
    return res

commands = [  # A list of all Commands in this Module.
    Command('eval', cmd_eval, 'runs code', allowed_chars=None),
    # Command( '<command name>', <command exec name>, '<help text>' (optional), <needs privilege> (= False), <owner only> (= False), <special arg parsing method>(*) (= None), <aliases> (= None), <allowed chars> (= string.printable), <disallowed chars> (= None) (**) ),
    # Command( '<command name>', <command exec name>, '<help text>' (optional), <needs privilege> (= False), <owner only> (= False), <special arg parsing method>(*) (= None), <aliases> (= None), <allowed chars> (= string.printable), <disallowed chars> (= None) (**) ),
    # ...
]

# (*) <special arg parsing method> = Some commands require a non-default argument parsing method.
# Pass it there when necessary. It must return the array of arguments.

# (**) Allowed and disallowed chars
# You can choose to allow/disallow a specific set of characters in the command's arguments.
# By default, the allowed chars is string.printable (see https://docs.python.org/3/library/string.html#string-constants for string constants).
# If a char is both allowed and disallowed, disallowed has higher importance.
# If allowed_chars is None, all chars are allowed (unless those specified in disallowed_chars).

# module_name = "<name used to address this module>"
