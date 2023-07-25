#!/usr/bin/env python

from os import environ, popen
import random

# check config
import sys
from os.path import expanduser

sys.path.append(expanduser('~/.config/fetch'))

from config import fetch_list, pre, sep

#get various infos

def user():
    return environ['USER']

def host():
    with open('/etc/hostname', 'r') as r:
        return r.read().strip()

def kernel():
    with open('/proc/version', 'r') as r:
        content = r.read()
        content = content.split()
        return content[2]

def os():
    with open('/etc/os-release', 'r') as r:
        content = r.read()
        content = content.split('PRETTY_NAME="')
        content = content[1].split('"')
        os_name = content[0]
        return os_name

def shell():
    sh = environ['SHELL']
    sh = sh.split('/bin/')
    return sh[-1]

def uptime():
    with open('/proc/uptime', 'r') as r:
        up = round(float(r.read().split()[0]))
        # seconds
        if up < 60:
            return f'{up}s'
        # minutes
        elif up < (60 * 60):
            secs = up % 60
            mins = up // 60
            return f'{mins}m {secs}s'
        # hours
        elif up < (60 * 60 * 24):
            mins = (up % (60 * 60)) // 60
            hours = up // (60 * 60)
            return f'{hours}h {mins}m'
        # days
        else:
            hours = (up % (60 * 60 * 24)) // (60 * 60)
            days = up // (60 * 60 * 24)
            return f'{days}d {hours}h'

def memory():
    with open('/proc/meminfo', 'r') as r:
        content = r.read()

        mem_total = content.split('MemTotal:')
        mem_total = mem_total[1]
        mem_total = mem_total.split()
        mem_total = mem_total[0]
        mem_total = round(int(mem_total) / 1024)

        mem_used = content.split('Active:')
        mem_used = mem_used[1]
        mem_used = mem_used.split()
        mem_used = mem_used[0]
        mem_used = round(int(mem_used) / 1024)

        return f'{mem_used}M / {mem_total}M'

def cpu():
    with open('/proc/cpuinfo', 'r') as r:
        content = r.read()

        model_name = content.split('model name	: ')
        model_name = model_name[1]
        model_name = model_name.split('\n')
        model_name = model_name[0]

        return model_name

# make it look nice

fetch_dict = {
    'user': user(),
    'host': host(),
    'kernel': kernel(),
    'os': os(),
    'shell': shell(),
    'uptime': uptime(),
    'memory': memory(),
    'cpu': cpu(),
}

def rand_color():
    rand_color = random.randrange(31,36)
    return f'\033[{rand_color};1;3m'

bold = '\033[1m'
italic = '\033[3m'
reset = '\033[0m'

def main():
    for key in fetch_list:
        value = fetch_dict[key]
        meat = f'{rand_color()}{pre}{reset}{bold}{key}{reset}{sep}{italic}{value}{reset}'
        print(meat)

main()
