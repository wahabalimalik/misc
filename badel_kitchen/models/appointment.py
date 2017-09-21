# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
import datetime

class appointmetSet(models.Model):
	_name='appointment.set'

	name = fields.Many2one('res.partner','Customer',required=True)
	appoint_date = fields.Datetime(string="Appoint Date")
	appoint_create = fields.Date(string="Appoint Creation", readonly="1" ,default=lambda self: fields.datetime.now())
	presentation_date = fields.Datetime(string="Presentation Date")
	job_oppor = fields.Selection([('high','High'),('low','Low'),('normal','Normal')],default='normal',string="Opportunity")
	appoint_notes = fields.Text('Important Notes')
	sale_person = fields.Many2one('res.users','Sale Person',domain=[('job_title','=','1')],required=True)
	currency_id = fields.Many2one('res.currency', string='Currency', default=3)
	budget = fields.Monetary(currency_field='currency_id',string='Budget')
	description = fields.Char(string="Description of Work")
	call_status = fields.Selection([('y','Yes'),('n','No')],string="Called Customer")
	today = fields.Date().today()
	completion_date = fields.Date('Due Date')
	invoice_ids = fields.Many2many("sale.badel")
	# states_by_color = fields.Selection([
	# 	('1' , 'call'),
	# 	])
	state = fields.Selection([
        ('not_yet','Not Called'),
		('call','Call'),
        ],default='not_yet')
	switch = fields.Selection([
        ('onn','ONN'),
		('off','OFF'),
        ],default='onn')

	def queru_subbmitted_btn(self):
		return self.write({'state' : 'call'})

	@api.multi
	def action_confirm(self):
		self.env['sale.badel'].create({
				'id' : self.id,
				'customer_name': self.name.id,
	            'sale_person': self.sale_person.id,
	            'sale_budget': self.budget,
	            'name': 'Job # %s' %(self.id),
	            'sale_approved_date': self.today,
	            'completion_date': self.completion_date,

	        })
		self.write({'switch': 'off'})
		# return {
		# 	'name':_('badel_kitchen sale_tree_glare'),
		# 	'view_mode': 'form',
		# 	'view_id': False,
		# 	'views': [(self.env.ref('badel_kitchen.sale_form_view_1').id,'form')],
		# 	'view_type': 'form',
		# 	'res_id' : self.id,
		# 	'res_model': 'sale.badel',
		# 	'type': 'ir.actions.act_window',
		# }
	@api.multi
	def action_confirm_undo(self):
		rec = self.env['sale.badel'].search([('id','=', self.id)]).unlink()
		self.write({'switch': 'onn'})

	sequence = fields.Integer(string ='Job')
	_order   = 'sequence'
