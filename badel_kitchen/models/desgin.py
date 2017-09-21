# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Desingbadel(models.Model):
	_name='design.badel'

	name = fields.Char('Job',readonly="1")
	start_date = fields.Date()
	sales_person = fields.Many2one('res.users','Sale Person',readonly="1")
	customer_name = fields.Many2one('res.partner','Customer',readonly="1")
	job_status = fields.Selection([('1','1st Drawing'),('2','2nd Drawing'),('a','Approved'),('n','Nested')],string="Working Status")
	urgent = fields.Char(readonly="1")
	notes = fields.Text()
	today = fields.Date().today()
	first_desing = fields.Date(string="First Drawing")
	second_design = fields.Date(string="Second Drawing")
	third_design = fields.Date(string="Approved Drawing")
	fourth_desing = fields.Date(string="Nested Drawing")
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

	sequence = fields.Integer(string ='Job')
	_order   = 'sequence'