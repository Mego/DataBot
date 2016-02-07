from Module import Command
from Config import Config
import ast, os, re, requests, subprocess, tempfile, traceback, urllib.parse, urllib.request

def parse_eval(cmd):
    try:
        if cmd.startswith("eval "):
            index = cmd.index(" ",5)
            # http://stackoverflow.com/a/249937/2508324
            return [cmd[5:index]] + re.findall(r'"(?:[^"\\]|\\.)*"', cmd[index+1:], re.DOTALL)
        elif cmd.startswith("evaldebug "):
            index = cmd.index(" ",10)
            # http://stackoverflow.com/a/249937/2508324
            return [cmd[10:index]] + re.findall(r'"(?:[^"\\]|\\.)*"', cmd[index+1:], re.DOTALL)
        elif cmd.startswith("e "):
            index = cmd.index(" ",2)
            # http://stackoverflow.com/a/249937/2508324
            return [cmd[2:index]] + re.findall(r'"(?:[^"\\]|\\.)*"', cmd[index+1:], re.DOTALL)
        else:
            return False
    except:
        if Config.global_debug:
            traceback.print_exc()
        return False

def run_seriously(code, cinput):
    cp437table = ''.join(map(chr,range(128))) + u"ÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜ¢£¥₧ƒáíóúñÑªº¿⌐¬½¼¡«»░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀αßΓπΣσµτΦΘΩδ∞φε∩≡±≥≤⌠⌡÷≈°∙·√ⁿ²■ "
    if any([x not in cp437table for x in code]):
        return "Error: non-CP437 characters detected in code."
    code = ''.join(map(lambda c:"{:02x}".format(c), code.encode('cp437')))
    process = subprocess.Popen(["python2", "{}/Seriously/seriously.py".format(Config.interpreters_dir), '-i', '-x', '-c', code], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        result, err = process.communicate(input=cinput.encode(), timeout=60)
    except subprocess.TimeoutExpired:
        process.kill()
        result = "Sorry, your code took too long to run!"
        partial_out, p_err = process.communicate() # communicate returns a tuple first element is stdout second is stderr
        if partial_out:
            result += "\nPartial output:\n" + partial_out
    except:
        if Config.global_debug:
            traceback.print_exc()
        result = "There was an issue running your code."
    return result.decode('cp437')


def run_marbelous(code, cinput):
    file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    file.write(code)
    file.close()
    process = subprocess.Popen(["{}/marbelous.py-master/marbelous/marbelous.py".format(Config.interpreters_dir), file.name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    try:
        result = process.communicate(input=cinput, timeout=60)[0]
    except subprocess.TimeoutExpired:
        process.kill()
        result = "Sorry, your code took too long to run!"
        partial_out = process.communicate()[0] # communicate returns a tuple first element is stdout second is stderr
        if partial_out:
            result += "\nPartial output:\n" + partial_out
    except:
        if Config.global_debug:
            traceback.print_exc()
        result = "There was an issue running your code."
    os.remove(file.name)
    return result

def run_pyth(code, cinput):
    process = subprocess.Popen(["{}/pyth/pyth.py".format(Config.interpreters_dir), '--safe', '-c', code], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    try:
        result = process.communicate(input=cinput, timeout=60)[0]
    except subprocess.TimeoutExpired:
        process.kill()
        result = "Sorry, your code took too long to run!"
        partial_out = process.communicate()[0] # communicate returns a tuple first element is stdout second is stderr
        if partial_out:
            result += "\nPartial output:\n" + partial_out
    except:
        if Config.global_debug:
            traceback.print_exc()
        result = "There was an issue running your code."
    return result

non_tio_langs = {
    "pyth":run_pyth,
    "marbelous":run_marbelous,
    "seriously":run_seriously,
}

def cmd_eval_debug(cmd, args):
    return cmd_eval(cmd, args, debug=True)

def cmd_eval(cmd, args, debug=False):
    if len(args) < 2:
        return 'Syntax: !eval <language name> "<code>" "[input]" "[args1]" "[args2]"...: Error: not enough arguments: got {}'.format(args)
    lang = args[0].lower()
    if Config.global_debug:
        print(args)
    code = ''
    cinput = ''
    cargs = '+'
    result = ""
    res = list(map(lambda a:ast.literal_eval(a),args[1:]))
    if Config.global_debug:
        print(res)
    if res:
        code = res[0]
        cinput = res[1] if len(res)>1 else ''
        cargs = "+".join(list(map(lambda a : urllib.parse.quote(a), res[2:]))) if len(res)>2 else ''
    if Config.global_debug:
        print(code, cinput, cargs)
    if lang in non_tio_langs:
        result = non_tio_langs[lang](code, cinput)
    else:
        url = "http://{}.tryitonline.net/cgi-bin/backend".format(lang)
        req = "code={}&input={}".format(urllib.parse.quote(code), urllib.parse.quote(cinput))
        if debug:
            req += "&debug=on"
        if len(args) > 2:
          req += "&args={}".format(cargs)
        try:
            result = requests.post(url, data=req).text[33:] # maybe find a way to figure out if there was a timeout on TIO
        except:
            if Config.global_debug:
                traceback.print_exc()
            return "Something went wrong with your request, sorry! Are you sure that language is on Try It Online?"

    result = result or "<no output>" # ugly :P CR would disapprove #golfier #pythonic #lelplebian
    return result

def cmd_langs(cmd, args):
    langs = None
    with urllib.request.urlopen('http://tryitonline.net') as req:
        langs = re.findall(r'<li><a href="//(.+).tryitonline.net/">.*</a></li>', req.read().decode())
    langs.extend([lang for lang in non_tio_langs if lang not in langs])
    return 'Languages supported: {}'.format(', '.join(sorted(langs)).strip())

commands = [  # A list of all Commands in this Module.
    Command('eval', cmd_eval, 'eval:\n\tEvaluates code through http://tryitonline.net backend.\n\tSyntax: Syntax: !eval <language name> "<code>" "[input]" "[args1]" "[args2]"...', special_arg_parsing = parse_eval, aliases=['e']),
    Command('evaldebug', cmd_eval_debug, 'eval:\n\tEvaluates code through http://tryitonline.net backend, with debugging on.\n\tSyntax: Syntax: !evaldebug <language name> "<code>" "[input]" "[args1]" "[args2]"...', special_arg_parsing = parse_eval, aliases=['d']),
    Command('langs', cmd_langs, 'langs:\n\tOutputs the list of supported languages for the eval command.', aliases=['l']),
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
