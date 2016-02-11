# The commands listed in this file can be read and loaded as a Module into a MetaModule by the load_module() function

# Add necessary import to this file, including:
# from Module import Command
from Module import Command
import ast, multiprocessing, os, re, requests, subprocess, tempfile, traceback, urllib.parse, urllib.request

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

def parse_eval(cmd):
    try:
        print(cmd)
        cmd_name_end = cmd.index(" ")+1
        index = cmd.index(" ",cmd_name_end)
        # http://stackoverflow.com/a/249937/2508324
        return [cmd[cmd_name_end:index]] + re.findall(r'"(?:[^"\\]|\\.)*"', cmd[index+1:], re.DOTALL)
    except:
        traceback.print_exc()
        return False
        
def run_subprocess(cinput, invoke, universal_newlines=True, **kwargs):
    process = subprocess.Popen(invoke, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=universal_newlines, **kwargs) 
    try:
        result = process.communicate(input=cinput, timeout=60)[0]
    except subprocess.TimeoutExpired:
        process.kill()
        result = "Sorry, your code took too long to run!"
        partial_out = process.communicate()[0] # communicate returns a tuple first element is stdout second is stderr
        if partial_out:
            result += "\nPartial output:\n" + partial_out
    except:
        traceback.print_exc()
        result = "There was an issue running your code."
    return result
        
#temporary workaround while TIO is bugged
def run_seriously(code, cinput):
    cp437table = ''.join(map(chr,range(128))) + u"ÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜ¢£¥₧ƒáíóúñÑªº¿⌐¬½¼¡«»░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀αßΓπΣσµτΦΘΩδ∞φε∩≡±≥≤⌠⌡÷≈°∙·√ⁿ²■ "
    if any([x not in cp437table for x in code]):
        return "Error: non-CP437 characters detected in code."
    code = ''.join(map(lambda c:"{:02x}".format(c), code.encode('cp437')))
    return run_subprocess(cinput.encode(), ["python2", "/home/ubuntu/workspace/INTERPRETERS/Seriously/seriously.py", '-i', '-x', '-c', code], universal_newlines=False).decode('cp437')
    
        
def run_marbelous(code, cinput):
    file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    file.write(code)
    file.close()
    result = run_subprocess(cinput, ["/home/ubuntu/workspace/INTERPRETERS/marbelous.py-master/marbelous/marbelous.py", file.name])
    os.remove(file.name)
    return result
    
def run_pyth(code, cinput):
    return run_subprocess(cinput, ["/home/ubuntu/workspace/INTERPRETERS/pyth/pyth.py", '--safe', '-c', code])
    
def run_japt(code, cinput):
    return run_subprocess(None, ["/home/ubuntu/workspace/spidermonkey/js", '/home/ubuntu/workspace/INTERPRETERS/japt.js', code, cinput])
        
non_tio_langs = {
    "pyth":run_pyth,
    "marbelous":run_marbelous,
    "seriously":run_seriously,
    "japt":run_japt,
}

lang_synonyms = {
    "bf":"brainfuck",
    "///":"slashes",
}

def cmd_eval_debug(cmd, bot, args, msg, event):
    return cmd_eval(cmd, bot, args, msg, event, debug=True)

def cmd_eval(cmd, bot, args, msg, event, debug=False):
    if len(args) < 2:
        return 'Syntax: !eval <language name> "<code>" "[input]" "[args1]" "[args2]"...: Error: not enough arguments: got {}'.format(args)
    lang = args[0].lower()
    print(args)
    code = ''
    cinput = ''
    cargs = '+'
    result = ""
    res = list(map(lambda a:ast.literal_eval(a),args[1:]))
    print(res)
    if res:
        code = res[0]
        cinput = res[1] if len(res)>1 else ''
        cargs = "+".join(list(map(lambda a : urllib.parse.quote(a), res[2:]))) if len(res)>2 else ''
    print(code, cinput, cargs)
    if lang in non_tio_langs:
        result = non_tio_langs[lang](code, cinput)
    else:
        if lang in lang_synonyms:
            lang = lang_synonyms[lang]
        url = "http://{}.tryitonline.net/cgi-bin/backend".format(lang)
        req = "code={}&input={}".format(urllib.parse.quote(code), urllib.parse.quote(cinput))
        if debug:
            req += "&debug=on"
        if len(args) > 2:
          req += "&args={}".format(cargs)
        try:
            result = requests.post(url, data=req).text[33:] # maybe find a way to figure out if there was a timeout on TIO
        except:
            traceback.print_exc()
            return "Something went wrong with your request, sorry! Are you sure that language is on Try It Online?"
            
    result = result or "<no output>" # ugly :P CR would disapprove #golfier #pythonic #lelplebian
    return result


def sub_eval(bot, msg, url, req):
    res = requests.post(url, data=req).text[33:]
    return res
    
def cmd_langs(cmd, bot, args, msg, event):
    langs = None
    with urllib.request.urlopen('http://tryitonline.net') as req:
        langs = re.findall(r'<li><a href="//(.+).tryitonline.net/">.*</a></li>', req.read().decode())
    langs.extend([lang for lang in non_tio_langs if lang not in langs])
    return 'Languages supported: {}'.format(', '.join(sorted(langs)).strip())

commands = [  # A list of all Commands in this Module.
    Command('eval', cmd_eval, 'eval:\n\tEvaluates code through http://tryitonline.net backend.\n\tSyntax: Syntax: !eval <language name> "<code>" "[input]" "[args1]" "[args2]"...', special_arg_parsing = parse_eval, allowed_chars=None),
    Command('evaldebug', cmd_eval_debug, 'eval:\n\tEvaluates code through http://tryitonline.net backend, with debugging on.\n\tSyntax: Syntax: !evaldebug <language name> "<code>" "[input]" "[args1]" "[args2]"...', special_arg_parsing = parse_eval, allowed_chars=None),
    Command('langs', cmd_langs, 'langs:\n\tOutputs the list of supported languages for the eval command.'),
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

module_name = "EvalModule"
