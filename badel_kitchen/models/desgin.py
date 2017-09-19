# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Desingbadel(models.Model):
	_name='design.badel'

	name = fields.Char('Sequence',readonly="1")
	start_date = fields.Date()
	sales_person = fields.Many2one('res.users','Sale Person')
	customer_name = fields.Many2one('res.partner','Customer')
	job_status = fields.Selection([('1','1st Drawing'),('2','2nd Drawing'),('a','Approved'),('n','Nested')],string="Working Status")
	urgent = fields.Char(readonly="1")
	notes = fields.Text()
	today = fields.Date().today()
	completion_date = fields.Date('Due Date',readonly="1")
	
	@api.multi
	def action_confirm(self):
		self.ensure_one()
		production = self.env['production.badel']
		production.create({
					'start_date': self.today,
					'urgent': self.urgent,
					'name': self.name,
					'completion_date': self.completion_date
		        })

	sequence = fields.Integer(string ='Sequence')
	_order   = 'sequence'