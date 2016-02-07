#!/usr/bin/env python3

import ModuleManifest
from Module import Module, MetaModule
import readline
from nesting import nesting_deco

modules = MetaModule(ModuleManifest.module_file_names, 'all')

def check_existence_and_chars(cmd_name, content):
    cmd_list = modules.list_commands()
    allowed = -1
    disallowed = -1
    for cmd in cmd_list:
        if cmd.name == cmd_name or (cmd.aliases is not None and cmd_name in cmd.aliases):
            allowed = cmd.allowed_chars
            disallowed = cmd.disallowed_chars
            break
    if allowed == -1:
        return False, False
    for c in content:
        if disallowed is not None and c in disallowed:
            return True, False
        if allowed is not None and c not in allowed:
            return True, False
    return True, True

def requires_special_arg_parsing(cmd_name):
    cmd_list = modules.list_commands()
    for cmd in cmd_list:
        if cmd.name == cmd_name:
            return cmd.special_arg_parsing is not None
    return False

def do_special_arg_parsing(cmd_name, full_cmd):
    cmd_list = modules.list_commands()
    for cmd in cmd_list:
        if cmd.name == cmd_name and cmd.special_arg_parsing is not None:
            return cmd.special_arg_parsing(full_cmd)
    return False

@nesting_deco
def command(cmd):
    cmd_args = cmd.split(' ')
    cmd_name = cmd_args[0].lower()
    args = cmd_args[1:]
    exists, allowed = check_existence_and_chars(cmd_name, ' '.join(args))
    if not exists:
        return "Command not found."
    if not allowed:
        return "Command contains invalid characters."
    if requires_special_arg_parsing(cmd_name):
        args = do_special_arg_parsing(cmd_name, cmd)
        if args is False:
            return "Argument parsing failed."
    return modules.command(cmd_name, args)

def main():
    while True:
        cmd = input()
        print(command(cmd))

if __name__ == '__main__':
    main()
