#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2015 deanishe@deanishe.net
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2015-04-30
#

"""
url_for_image.py <imagefile>

Upload file to Google Image Search and return URL for results page.

Google Image Search supports PNG, GIF, JPG and BMP files.

The URL of the results page is printed to STDOUT.

"""
from __future__ import print_function, unicode_literals, absolute_import

import os
import subprocess
import sys


SEARCH_URL = 'https://www.google.com/searchbyimage/upload'
USER_AGENT = 'alfred-similiar-image-search 0.1 ()'
CURL = '/usr/bin/curl'


def log(s, *args):
    """Simple STDERR logger."""
    if args:
        s = s % args
    print(s, file=sys.stderr)


def similar_images_url(image_path):
    """Return URL for results page for similar images.

    The request is built based on the information in this SO thread:
        https://stackoverflow.com/questions/7584808/

    """
    redir_url = None

    log('uploading %r to Google ...', image_path)

    cmd = [
        CURL,
        '--include',  # Show HTTP headers
        '--silent',   # Don't show progress
        '--user-agent', USER_AGENT,
        '--form', 'image_url=',
        '--form', 'filename=',
        '--form', 'h1=en',
        '--form', 'bih=179',
        '--form', 'biw=1600',
        '--form', 'encoded_image=@{0}'.format(image_path),
        SEARCH_URL,
    ]

    # Encode and run command
    cmd = [s.encode('utf-8') for s in cmd]
    log('cmd=%r', cmd)
    output = subprocess.check_output(cmd)

    # Extract the `Location:` header
    for line in output.split('\n'):
        log('[response] %s', line)
        if line.lower().startswith('location: '):
            redir_url = line[10:]
            break

    return redir_url


def main(args=None):
    """Print URL of Google Similar Images search for image file"""
    # Collect and validate script arguments
    args = args or sys.argv[1:]
    assert len(args) == 1, 'Usage: url_for_image.py <imagefile>'
    filepath = args[0].decode('utf-8')
    assert os.path.exists(filepath), 'File does not exist: {}'.format(filepath)

    url = similar_images_url(filepath)
    if url is None:
        raise ValueError("Couldn't understand server response")
    print(url, end='')


if __name__ == '__main__':
    sys.exit(main())
