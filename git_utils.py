#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import check_output as shell


def parse_blame(blame):
    sha, file_path, user, date, time, tz_offset, *_ = blame.decode(
        'utf-8').split()

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


def check_if_git_tracked(path):
    result = shell(["git", "rev-parse", "--is-inside-work-tree"],
                   cwd=os.path.dirname(os.path.realpath(path)))
    print("check_if_git_tracked", result)
    return result


def get_blame(line, path):
    try:
        return shell(["git", "blame", "--minimal", "-w",
                      "-L {0},{0}".format(line), path],
                     cwd=os.path.dirname(os.path.realpath(path)),
                     startupinfo=si,
                     stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        pass
        print("Git blame: git error {}:\n{}".format(
            e.returncode, e.output.decode("UTF-8")))
    except Exception as e:
        pass
        print("Git blame: Unexpected error:", e)
