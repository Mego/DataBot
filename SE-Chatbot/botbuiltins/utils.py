from Module import Command
from datetime import datetime
from requests import HTTPError
import re
import os
from ChatExchange3.chatexchange3.messages import Message


def command_alive(cmd, bot, args, msg, event):
    return "Yes, I'm alive."


def command_utc(cmd, bot, args, msg, event):
    return datetime.utcnow().ctime()


def command_listcommands(cmd, bot, args, msg, event):
    if len(args) == 0:
        return "Commands:%s%s" % (os.linesep, ', '.join([command.name for command in bot.modules.list_commands()]))
    elif len(args) == 1:
        module = bot.modules.find_module_by_name(args[0])
        if module is None:
            return "That module does not exist, or it is disabled."
        cmds = module.list_commands()
        if len(cmds) == 0:
            return "No commands found in `%s`." % args[0]
        return "Commands in `%s`:%s%s" % (args[0], os.linesep, ', '.join([command.name for command in cmds]))
    else:
        return "0 or 1 argument(s) expected."


#def parse_cat_command(cmd):
#    if cmd.startswith("cat "):
#        return [cmd[4:]]
#    else:
#        return False

def command_help(cmd, bot, args, msg, event):
    if len(args) == 0:
        return "I'm $BOT_NAME, $OWNER_NAME's chatbot. You can find the source code [on GitHub]($GITHUB). You can get a list of all commands by running `$PREFIXlistcommands`, or you can run `$PREFIXhelp command` to learn more about a specific command."
    return bot.modules.get_help(args[0]) or "The command you want to look up does not exist."


#def command_cat(cmd, bot, args, msg, event):
#    return args[0]


def command_read(cmd, bot, args, msg, event):
    if len(args) == 0:
      return "No message id/link supplied."
    else:
        message = []
        for msg_id in args:
            if msg_id.isdigit():
                m_id = int(msg_id)
            elif msg_id.split("#")[-1].isdigit():
                m_id = int(msg_id.split("#")[-1])
            elif msg_id.split("/")[-1].isdigit():
                m_id = int(msg_id.split("/")[-1])
            else:
                return msg_id + " is not a valid message id/link."
            try:
                message += [re.sub(r'^:[0-9]+ ', '', Message(m_id, bot.client).content_source)]
            except HTTPError:
                return msg_id + ": message not found."
        return ' '.join(message)


#def command_getcurrentusers(cmd, bot, args, msg, event):
#    try:
#        users = bot.room.get_current_user_names()
#    except HTTPError:
#        return "HTTPError when executing the command; please try again."
#    except ConnectionError:
#        return "ConnectionError when executing the command; please try again."
#    users = [x.encode('ascii', errors='replace').decode('unicode_escape') for x in users]
#    if len(args) > 0 and args[0] == "pingformat":
#        users = [x.replace(" ", "") for x in users]
#        return " ".join(users)
#    return ", ".join(users)


#def command_ping(cmd, bot, args, msg, event):
#    if len(args) == 0:
#        return "No arguments supplied"
#    else:
#        return " ".join(["@" + arg for arg in args])

commands = [Command('alive', command_alive, "A command to see whether the bot is there. Syntax: `$PREFIXalive`", False, False),
            Command('utc', command_utc, "Shows the current UTC time. Syntax: `$PREFIXutc`", False, False),
            Command('listcommands', command_listcommands, "Returns a list of all commands. Syntax: `$PREFIXlistcommands`", False, False),
            Command('help', command_help, "Shows information about the chat bot, or about a specific command. Syntax: `$PREFIXhelp [ command ]`", False, False),
            #Command('cat', command_cat, "Repeats what you said back at you. Syntax: `$PREFIXcat something`", False, False, parse_cat_command, None, None, None),
            Command('read', command_read, "Reads a post to you. Syntax: `$PREFIXread [ message_id ] ...`", False, False),
            #Command('getcurrentusers', command_getcurrentusers, "Shows the current users of a room. Syntax: `$PREFIXgetcurrentusers`", False, False),
            #Command('ping', command_ping, "Pings a list of users for you. Syntax: `$PREFIXping user [...]`", False, False, None, None, None, None)
    ]
module_name = "utils"
