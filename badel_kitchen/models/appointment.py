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
	call_status = fields.Selection([('y','Yes'),('n','No')],string="Called Customer")
	state     = fields.Selection([
        ('not_yet','Not Called'),
		('call','Call'),
        ],default='not_yet')

	def queru_subbmitted_btn(self):
		return self.write({'state' : 'call'})

	@api.multi
	def action_confirm(self):
		self.ensure_one()
		sale = self.env['sale.badel']
		if len(sale) > 1:
			for x in sale:
				x.create({
		            'customer_name': self.name.id,
		            'sale_person': self.sale_person.id,
		            'sale_budget': self.budget,
		            'name': 'Order # %s' %(self.id),
		        })
		else:
			sale.create({
		            'customer_name': self.name.id,
		            'sale_person': self.sale_person.id,
		            'sale_budget': self.budget,
		            'name': 'Order # %s' %(self.id),
		        })

		# return {
	 #        'view_type': 'form',
	 #        'view_mode': 'form',
	 #        'res_model': 'sale.badel',
	 #        'target': 'current',
	 #        'res_id': self.env.ref('action_list_sales'),
	 #        'type': 'ir.actions.act_window'
	 #    }
