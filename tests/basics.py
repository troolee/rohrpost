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
from rohrpost.channels.intercom import IntercomClient
from rohrpost.core import IncomeMessage


logger = logging.getLogger('rohrpost-test')

router = None

def handler_a1(router, channel, msg):
    logger.debug('handler_a1')
    channel.say(('hello', {'foo': 'bar'}))


def handler_a2(router, channel, msg):
    logger.debug('handler_a2')


def handler_b1(router, channel, msg):
    logger.debug('handler_b1')
    msg.reply(('ololo', {1:1}))
    raise StopIteration()


def handler_b2(router, channel, msg):
    logger.debug('handler_b2')


def intercom_handler(client, msg):
    logger.debug('intercom_handler %s %s', msg.name, msg.data)
    if msg.name == 'hello':
        msg = IncomeMessage('foo', {1:1}, client)
        router.process_message('channel_b', msg)

    
router = make_router({
    'channel_a': {
        'message_a1': handler_a1,
        'message_a2': handler_a2,
    },
    'channel_b': {
        '*': [handler_b1, handler_b2],
    },
})
router.get_channel('channel_a').connect(IntercomClient({'id': 'intercom-client'}, intercom_handler))


class BasicTests(unittest.TestCase):

    def test_make_router(self):
        router.process_message('channel_a', ('foo', {'bar': True}))
        router.process_message('channel_a', IncomeMessage('message_a1', {'param1': 1}))
        for x in xrange(2):
            router.process_message('channel_b', ('foo', {'bar': True}))
            router.process_message('channel_b', ('foo', {'bar': False}))

        time.sleep(1)
