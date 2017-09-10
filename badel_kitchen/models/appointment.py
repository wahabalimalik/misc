# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime

class appointmetSet(models.Model):
	_name='appointment.set'

	name = fields.Many2one('res.partner','Customer',required=True)
	appoint_date = fields.Datetime(string="Appoint Date")
	presentation_date = fields.Datetime(string="Presentation Date")
	job_oppor = fields.Selection([('high','High'),('low','Low'),('normal','Normal')],default='normal',string="Opportunity")
	appoint_notes = fields.Text()
	sale_person = fields.Many2one('res.users','Sale Person',required=True)
	budget = fields.Integer()
	description = fields.Char(string="Description of Work")


	@api.multi
	def action_confirm(self):
		print "ddddddddddddddddddddddddd"
		self.ensure_one()
		sale = self.env['sale.badel']
		if len(sale) > 1:
			for x in sale:
				x.create({
		            'customer_name': self.name.id,
		            'sale_person': self.sale_person.id,
		            'sale_budget': self.budget,
		            'name': 'SEQ # %s' %(self.id),
		        })
		else:
			sale.create({
		            'customer_name': self.name.id,
		            'sale_person': self.sale_person.id,
		            'sale_budget': self.budget,
		            'name': 'SEQ # %s' %(self.id),
		        })
