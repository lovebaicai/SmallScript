#! /usr/bin/env python

import telnetlib
import re

MacHost1 = "host1"
MacHost2 = "host2"
PASSWORD = b"password"


def filter_in(lines, include):
    regex = re.compile(include)
    return [line for line in lines if regex.search(line)]

def filter_out(lines, exclude):
    regex = re.compile(exclude)
    return [line for line in lines if not regex.search(line)]

def print_lines(lines):
    for line in lines:
        print(line)
    print()

# router
def bw_router(host):
    data = b''
    tn = telnetlib.Telnet(host)
    data += tn.read_until(b'Password:')
    tn.write(PASSWORD + b'\n')
    
    data += tn.read_very_eager()
    tn.write(b'display interface GigabitEthernet | include Last.*rate\n')
    tn.write(b'quit\n')
    data += tn.read_all()

    return data.decode('ascii')

# switch
def bw_switch(host):
    data = b''
    tn = telnetlib.Telnet(host)
    data += tn.read_until(b'Password:')
    tn.write(PASSWORD + b'\n')
    
    data += tn.read_very_eager()
    tn.write(b'display interface GigabitEthernet | include (Gigabit.* UP|Last .* output)\n')
    data += tn.read_until(b'>')
    ind, _, d = tn.expect([b'More', b'<\w*>'])
    while ind == 0:
        data += d
        tn.write(b' \n')
        ind, _, d = tn.expect([b'More', b'<\w*>'])
    data += d
    tn.write(b'quit\n')
    data += tn.read_all()

    return data.decode('ascii')


if __name__ == '__main__':
    lines = filter_in(bw_router(MacHost1).splitlines(), 'Last.*rate')
    print_lines(lines)
    lines = filter_out(filter_in(bw_switch(MacHost2).splitlines(), 'Gigabit.* UP|Last .* output'), '-%')
    print_lines(lines)
    for i in range(1,7):
        lines = filter_out(filter_in(bw_switch('host.{}'.format(i)).splitlines(), 'Gigabit.* UP|Last .* output'), '-%')
        print_lines(lines)
