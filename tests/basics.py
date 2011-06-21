# -*- coding: utf-8 -*-
#
# Author: Pavel Reznikov <pashka.reznikov@gmail.com>
# Created: 6/21/11
#
# Id: $Id$

import unittest2 as unittest
import logging
import time

from rohrpost import make_router
from rohrpost.core import IncomeMessage


logger = logging.getLogger('rohrpost-test')


def handler_a1(router, channel, msg):
    logger.debug('handler_a1')
    pass


def handler_a2(router, channel, msg):
    logger.debug('handler_a2')
    pass


def handler_b1(router, channel, msg):
    logger.debug('handler_b1')
    raise StopIteration()


def handler_b2(router, channel, msg):
    logger.debug('handler_b2')
    pass


class BasicTests(unittest.TestCase):
    def setUp(self):
        self.router = make_router({
            'channel_a': {
                'message_a1': handler_a1,
                'message_a2': handler_a2,
            },
            'channel_b': {
                '*': [handler_b1, handler_b2],
            },
        })

    def test_make_router(self):
        self.router.process_message('channel_a', ('foo', {'bar': True}))
        self.router.process_message('channel_a', IncomeMessage('message_a1', {'param1': 1}))
        for x in xrange(2):
            self.router.process_message('channel_b', ('foo', {'bar': True}))
            self.router.process_message('channel_b', ('foo', {'bar': False}))

        time.sleep(1)
        