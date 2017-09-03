# -*- coding: utf-8 -*-

import urllib2

import logging
from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class SMS_Template(models.Model):
    _name = 'sms.templates'
    
    to = fields.Char()
    line = fields.Char()
    message = fields.Text()

    @api.multi
    def send(self):
    	get_param = self.env['ir.config_parameter'].get_param

        user = get_param('user', default='')
        password = get_param('password', default='')
        number = self.to
        message = self.message
        message = message.replace(" ", "%20")
        line = self.line
        url = get_param('url', default='')

        if not ',' in number:
        	_logger.info(">>>> Sendings sms to given number")
        	urllib2.urlopen(url+'?u=%s&p=%s&l=%s&n=%s&m=%s' %(user,password,line,number,message))
        	_logger.info('>>>>>Message sent')
        else:
        	print 'no'