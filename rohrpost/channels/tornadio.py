# -*- coding: utf-8 -*-
#
# Author: Pavel Reznikov <pashka.reznikov@gmail.com>
# Created: 6/21/11
#
# Id: $Id$

import json
from rohrpost import AbstractClient


class TornadioClient(AbstractClient):
    def __init__(self, ident, connection):
        super(TornadioClient, self).__init__(ident)
        self.connection = connection

    def post_message(self, msg):
        msg_dump = json.dumps({'name': msg.name, 'data': msg.data})
        self.connection.send(msg_dump)
