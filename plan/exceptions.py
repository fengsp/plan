# -*- coding: utf-8 -*-
"""
    plan.exceptions
    ~~~~~~~~~~~~~~~

    Plan exceptions.

    :copyright: (c) 2014 by Shipeng Feng.
    :license: BSD, see LICENSE for more details.
"""
from ._compat import text_type, PY2


class BaseError(Exception):
    """Baseclass for all Plan errors."""

    if PY2:
        def __init__(self, message=None):
            if message is not None:
                message = text_type(message).encode('utf-8')
            Exception.__init__(self, message)

        @property
        def message(self):
            if self.args:
                message = self.args[0]
                if message is not None:
                    return message.decode('utf-8', 'replace')

        def __unicode__(self):
            return self.message or u''
    else:
        def __init__(self, message=None):
            Exception.__init__(self, message)

        @property
        def message(self):
            if self.args:
                message = self.args[0]
                if message is not None:
                    return message


class PlanError(BaseError):
    """Plan error.

    .. versionadded:: 0.4
    """


class ParseError(BaseError):
    """Plan job every and at value parse error."""


class ValidationError(BaseError):
    """Plan job every and at value validation error."""
