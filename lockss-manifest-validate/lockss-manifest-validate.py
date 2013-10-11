#!/usr/bin/python
"""

This is a tool to verify checksum hashes produced by LOCKSS against hashes
provided by a BagIt manifest document.

Invoke with -h for usage help.

Written by Stephen Eisenhauer
At University of North Texas Libraries
On 2013-04-17

Notes:

  * The LOCKSS hash list will have more entries than we actually care about
    (checksums for Apache directory listing pages, etc.), so we should just
    go down the list of bag manifest entries and ensure that everything
    there is also present (and identical) in the LOCKSS list.

"""
import argparse
import os
import re
import urllib

def load_lockss_hashes(hashcus_path):
    prefix = None
    hashes = dict()
    f = open(hashcus_path, 'r')
    for line in f:
        m = re.match('[0-9A-F]{32}   (.+)', line)
        if m:
            if not prefix:
                prefix = len(m.group(1)) + 1
                continue
            
            hashes[m.group(1)[prefix:]] = line[:32]
    f.close()
    print "Found %d hashes in HashCUS file" % len(hashes)
    return hashes


def compare_manifest_hashes(manifest_path, hashes):
    records = 0
    errors = 0
    f = open(manifest_path, 'r')
    for line in f:
        m = re.match('[0-9a-f]{32}  (.+)', line)
        if m:
            records += 1
            path = urllib.quote(m.group(1), safe="%/:=&?~#+!$,;'@()*[]")
            if not path in hashes:
                print "No LOCKSS hash found for path: %s" % path
                errors += 1
            elif line[:32].upper() != hashes[path]:
                print "Hash mismatch: %s != %s for path %s" % (line[:32], hashes[path], path)
                errors += 1
    f.close()
    print "Compared %d records, encountered %d errors." % (records, errors)


def _make_arg_parser():
    parser = argparse.ArgumentParser(
        description='Compare a LOCKSS hash list to a bag manifest.')
    parser.add_argument('HashCUS',
        help="path to the HashCUS.txt file downloaded from LOCKSS")
    parser.add_argument('manifest',
        help="path to the bag manifest (e.g. mybag/manifest-md5.txt")

    return parser


if __name__ == "__main__":
    parser = _make_arg_parser()
    args = parser.parse_args()
    
    hascus_path = os.path.abspath(args.HashCUS)
    manifest_path = os.path.abspath(args.manifest)

    hashes = load_lockss_hashes(hascus_path)
    compare_manifest_hashes(manifest_path, hashes)
