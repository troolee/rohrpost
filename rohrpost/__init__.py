# -*- coding: utf-8 -*-
#
# Author: Pavel Reznikov <pashka.reznikov@gmail.com>
# Created: 6/21/11
#
# Id: $Id$

import logging
from core import *


logger = logging.getLogger('rohrpost')


def make_router(message_map):
    router = Router()
    for channel_name, messages in message_map.items():
        channel = Channel(channel_name, router)
        router.register_channel(channel_name, channel)
        for msg, handlers in messages.items():
            if isinstance(handlers, (list, tuple)):
                for handler in handlers:
                    channel.add_handler(msg, handler)
            else:
                channel.add_handler(msg, handlers)
    return router
