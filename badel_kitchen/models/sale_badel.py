# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Salebadel(models.Model):
	_name='sale.badel'

	name = fields.Char('Sequence',readonly="1")
	sale_approved_date = fields.Date()
	sale_person = fields.Many2one('res.users','Sale Person')
	payment_type = fields.Selection([('dd','DD'),('cc','CC')],default='dd',string="Payment Type")
	balance = fields.Integer(readonly = "1",compute='_compute_balance')
	sale_budget = fields.Integer()
	customer_name = fields.Many2one('res.partner','Customer')
	delivery_type = fields.Selection([('p','Pick up'),('d','Delivery')],default='d',string="Delivery Type")
	date_approved = fields.Date()
	completion_date = fields.Date()
	completed_job = fields.Selection([('y','Yes'),('n','No')],string="Job Completed")
	invoiced_job = fields.Selection([('y','Yes'),('n','No')],string="Job Invoiced")
	filled_job = fields.Selection([('y','Yes'),('n','No')],string="Job Filled")
	varient = fields.Float('Variant')
	payment = fields.One2many('sale.badel.line','sale_id')

	@api.multi
	@api.depends('varient','payment')
	def _compute_balance(self):

		self.balance = self.sale_budget
		if self.varient:
			self.balance = self.sale_budget + self.varient

		if self.payment:
			for x in self.payment:
				self.balance = self.balance - x.payment

class SalebadelTree(models.Model):
	_name='sale.badel.line'
	date = fields.Date()
	payment = fields.Float()
	sale_id = fields.Many2one('sale.badel',ondelete='cascade', required=True)