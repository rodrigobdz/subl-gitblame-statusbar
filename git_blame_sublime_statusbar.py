import sublime
import sublime_plugin
import os
import subprocess
from subprocess import check_output as shell
from datetime import datetime

try:
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
except:
    si = None

class GitBlameStatusbarCommand(sublime_plugin.EventListener):
  def parse_blame(self, blame):
    sha, file_path, user, date, time, tz_offset, *_ = blame.decode('utf-8').split()

    # Was part of the inital commit so no updates
    if file_path[0] == '(':
        user, date, time, tz_offset = file_path, user, date, time
        file_path = None

    # Fix an issue where the username has a space
    # Im going to need to do something better though if people
    # start to have multiple spaces in their names.
    if not date[0].isdigit():
        user = "{0} {1}".format(user, date)
        date, time = time, tz_offset

    return(sha, user[1:], date, time)

  def get_blame(self, line, path):
    try:
        return shell(["git", "blame", "--minimal", "-w",
            "-L {0},{0}".format(line), path],
            cwd=os.path.dirname(os.path.realpath(path)),
            startupinfo=si,
            stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        pass
        # print("Git blame: git error {}:\n{}".format(e.returncode, e.output.decode("UTF-8")))
    except Exception as e:
        pass
        # print("Git blame: Unexpected error:", e)

  def days_between(self, d):
    # now = datetime.strptime(datetime.now(), "%Y-%m-%d")
    now = datetime.now()
    d = datetime.strptime(d, "%Y-%m-%d")
    return abs((now - d).days)

  def on_selection_modified_async(self, view):
    current_line = view.substr(view.line(view.sel()[0]))
    (row,col) = view.rowcol(view.sel()[0].begin())
    path = view.file_name()
    blame = self.get_blame(int(row) + 1, path)
    output = ''
    if blame:
        sha, user, date, time = self.parse_blame(blame)
        # try:
        #     time = '( ' + str(self.days_between(time)) + ' days ago )'
        # except Exception as e:
        #     time = ''
        #     print("Git blame: days_between ", e)
        time = ''
        output = '☞ ' + user + ' ' + time

    view.set_status('git_blame', output)