#!/usr/bin/env python3

from argparse import ArgumentParser
from termcolor import colored


apt_parser = ArgumentParser()
apt_parser.add_argument('op', choices=['list', 'search', 'show', 'install',
                                       'remove', 'autoremove', 'update',
                                       'upgrade', 'full-upgrade',
                                       'edit-sources', 'purge'])
apt_parser.add_argument('packages', nargs='*')

with open('/var/log/apt/history.log') as history_file:
    history = history_file.readlines()

history = filter(lambda line: line.startswith('Commandline: '), history)
history = map(lambda entry: entry.strip().split(' ')[1:], history)

for entry in history:
    if entry[0] not in ['apt', 'apt-get']:
        print(colored('WARNING: malformed entry: {}'.format(entry), 'yellow'))
        continue

    args, _ = apt_parser.parse_known_args(entry[1:])
    if len(args.packages) > 0:
        if args.op in ['install']:
            print(colored('\n'.join(args.packages), 'green'))
        elif args.op in ['remove', 'purge']:
            print(colored('\n'.join(args.packages), 'red'))
