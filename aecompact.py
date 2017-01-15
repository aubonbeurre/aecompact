#!/usr/bin/env python

import sys
import os
from optparse import OptionParser, OptionGroup
import logging
import subprocess


# 75% of AE sandbox (source: windirstat)
G_compress_exts = (".pdb", ".obj", ".pch", ".lib", ".a", ".tlog")
G_compress_folders = ("obj", "lib", "targets")


def compact(options):
    for root, dirs, files in os.walk(options.path):
        to_compact = []
        for f in files:
            base, ext = os.path.splitext(f)
            if ext.lower() in G_compress_exts:
                to_compact.append(f)

        if to_compact:
            action = ["compact", "/u"] if options.uncompress else ["compact", "/c"]
            subprocess.check_call(action + to_compact, cwd=root)

        to_compact = []
        for d in dirs:
            if d.lower() in G_compress_folders:
                to_compact.append(d)

        if to_compact:
            for d in to_compact:
                action = ["compact", "/u", "/s"] if options.uncompress else ["compact", "/c", "/s"]
                subprocess.check_call(action, cwd=os.path.join(root, d))


def main():
    try:
        parser = OptionParser(usage="%prog [options]", version="%prog 1.0")

        group = OptionGroup(parser,  "Operations", "Compress, uncompress...")
        group.add_option("-u", "--uncompress", help="Uncompress, default is compress (recursively)",
                         dest="uncompress", action="store_true")
        group.add_option("-p", "--path", help="Path to compress, else current path (recursively)",
                         dest="path", metavar="PATH", default=os.getcwd())
        parser.add_option_group(group)

        group = OptionGroup(parser,  "Display Options",
                            "Verbose...")
        group.add_option("-v", "--verbose", help="More verbose",
                         default=False, action="store_true", dest="verbose")
        parser.add_option_group(group)

        (options, args) = parser.parse_args()

        if args:
            parser.error("Too many arguments")
        
        logging.basicConfig(level=logging.INFO if options.verbose else logging.WARNING,
                            format='%(asctime)s.%(msecs)03d %(levelname)-8s: %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            stream=sys.stdout)
        compact(options)

    except Exception:
        logging.error("Error", exc_info=True)

    return 0

if __name__ == "__main__":
    sys.exit(main())
