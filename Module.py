import importlib
import types
import os
import traceback
import string


class Command:  # An executable command.
    def __init__(self, name, execute, help_data='', aliases=None, allowed_chars=None, disallowed_chars="", special_arg_parsing=None):
        self.name = name
        self._execute = execute
        self.help_data = help_data or "Command exists, but no help entry found."
        self.aliases = aliases
        self.special_arg_parsing = special_arg_parsing
        if allowed_chars is not None and " " not in allowed_chars:
            allowed_chars += " "
        # Space should always be allowed for multiple arguments.
        # If you really want to disallow spaces, add one to disallowed_chars.
        self.allowed_chars = allowed_chars
        self.disallowed_chars = disallowed_chars
    def execute(self, args):
        return self._execute(self.name, args)


class Module:  # Contains a list of Commands.
    def __init__(self, commands, module_name):
        self.commands = commands
        self.module_name = module_name
        self.enabled = True

    def command(self, name, args):
        if not self.enabled:
            return False
        command = self.find_commands(name)
        if command:
            return command.execute(args)
        else:
            return False

    def get_help(self, name):
        match = self.find_commands(name)
        if match:
            return match.help_data
        else:
            return ''

    def find_commands(self, name):
        for command in self.commands:
            if command.name == name: return command
            elif command.aliases is not None and name in command.aliases: return command
        return None

    def list_commands(self):
        if not self.enabled:
            return []
        cmd_list = []
        for command in self.commands:
            cmd_list.append(command)
        return cmd_list


class MetaModule:  # Contains a list of Modules.
    def __init__(self, modules, module_name, path=''):
        self.modules = []
        self.module_name = module_name
        self.enabled = True
        if path and not path[-1] == '.':
            self.path = path + '.'
        else:
            self.path = ''
        for module in modules:
            self.modules.append(self.load_module(module))

    def command(self, name, args):
        if not self.enabled:
            return False
        response = False
        for module in self.modules:
            response = module.command(name, args)
            if response is not False:
                break
        return response

    def get_help(self, name):
        if not self.enabled:
            return False
        response = False
        for module in self.modules:
            if not module.enabled:
                continue
            response = module.get_help(name)
            if response:
                break
        return response

    def load_module(self, file_):
        file_ = self.path + file_
        try:
            module_file = importlib.import_module(file_)
        except ImportError as e:
            msg = "Error at importing " + file_ + os.linesep
            msg += "ImportError: " + e.msg
            msg += os.linesep
            msg += traceback.format_exc()
            raise ModuleLoadError(msg)
        try:
            mdls = module_file.modules
            try:
                module_name = module_file.module_name
            except AttributeError:
                module_name = file_
            if not isinstance(module_name, str):
                raise MalformedModuleException("Module: '%s', 'module_name' is not a string." % file_)
            if type(mdls) is list:
                return MetaModule(mdls, module_name, file_[:file_.rfind('.')])
            else:
                raise MalformedModuleException("Module: '" + file_ + "', 'modules' is not a list.")
        except AttributeError:
            try:
                cmds = module_file.commands
                try:
                    module_name = module_file.module_name
                except AttributeError:
                    module_name = file_
                if not isinstance(module_name, str):
                    raise MalformedModuleException("Module: '%s', 'module_name' is not a string." % file_)
                try:
                    save_subdir = module_file.save_subdir
                    if isinstance(save_subdir, str):
                        self.bot.save_subdirs.append(save_subdir)
                    else:
                        raise MalformedModuleException("Module: '%s', 'save_subdir' is not a string." % file_)
                except AttributeError:
                    pass
                if type(cmds) is list:
                    return Module(cmds, module_name)
                else:
                    raise MalformedModuleException("Module: '" + file_ + "', 'commands' is not a list.")
            except AttributeError:
                raise MalformedModuleException("Module: '" + file_ + "' does not contain a variable called either 'modules' or 'commands'.")

    def list_commands(self):
        if not self.enabled:
            return []
        cmd_list = []
        for module in self.modules:
            cmd_list.extend(module.list_commands())
        return cmd_list

    def find_module_by_name(self, name):
        if not self.enabled:
            return None
        if self.module_name == name:
            return self
        for m in self.modules:
            if m.module_name == name:
                return m
            if isinstance(m, MetaModule):
                m1 = m.find_module_by_name(name)
                if m1 is not None:
                    return m1
        return None

    def disable_module(self, name):
        if not self.enabled:
            return False
        if self.module_name == name:
            self.enabled = False
            return True
        for m in self.modules:
            if m.module_name == name:
                m.enabled = False
                return True
            if isinstance(m, MetaModule):
                m1 = m.disable_module(name)
                if m1:
                    return True
        return False

    def enable_module(self, name):
        if self.module_name == name:
            self.enabled = True
            return True
        if not self.enabled:
            return False
        for m in self.modules:
            if m.module_name == name:
                m.enabled = True
                return True
            if isinstance(m, MetaModule):
                m1 = m.enable_module(name)
                if m1:
                    return True
        return False


class ModuleLoadError(Exception):
    pass


class MalformedModuleException(Exception):
    pass
