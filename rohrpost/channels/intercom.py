# -*- coding: utf-8 -*-
#
# Author: Pavel Reznikov <pashka.reznikov@gmail.com>
# Created: 6/21/11
#
# Id: $Id$

from rohrpost.core import AbstractClient


class IntercomClient(AbstractClient):
    def __init__(self, ident, handler):
        super(IntercomClient, self).__init__(ident)
        self._handler = handler

    def post_message(self, msg):
        self._handler(self, msg)
