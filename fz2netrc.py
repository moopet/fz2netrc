#!/usr/bin/env python
from xml.parsers.expat import ExpatError
from xml.dom import minidom
import sys

def main():
    DEFAULT_ENTRY = { 
        'username': None,
        'password': None,
        'local_dir': None,
        'remote_dir': None,
    }

    try:
        xmldoc = minidom.parse(sys.stdin)
    except ExpatError:
        print >> sys.stderr, 'Error parsing input file'
        sys.exit(1)

    entries = {}
    for server in xmldoc.getElementsByTagName('Server'):
        entry = DEFAULT_ENTRY.copy()

        tmp = server.getElementsByTagName('Host')
        if not tmp:
            continue
        hostname = tmp[0].firstChild.nodeValue

        tmp = server.getElementsByTagName('User')
        if tmp and tmp[0].firstChild:
            entry['username'] = tmp[0].firstChild.nodeValue

        tmp = server.getElementsByTagName('Pass')
        if tmp and tmp[0].firstChild:
            entry['password'] = tmp[0].firstChild.nodeValue

        tmp = server.getElementsByTagName('LocalDir')
        if tmp and tmp[0].firstChild:
            entry['local_dir'] = tmp[0].firstChild.nodeValue

        tmp = server.getElementsByTagName('RemoteDir')
        if tmp and tmp[0].firstChild:
            entry['remote_dir'] = tmp[0].firstChild.nodeValue.split()[-1]

        entries[hostname] = entry

    if entries:
        for hostname in entries.keys():
            entry = entries[hostname]
            print 'machine', hostname
            if entry['username']:
                print 'login', entry['username']
                if entry['password']:
                    print 'password', entry['password']
            if entry['local_dir'] or entry['remote_dir']:
                print 'macdef init'
                if entry['local_dir']:
                    print 'lcd', entry['local_dir']
                if entry['remote_dir']:
                    print 'cd', entry['remote_dir']
                print
            print

if __name__ == '__main__':
    main()
