# -*- coding: utf-8 -*-
import configparser
import re
import textwrap

import pytest


class CodeCollector(object):
    def __init__(self, name="code"):

        self.name = name
        self.collected = []

    def __call__(self, f):

        self.collected.append(f)
        return f

    def xfail(self, f):

        self(pytest.param(f, marks=pytest.mark.xfail))
        return f

    def __iter__(self):

        return iter(self.collected)

    def parametrize(self, test_func):

        return pytest.mark.parametrize(self.name, self)(test_func)


def tox_info(var):
    """Get variable value from all sections in the tox.ini file."""
    ini_parser = configparser.ConfigParser()
    ini_parser.read("tox.ini")
    for section in ini_parser:
        if var in ini_parser[section]:
            value = textwrap.dedent(ini_parser[section][var].strip())
            yield section, value


def tox_parse_envlist(string):
    """Parse tox environment list with proper comma escaping."""
    escaped = string
    while re.search(r"({[^,}]*),", escaped):
        escaped = re.subn(r"({[^,}]*),", r"\1:", escaped)[0]
    parts = escaped.split(",")
    return [re.subn(r":", ",", p)[0].strip() for p in parts]
