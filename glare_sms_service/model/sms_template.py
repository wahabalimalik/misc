# -*- coding: utf-8 -*-

import urllib2,time

import logging
from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class SMS_Template(models.TransientModel):
    _name = 'sms.templates'
    
    to = fields.Char()
    line = fields.Char()
    message = fields.Text()

    @api.onchange('to')
    def onload(self):
        numbers = ''
        active_class =self.env['res.partner'].browse(self._context.get('active_ids'))
        if len(active_class) > 1:
            for rec in active_class:
                if rec.mobile != False:
                    numbers = numbers + rec.mobile + ','
        else:
            numbers = numbers + active_class.mobile
        self.to = numbers

    @api.constrains('message')
    def message_check(self):
        if not self.message:
            raise ValidationError(_('You should have to type some message..'))

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
            number = number[:-1]
            if number.startswith('05'):
                line = 2
            elif number.startswith('07'):
                line = 3
            else:
                line = 1
            _logger.info(">>>> Sendings sms to number : %s" %(number))
            try:
                urllib2.urlopen(url+'?u=%s&p=%s&l=%s&n=%s&m=%s' %(user,password,line,number,message))
                _logger.info('>>>>>Message sent')
            except Exception as e:
                raise ValidationError(_('Facing error something like : [%s]' %(e)))
        else:
            bulk_numbers = number.split(',')
            for x in bulk_numbers[:-1]:
                if x.startswith('05'):
                    line = 2
                elif x.startswith('07'):
                    line = 3
                else:
                    line = 1

                _logger.info(">>>> Sendings sms to number : %s" %(x))
                try:
                    urllib2.urlopen(url+'?u=%s&p=%s&l=%s&n=%s&m=%s' %(user,password,line,x,message))
                    _logger.info('>>>>>Message sent')
                    time.sleep( 5 )
                except Exception as e:
                    raise ValidationError(_('Facing error something like : [%s]' %(e)))