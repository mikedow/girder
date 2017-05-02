#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  Copyright Kitware Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the 'License' );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an 'AS IS' BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
###############################################################################

import ldap
import mock

from girder.models.model_base import ValidationException
from tests import base


def setUpModule():
    base.enabledPlugins.append('ldap')
    base.startServer()


def tearDownModule():
    base.stopServer()


class MockLdap(object):
    def __init__(self, bindFail=False, searchFail=False):
        self.bindFail = bindFail
        self.searchFail = searchFail

    def bind_s(self, *args, **kwargs):
        if self.bindFail:
            raise ldap.LDAPError('failed to connect')

    def search_s(self, *args, **kwargs):
        if self.searchFail:
            return []

        return [(None, {
            'distinguishedName': ['foobar'],
            'uid': 'foobar',
            'sn': ['Bar'],
            'givenName': ['Foo'],
            'mail': ['foo@bar.com']
        })]
    def unbind_s(self, *args, **kwargs):
        pass


class LdapTestCase(base.TestCase):
    def testLdapLogin(self):
        from girder.plugins.ldap.constants import PluginSettings
        settings = self.model('setting')

        with self.assertRaises(ValidationException):
            settings.set(PluginSettings.LDAP_SERVERS, {})

        settings.set(PluginSettings.LDAP_SERVERS, [{
            'baseDn': 'cn=Users,dc=foo,dc=bar,dc=org',
            'bindName': 'cn=foo,cn=Users,dc=foo,dc=bar,dc=org',
            'password': 'foo',
            'searchField': 'mail',
            'uri': 'ldap://foo.bar.org:389'
        }])

        with mock.patch('ldap.initialize', return_value=MockLdap()) as ldapInit:
            resp = self.request('/user/authentication', basicAuth='hello:world')
            self.assertEqual(len(ldapInit.mock_calls), 1)
            self.assertStatusOk(resp)

            # Register a new user
            user = resp.json['user']
            self.assertEqual(user['email'], 'foo@bar.com')
            self.assertEqual(user['firstName'], 'Foo')
            self.assertEqual(user['lastName'], 'Bar')
            self.assertEqual(user['login'], 'foobar')

            # Login as an existing user
            resp = self.request('/user/authentication', basicAuth='hello:world')
            self.assertStatusOk(resp)
            self.assertEqual(resp.json['user']['_id'], user['_id'])

        with mock.patch('ldap.initialize', return_value=MockLdap(bindFail=True)):
            resp = self.request('/user/authentication', basicAuth='hello:world')
            self.assertStatus(resp, 401)

        with mock.patch('ldap.initialize', return_value=MockLdap(searchFail=True)):
            resp = self.request('/user/authentication', basicAuth='hello:world')
            self.assertStatus(resp, 401)

        # Test fallback to logging in with core auth
        normalUser = self.model('user').createUser(
            login='normal', firstName='Normal', lastName='User', email='normal@user.com',
            password='normaluser')
        with mock.patch('ldap.initialize', return_value=MockLdap(searchFail=True)):
            resp = self.request('/user/authentication', basicAuth='normal:normaluser')
            self.assertStatusOk(resp)
            self.assertEqual(str(normalUser['_id']), resp.json['user']['_id'])
