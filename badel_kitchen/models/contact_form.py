# -*- coding: utf-8 -*-
from odoo import models, fields

class Partner(models.Model):
	_inherit='res.partner'

	suburb = fields.Many2one('res.suburb')
	source_contact = fields.Selection([('1','Google'),('2','Facebook'),('3','Words of Mouth'),('4','Othrs')],default="1",string="How heard about us?")
	date_client_contact = fields.Date("Client First Contact")

class Suburb(models.Model):
	_name = 'res.suburb'
	name = fields.Char()

class Saleperson(models.Model):
	_inherit='res.users'

	job_title = fields.Selection([('1','Yes'),('2','No')],string="Sale Person",default='2')