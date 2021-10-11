#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# by Lucas Cavalcante, 2021

"""
This script moves all files from all members of a group to an `archive`
folder.
The name of the group is be a parameter of the program.

Optionally, change the targe directory setting the `TARGETDIR` environment variable.
"""

from argparse import ArgumentParser
from grp import getgrall
from subprocess import call, Popen, PIPE
import logging
import os

_log = logging.getLogger(__name__)
logging.basicConfig(filename='out.log', level=logging.DEBUG)

TARGETDIR = os.getenv('TARGETDIR', 'archive')


def get_group_members(groupname: str) -> list:
    """
    Get all user members of a group.
    """
    group_members = [
        group.gr_mem for group in getgrall() if group.gr_name == groupname
    ]
    _log.info(f" [*] Obtained user members of group '{groupname}'")
    return next(iter(group_members), [])


def move_files(files: list) -> None:
    """
    Move all files from a list of files to the `TARGETDIR` directory.
    """
    if not os.path.exists(TARGETDIR):
        os.mkdir(TARGETDIR)
        _log.info(f" [*] Directory '{TARGETDIR}' created")
    for file in files:
        try:
            call(f'mv {file} {TARGETDIR}', shell=True, stdout=PIPE)
            _log.info(f" [*] Moved '{file}' to directory '{TARGETDIR}'")
        except Exception as exc:
            _log.error(
                ' [!] Could not move file {file}. Task raised exception: %r'
                % (file, exc)
            )
            raise exc


def get_all_files_owned_by_user(username: str) -> list:
    """
    Get all files owned by an user in the filesystem.
    """
    try:
        with Popen(f'find / -user {username} 2>&-', shell=True, stdout=PIPE) as proc:
            output = proc.stdout.read()
            files = output.decode('utf-8').splitlines()
        _log.info(f" [*] Obtained list of files owned by user '{username}'")
        return files
    except Exception as exc:
        _log.error(
            ' [!] Could not get files owned by %r. Task raised exception: %r'
            % (username, exc)
        )
        raise exc


def move_files_of_an_owner(username: str) -> None:
    """
    Move all files in the filesystem owned by an user to the
    `TARGETDIR` directory.
    """
    files = get_all_files_owned_by_user(username)
    try:
        move_files(files)
        _log.info(
            f" [*] Successfully moved all files owned by user '{username}'"
        )
    except Exception as exc:
        _log.error(
            ' [!] Could not move files owned by %r. Task raised exception: %r'
            % (username, exc)
        )
        raise exc


def move_files_of_a_group(groupname: str) -> None:
    """
    Move all files in the filesystem owned by user of a given group to
    the `TARGETDIR` directory.
    """
    group_members = get_group_members(groupname)
    for user in group_members:
        move_files_of_an_owner(user)
    _log.info(
        f" [*] Successfully moved all files owned by users of group '{groupname}'"
    )


if __name__ == '__main__':
    """
    Main script function.
    """
    parser = ArgumentParser(description='Enter target group.')
    parser.add_argument('--groupname', type=str, default='')
    args = parser.parse_args()

    groupname_value = args.groupname
    move_files_of_a_group(groupname_value)
