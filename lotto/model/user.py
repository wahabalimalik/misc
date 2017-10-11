# -*- coding: utf-8 -*-

from odoo import models, fields, api

class lotto_operator(models.Model):
	_inherit = 'res.users'

	branch_name = fields.Many2one('res.branch','Branch Name')
	urole = fields.Selection([('1','Operator'),('2','Manager')],default="1",string="User Role")

class branch(models.Model):
	_name = 'res.branch'
	name = fields.Char()
	address = fields.Char()
	phone = fields.Char()