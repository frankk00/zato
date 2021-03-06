# -*- coding: utf-8 -*-

"""
Copyright (C) 2010 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
import logging
from contextlib import closing
from traceback import format_exc

# Zato
from zato.common import zato_namespace
from zato.common.broker_message import MESSAGE_TYPE
from zato.server.service import Service

success_code = 0
success = '<error_code>{}</error_code>'.format(success_code)

logger = logging.getLogger(__name__)

class AdminService(Service):
    """ A Zato admin service, part of the API.
    """
    def __init__(self):
        super(AdminService, self).__init__()
        
    def before_handle(self):
        request = self.request.input.toDict()
        for k, v in request.items():
            if 'password' in k:
                request[k] = '*****'

        self.logger.info('cid:[{}], name:[{}], SIO request:[{}]'.format(self.cid, self.name, request))
        
    def handle(self, *args, **kwargs):
        raise NotImplementedError('Should be overridden by subclasses')
    
    def after_handle(self):
        payload = self.response.payload
        response = payload if isinstance(payload, basestring) else payload.getvalue()
            
        self.logger.info('cid:[{}], name:[{}], response:[{}]'.format(self.cid, self.name, response))
    
    def get_data(self, *args, **kwargs):
        raise NotImplementedError('Should be overridden by subclasses')
    
class AdminSIO(object):
    namespace = zato_namespace

class Ping(AdminService):
    class SimpleIO(AdminSIO):
        output_required = ('pong',)
        response_elem = 'zato_ping_response'
        
    def handle(self):
        self.response.payload.pong = 'zato'
    
class Ping2(Ping):
    class SimpleIO(Ping.SimpleIO):
        response_elem = 'zato_ping2_response'

class ChangePasswordBase(AdminService):
    """ A base class for handling the changing of any of the ODB passwords.
    """
    class SimpleIO(AdminSIO):
        input_required = ('id', 'password1', 'password2')

    def _handle(self, class_, auth_func, action, name_func=None, msg_type=MESSAGE_TYPE.TO_PARALLEL_ALL,
                *args, **kwargs):

        with closing(self.odb.session()) as session:
            try:
                if not self.request.input.password1:
                    raise Exception('Password must not be empty')

                if not self.request.input.password2:
                    raise Exception('Password must be repeated')

                if self.request.input.password1 != self.request.input.password2:
                    raise Exception('Passwords need to be the same')

                auth = session.query(class_).\
                    filter(class_.id==self.request.input.id).\
                    one()

                auth_func(auth, self.request.input.password1)

                session.add(auth)
                session.commit()

                if msg_type:
                    name = name_func(auth) if name_func else auth.name

                    self.request.input.action = action
                    self.request.input.name = name
                    self.request.input.password = auth.password
                    self.request.input.salt = kwargs.get('salt')
                    self.broker_client.publish(self.request.input, msg_type=msg_type)

            except Exception, e:
                msg = 'Could not update the password, e:[{}]'.format(format_exc(e))
                self.logger.error(msg)
                session.rollback()

                raise
