#!/usr/bin/env python

import argparse
import plistlib
import sys

PLIST_START_MARKER = '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">'
PLIST_END_MARKER = '</plist>'

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Extracts the list of device udids associated with a .mobileprovision file.")
    parser.add_argument("provisioning_profile",
                        help="path to a .mobileprovision file"
                       )
    args = parser.parse_args()

    with open(args.provisioning_profile, "rb") as provisioning_file:
        file_contents = provisioning_file.read()

    plist_start = file_contents.find(PLIST_START_MARKER)
    plist_end = file_contents.find(PLIST_END_MARKER)
    if plist_start < 0 or plist_end < 0:
        print("Could not parse {f}. Please check for an updated version of this script.".format(f=args.provisioning_profile))
        return 1

    plist_end += len(PLIST_END_MARKER)

    plist_dict = plistlib.readPlistFromString(file_contents[plist_start:plist_end])
    try:
        devices = plist_dict['ProvisionedDevices']
    except KeyError:
        print("Could not find list of devices in {f}. Please check for an updated version of this script.".format(f=args.provisioning_profile))
        return 1

    for device in devices:
        print device

if __name__ == '__main__':
    sys.exit(main())
