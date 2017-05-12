#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tests import base


# For more on testing your Python plugins, see:
# http://girder.readthedocs.io/en/latest/plugin-development.html#automated-testing-for-plugins
def setUpModule():
    base.enabledPlugins.append('{{ cookiecutter.plugin_name }}')
    base.startServer()


def tearDownModule():
    base.stopServer()


class {{ cookiecutter.plugin_name }}TestCase(base.TestCase):
    def setUp(self):
        super({{ cookiecutter.plugin_name }}TestCase, self).setUp()

    def testThings(self):
        self.assertTrue(True)
