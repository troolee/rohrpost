# -*- coding: utf-8 -*-
#
# Author: Pavel Reznikov <pashka.reznikov@gmail.com>
# Created: 6/23/11
#
# Id: $Id$

import logging


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
