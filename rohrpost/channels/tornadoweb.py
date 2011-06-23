# -*- coding: utf-8 -*-
#
# Author: Pavel Reznikov <pashka.reznikov@gmail.com>
# Created: 6/21/11
#
# Id: $Id$

import json
import logging
from rohrpost.core import IncomeMessage
from tornado import ioloop, websocket
from rohrpost import AbstractClient


logger = logging.getLogger('rohrpost')


class TornadoClient(AbstractClient):
    def __init__(self, ident, connection):
        super(TornadoClient, self).__init__(ident)
        self.connection = connection

    def post_message(self, msg):
        msg_dump = json.dumps({'name': msg.name, 'data': msg.data})
        ioloop.IOLoop.instance().add_callback(self.connection.async_callback(self._post_to_socket, msg_dump))

    def _post_to_socket(self, msg):
        self.connection.write_message(msg)


class RohrpostTornadoConnection(websocket.WebSocketHandler):
    def initialize(self, **kwargs):
        self.router = kwargs.pop('router')

    def open(self, channel, *args, **kwargs):
        try:
            ident = self.request.arguments.get('ident')
            self.ident = json.loads(ident[0]) if ident else {}

            logger.debug('client %s connected to %s', self.ident, channel)
        except Exception:
            logger.warn('bad identification %s. disconnect', ident)
            self.close()
            return

        self.channel = channel
        self.client = TornadoClient(self.ident, self)
        self.router.get_channel(self.channel).connect(self.client)

    def on_message(self, message):
        try:
            message = json.loads(message)
        except Exception:
            logger.warn('bad income message: %s', message)
            return

        msg = IncomeMessage(message['name'], message['data'], sender=self.client)
        self.router.process_message(self.channel, msg)

    def on_close(self):
        logger.debug('client %s disconnected from %s', self.client.ident, self.channel)
        self.router.get_channel('chat').disconnect(self.client)


def rohrpost_route(prefix, router, channels):
    if prefix and prefix != '/':
        prefix += '/'
    prefix += '(' + '|'.join(channels) + ')'
    return prefix, RohrpostTornadoConnection, {'router': router}