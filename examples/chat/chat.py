# -*- coding: utf-8 -*-
#
# Author: Pavel Reznikov <pashka.reznikov@gmail.com>
# Created: 6/22/11
#
# Id: $Id$

from os import path as op
import logging

import tornado
import tornado.websocket
from tornado import httpserver, ioloop

from rohrpost import make_router
from rohrpost.channels.tornadoweb import rohrpost_route


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
