#!/usr/bin/python2.7
#
# Copyright (c) 2017 Martin Wind
#
from __future__ import with_statement, print_function
import sys

try:
    from calibre.ebooks.metadata.meta import get_metadata
except ImportError:
    print('No module named calibre')
    print('try to run the script with calibre-debug (calibre bundled python)')
    sys.exit(1)

import os
import json
import base64
import re
import hashlib
import argparse
from json import JSONEncoder
from datetime import datetime, date

BLOCKSIZE = 65536 #hashing
IGNORE = [
    'author_link_map',
    'user_categories',
    'manifest',
    'guide',
    'spine'
]

class SaveEncoder(JSONEncoder):
    def default(self, o):
        if (isinstance(o, date)):
            return o.isoformat()
        return o.__dict__


def crawl_file(path, inline_cover = False, export_cover_dir = None):
    stream_type = os.path.splitext(path)[1].replace('.', '').lower()
    file_name = os.path.basename(path)
    meta = {
        'file': file_name,
        'path': path,
        'crawl_date': datetime.utcnow(),
    }
    with open(path, 'rb') as stream:
        hasher = hashlib.sha256()
        buf = stream.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = stream.read(BLOCKSIZE)
        file_hash = hasher.hexdigest()
        stream.seek(0)

        mi = get_metadata(stream, stream_type, force_read_metadata=True)
        # print(dir(mi))
        meta = {
            'file': file_name,
            'hash': file_hash,
            'path': path,
            'crawl_date': datetime.utcnow().isoformat(),
        }
        try:
            meta['tag'] = re.search('.*\[([^\]]+)\].*', file_name).group(1)
        except:
            pass
        for key in mi.all_field_keys():
            if key == 'cover_data':
                try:
                    (format, data) = mi.get(key)
                    meta['cover_data_format'] = format
                    if inline_cover:
                        meta['cover_data'] = base64.standard_b64encode(data)
                    if export_cover_dir:
                        cover_folder = os.path.join(export_cover_dir, file_hash[0:2], file_hash[2:4])
                        if not os.path.isdir(cover_folder):
                            os.makedirs(cover_folder)
                        cover_file = os.path.join(cover_folder, '%s.%s' % (file_hash, format))
                        meta['cover_file'] = cover_file
                        with open(cover_file, 'w') as cfile:
                            cfile.write(data)
                except:
                    meta.pop('cover_data', None)
                    meta.pop('cover_data_format', None)
                    meta.pop('cover_file', None)
            elif key in IGNORE:
                pass
            else:
                val = mi.get(key)
                if val:
                    meta[key] = val
    return meta

def json_crawl_file(*args, **kwargs):
    return json.dumps(crawl_file(*args, **kwargs), cls=SaveEncoder)

def main(args=sys.argv):
    parser = argparse.ArgumentParser(
        description='Print eBook metadata in JSON format',
        usage='''

  python2.7 %(prog)s [-h] [--inline-covers] [--covers-dir dir] file
  calibre-debug %(prog)s -- [-h] [--inline-covers] [--covers-dir dir] file'''
    )
    parser.add_argument('dir', metavar='file',
                        help='directory or file to read')
    parser.add_argument('--inline-covers', action='store_true', default=False,
                        help='include cover images as base64 data')
    parser.add_argument('--covers-dir', metavar='dir',
                        help='directory to store the cover images')
    args = parser.parse_args()
    if os.path.isdir(args.dir):
        dirname = args.dir
        file_names = os.listdir(dirname)
        file_count = len(file_names)
        print('[')
        if file_count:
            for file_name in file_names[:-1]:
                print('%s,' % json_crawl_file(
                    os.path.join(dirname, file_name),
                    export_cover_dir=args.covers_dir,
                    inline_cover=args.inline_covers
                ))
            print('%s' % json_crawl_file(
                os.path.join(dirname, file_names[-1]),
                export_cover_dir=args.covers_dir,
                inline_cover=args.inline_covers
            ))
        print(']')
    elif os.path.isfile(args.dir):
        print('%s' % json_crawl_file(
            args.dir,
            export_cover_dir=args.covers_dir,
            inline_cover=args.inline_covers
        ))
    else:
        print('argument is not a file or a directory')
        return 2
    return 0

if __name__ == '__main__':
    sys.exit(main())
