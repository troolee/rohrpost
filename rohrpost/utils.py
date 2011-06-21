# -*- coding: utf-8 -*-
#
# Author: Pavel Reznikov <pashka.reznikov@gmail.com>
# Created: 6/21/11
#
# Id: $Id$

from functools import wraps
from threading import Thread


def async(func):
    @wraps(func)
    def call_async(*args, **kwargs):
        Thread(target=func, args=args, kwargs=kwargs).start()
    func.call_async = call_async
    return func

