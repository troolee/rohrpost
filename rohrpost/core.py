# -*- coding: utf-8 -*-
#
# Author: Pavel Reznikov <pashka.reznikov@gmail.com>
# Created: 6/21/11
#
# Id: $Id$

import logging
import json
from rohrpost.utils import async


logger = logging.getLogger('rohrpost')


class Router(object):
    def __init__(self):
        self._channels = {}

    def process_message(self, channel, msg):
        if isinstance(msg, (tuple, list)):
            msg = IncomeMessage(*msg)
        assert(isinstance(msg, IncomeMessage))
        self._channels[channel].process_message(msg)

    def broadcast(self, msg, filter=None):
        for c in self._channels.values():
            c.say(msg, filter)

    def get_channel(self, channel):
        return self._channels[channel]

    def register_channel(self, name, channel):
        logger.debug('register channel %s', name)
        if name in self._channels:
            raise ValueError('Channel "%s" already exists.' % name)
        self._channels[name] = channel

    def unregister_channel(self, name):
        logger.debug('unregister channel %s', name)
        del self._channels[name]


class Channel(object):
    def __init__(self, name, router):
        self._name = name
        self._router = router
        self._handlers = {}
        self._clients = []

    @property
    def name(self):
        return self._name

    def connect(self, client):
        self._clients.append(client)

    def disconnect(self, client):
        self._clients.remove(client)

    def say(self, msg, filter=None):
        @async
        def do_say():
            logger.debug('say %s to %s in %s', msg, filter if filter else 'ALL', self.name)
            for c in self._clients:
                if c.test(filter):
                    c.say(msg)
        do_say.call_async()

    def add_handler(self, msg_id, handler):
        logger.debug('add message handler %s::%s (%s)', self.name, msg_id, handler)
        handlers = self._handlers.get(msg_id, [])
        handlers.append(handler)
        self._handlers[msg_id] = handlers

    def remove_handler(self, msg_id, handler):
        handlers = self._handlers.get(msg_id, [])
        while True:
            try:
                handlers.remove(handler)
            except ValueError:
                break

    def process_message(self, msg):
        @async
        def do_process_message():
            logger.debug('processing income message %s::%s %s', self.name, msg.name, msg.data)
            processed = False
            for msg_id in [msg.name, '*']:
                handlers = self._handlers.get(msg_id, [])
                for h in handlers:
                    try:
                        processed = True
                        h(self._router, self, msg)
                    except StopIteration:
                        break
            if not processed:
                logger.warn('no handler for message %s::%s', self.name, msg.name)
        do_process_message.call_async()


class AbstractClient(object):
    def __init__(self, ident):
        self._ident = ident
        self.reindent()

    def reindent(self):
        self._tester = {}

        for k, v in self._ident.items():
            def add_tester(k, v):
                self._tester[k] = lambda x: x == v
            add_tester(k, v)

    @property
    def ident(self):
        return self._ident

    def test(self, filter):
        if filter is not None:
            if callable(filter):
                return filter(self._ident)
            assert(isinstance(filter, dict))
            for k, v in filter.items():
                t = self._tester.get(k, lambda x: False)
                if not t(v):
                    return False
        return True

    def say(self, msg):
        if isinstance(msg, (list, tuple)):
            msg = OutgoingMessage(*msg)
        assert(isinstance(msg, OutgoingMessage))
        self.post_message(msg)

    def post_message(self, msg):
        raise NotImplementedError()


class IncomeMessage(object):
    def __init__(self, name, data, sender=None):
        self._name = name
        self._data = data
        self._sender = sender

    @property
    def name(self):
        return self._name

    @property
    def data(self):
        return self._data

    @property
    def sender(self):
        return self._sender

    def reply(self, msg, filter=None):
        logger.debug('reply %s on %s', msg, self.name)
        if self._sender and self._sender.test(filter):
            self._sender.say(msg)


class OutgoingMessage(object):
    def __init__(self, name, data):
        self.name = name
        self.data = data

    @property
    def serialized(self):
        return json.dumps({'name': self.name, 'data': self.data})
