# -*- coding: utf-8 -*-
#
# Author: Pavel Reznikov <pashka.reznikov@gmail.com>
# Created: 6/22/11
#
# Id: $Id$

import unittest2 as unittest
from rohrpost.core import AbstractClient


class FilterTest(unittest.TestCase):
    def test_filter(self):
        client = AbstractClient({'id': '1', 'param2': 'foobar'})
        self.assertTrue(client.test(None))
        self.assertFalse(client.test({'id': '2'}))
        self.assertTrue(client.test({'id': '1'}))
        self.assertTrue(client.test({'param2': 'foobar'}))
        self.assertTrue(client.test({'param2': 'foobar', 'id': '1'}))
        self.assertFalse(client.test({'param2': 'foobar', 'id': '2'}))
        self.assertTrue(client.test(lambda x: True))
        self.assertFalse(client.test(lambda x: False))
        self.assertTrue(client.test(lambda x: x.get('id') == '1'))
        self.assertFalse(client.test(lambda x: x.get('param2') == '1'))
