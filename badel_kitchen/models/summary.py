# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SummaryBadel(models.Model):
	_name="summary.badel"

	name=fields.Char()
	customer_name = fields.Many2one('res.partner','Customer Name')
	sale_person = fields.Many2one('res.users','Sale Person')
	budget = fields.Integer('Budget')
	balance = fields.Integer('Balance')
	job_status = fields.Selection([('q','Queue'),('f','Finished'),('in','In Production')],string="Job status")
	invoiced = fields.Selection([('y','Yes'),('n','No')],string="Invoiced")
	department = fields.Selection([('a','Appointment'),('s','Sale'),('d','Design'),('p','Production')],string="Departement")

	sequence = fields.Integer(string ='Sequence')
	_order   = 'sequence'
