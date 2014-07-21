# -*- coding: utf-8 -*-
"""
    plan.testsuite
    ~~~~~~~~~~~~~~

    Tests Plan itself.

    :copyright: (c) 2014 by Shipeng Feng.
    :license: BSD, see LICENSE for more details.
"""
import sys
import pkgutil
import unittest

from plan._compat import PY2, string_types


class BaseTestCase(unittest.TestCase):
    """Baseclass for all the tests that Plan uses.  We use this
    BaseTestCase for code style consistency.
    """

    def setup(self):
        pass

    def teardown(self):
        pass

    def setUp(self):
        self.setup()

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.teardown()

    def assert_equal(self, first, second):
        return self.assertEqual(first, second)

    def assert_true(self, expr, msg=None):
        self.assertTrue(expr, msg)

    def assert_false(self, expr, msg=None):
        self.assertFalse(expr, msg)

    def assert_raises(self, exception, callable=None, *args, **kwargs):
        self.assertRaises(exception, callable, *args, **kwargs)

    def assert_in(self, first, second):
        self.assertIn(first, second)

    def assert_not_in(self, first, second):
        self.assertNotIn(first, second)

    def assert_isinstance(self, obj, cls):
        self.assertIsInstance(obj, cls)

    if sys.version_info[:2] == (2, 6):
        def assertIn(self, x, y):
            assert x in y, "%r not found in %r" % (x, y)

        def assertNotIn(self, x, y):
            assert x not in y, "%r unexpectedly in %r" % (x, y)

        def assertIsInstance(self, x, y):
            assert isinstance(x, y), "not isinstance(%r, %r)" % (x, y)


def import_string(import_name):
    """Import a module based on a string.

    :param import_name: the dotted name for the object to import.
    :return: imported object
    """
    assert isinstance(import_name, string_types)
    if '.' in import_name:
        module, obj = import_name.rsplit('.', 1)
    else:
        return __import__(import_name)
    if PY2 and isinstance(obj, unicode):
        obj = obj.encode('utf-8')
    return getattr(__import__(module, None, None, [obj]), obj)


def find_modules(import_name):
    """Find all modules under one package.
    """
    module = import_string(import_name)
    path = getattr(module, '__path__', None)
    if path is None:
        raise ValueError('%s is not a package' % import_name)
    basename = module.__name__ + '.'
    for importer, modname, ispkg in pkgutil.iter_modules(path):
        modname = basename + modname
        if not ispkg:
            yield modname


def iter_suites():
    """Generator for all testsuites."""
    for module in find_modules(__name__):
        mod = import_string(module)
        if hasattr(mod, 'suite'):
            yield mod.suite()


def suite():
    """A testsuite that has all the Plan tests.
    """
    suite = unittest.TestSuite()
    for module_suite in iter_suites():
        suite.addTest(module_suite)
    return suite


def main():
    """Runs the testsuite."""
    unittest.main(__name__, defaultTest='suite')
