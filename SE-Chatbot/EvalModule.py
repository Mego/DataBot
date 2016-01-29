# The commands listed in this file can be read and loaded as a Module into a MetaModule by the load_module() function

# Add necessary import to this file, including:
# from Module import Command
from Module import Command
import urllib.parse, requests

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
    print(args)
    if len(args) < 2:
        return "Syntax: !eval <language name> <code>: Error: not enough arguments: got {}".format(args)
    lang = args[0]
    code = args[1]
    cinput = ''
    if len(args) > 2:
        cinput = args[3]
    url = "http://{}.tryitonline.net/cgi-bin/backend".format(lang)
    req = "code={}&input={}&debug=on".format(urllib.parse.quote(code, encoding='utf-8'), urllib.parse.quote(cinput))
    try:
        return requests.post(url, data=req).text[33:]
    except:
        return "Something went wrong with your request, sorry! Are you sure that language is on Try It Online?"


commands = [  # A list of all Commands in this Module.
    Command('eval', cmd_eval, 'runs code'),
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
