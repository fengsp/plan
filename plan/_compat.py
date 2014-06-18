# -*- coding: utf-8 -*-
"""
    plan._compat
    ~~~~~~~~~~~~

    Some py2/py3 compatibility support.

    :copyright: (c) 2014 by Shipeng Feng.
    :license: BSD, see LICENSE for more details.
"""
import sys

PY2 = sys.version_info[0] == 2


if not PY2:
    text_type = str
    string_types = (str,)
    integer_types = (int,)

    iterkeys = lambda d: iter(d.keys())
    itervalues = lambda d: iter(d.values())
    iteritems = lambda d: iter(d.items())
else:
    text_type = unicode
    string_types = (str, unicode)
    integer_types = (int, long)

    iterkeys = lambda d: d.iterkeys()
    itervalues = lambda d: d.itervalues()
    iteritems = lambda d: d.iteritems()


def get_binary_content(content):
    """Get binary content for binary_writer."""
    if isinstance(content, text_type):
        return content.encode('utf-8')
    return content
