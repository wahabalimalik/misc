# -*- coding: utf-8 -*-
from odoo import models, fields

class Partner(models.Model):
	_inherit='res.partner'

	suburb = fields.Many2one('res.suburb')
	source_contact = fields.Char('"Contact From"')
	date_client_contact = fields.Date("Client First Contact")

class Suburb(models.Model):
	_name = 'res.suburb'
	name = fields.Char()