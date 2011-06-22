# -*- coding: utf-8 -*-
#
# Author: Pavel Reznikov <pashka.reznikov@gmail.com>
# Created: 6/22/11
#
# Id: $Id$

import json
from os import path as op

import tornado.web
import tornadio
import tornadio.router
import tornadio.server

from rohrpost import make_router
from rohrpost.channels.tornadio import TornadioClient
from rohrpost.core import IncomeMessage


def on_message(router, channel, msg):
    text = msg.data.get('text')
    if not text:
        return
    channel.say(('message', {'text': text}))


def on_direct_message(router, channel, msg):
    to = msg.data.get('to')
    text = msg.data.get('text')
    if not to or not text:
        return
    channel.say(('dm', {'text': text}), {'login': to})


router = make_router({
    'chat': {
        'message': on_message,
        'dm': on_direct_message,
    }
})


class ChatConnection(tornadio.SocketConnection):
    def on_open(self, *args, **kwargs):
        ident = {}
        self.client = TornadioClient(ident, self)
        router.get_channel('chat').connect(self.client)

    def on_close(self):
        router.get_channel('chat').disconnect(self.client)

    def on_message(self, message):
        message = json.loads(message)
        msg = IncomeMessage(message['name'], message['data'], sender=self.client)
        router.process_message('chat', msg)

        
ChatRouter = tornadio.get_router(ChatConnection)


class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the chatroom page"""
    def get(self):
        self.render("index.html")

ROOT = op.normpath(op.dirname(__file__))

application = tornado.web.Application(
    [(r"/", IndexHandler), ChatRouter.route()],
    enabled_protocols = ['websocket',
                         'flashsocket',
                         'xhr-multipart',
                         'xhr-polling'],
    flash_policy_port = 843,
    flash_policy_file = op.join(ROOT, 'flashpolicy.xml'),
    socket_io_port = 8001
)

if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    tornadio.server.SocketServer(application)
