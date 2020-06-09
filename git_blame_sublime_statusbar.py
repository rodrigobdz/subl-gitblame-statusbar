#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import os
import subprocess
from datetime import datetime
import git_utils

try:
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
except:
    si = None


class GitBlameStatusbarCommand(sublime_plugin.EventListener):
    """ Show Git blame author for the currently selected line. """

    def days_between(self, d):
        now = datetime.now()
        d = datetime.strptime(d, "%Y-%m-%d")
        return abs((now - d).days)

    def on_activated(self, view):
        git_utils.check_if_git_tracked(view.file_name())

    def on_selection_modified_async(self, view):
        current_line = view.substr(view.line(view.sel()[0]))
        (row, col) = view.rowcol(view.sel()[0].begin())
        path = view.file_name()
        blame = git_utils.get_blame(int(row) + 1, path)
        output = ''
        if blame:
            sha, user, date, time = git.parse_blame(blame)
            time = ''
            output = '☞ ' + user + ' ' + time

        view.set_status('git_blame', output)
