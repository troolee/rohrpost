# -*- coding: utf-8 -*-
#
# Author: Pavel Reznikov <pashka.reznikov@gmail.com>
# Created: 6/22/11
#
# Id: $Id$

import json
from os import path as op
import logging

import tornado
import tornado.websocket
from tornado import httpserver, ioloop

from rohrpost import make_router
from rohrpost.channels.tornadoweb import TornadoClient, RohrpostTornadoConnection, rohrpost_route
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


def on_def_message(router, channel, msg):
    logging.debug('default handler on %s::%s %s', channel.name, msg.name, msg.data)


router = make_router({
    'chat': {
        'message': on_message,
        'dm': on_direct_message,
        '*': on_def_message,
    }
})

class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the chatroom page"""
    def get(self, *args, **kwargs):
        self.render("index.html")

ROOT = op.normpath(op.dirname(__file__))

application = tornado.web.Application(
    [
            (r"/", IndexHandler),
            rohrpost_route(r'/ws', router, ['chat']),
    ]
)

if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    http_server = httpserver.HTTPServer(application)
    http_server.listen(8001)
    ioloop.IOLoop.instance().start()
