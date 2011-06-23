# -*- coding: utf-8 -*-
#
# Author: Pavel Reznikov <pashka.reznikov@gmail.com>
# Created: 6/22/11
#
# Id: $Id$

import logging

import os
import tornado
import tornado.websocket
from tornado import httpserver, ioloop, web

from rohrpost import make_router
from rohrpost.channels.tornadoweb import rohrpost_route

logging.getLogger().setLevel(logging.DEBUG)


router = make_router({
    'chat': {
        'message': 'handlers.on_message',
        'dm': 'handlers.on_direct_message',
        '*': 'handlers.on_def_message',
    }
})

class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("index.html")

ROOT = os.path.abspath(os.path.dirname(__file__))

application = tornado.web.Application(
    [
            (r"/", IndexHandler),
            (r'/(.*\.js)', web.StaticFileHandler, {"path": ROOT}),
            rohrpost_route(r'/ws', router, ['chat']),
    ]
)

if __name__ == "__main__":
    http_server = httpserver.HTTPServer(application)
    http_server.listen(8001)
    ioloop.IOLoop.instance().start()
