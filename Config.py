#!/usr/bin/env python3

class ConfigClass:
    def __getattr__(self, name):
        setattr(self, name, None)
        return None

Config = ConfigClass()

Config.interpreters_dir = "."
Config.global_debug = False
