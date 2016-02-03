from Module import Command

module_name = "modulecontrols"

def module(cmd, bot, args, msg, event):
    if len(args) < 1:
        return "Not enough arguments. Syntax: `module <action> <options...>`"
    if args[0] == "help":
        return "Contains controls for modules.\n`module enable <name>` - enables a module\n`module disable <name>` - " \
            "disables a module\n"
    elif args[0] == "enable":
        return module_enable(cmd, bot, args, msg, event)
    elif args[0] == "disable":
        return module_disable(cmd, bot, args, msg, event)


def module_disable(cmd, bot, args, msg, event):
    if len(args) < 2:
        return "Not enough arguments."
    mod = args[1]
    success = bot.modules.disable_module(mod)
    if success:
        return "Module disabled."
    else:
        return "No such module, or it (or its container) has already been disabled."


def module_enable(cmd, bot, args, msg, event):
    if len(args) < 2:
        return "Not enough arguments."
    mod = args[1]
    success = bot.modules.enable_module(mod)
    if success:
        return "Module enabled."
    else:
        return "No such module, or its container is still disabled."


commands = [
    Command("module", module, "Contains controls for modules. Run `module help` for details.", False, True)
]
