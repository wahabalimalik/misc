# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Salebadel(models.Model):
	_name='sale.badel'


	name = fields.Char('Job',readonly="1")
	sale_approved_date = fields.Date()
	sale_person = fields.Many2one('res.users','Sale Person')
	payment_type = fields.Selection([('dd','DD'),('cc','CC')],default='dd',string="Payment Type")
	currency_id = fields.Many2one('res.currency', string='Currency', default=3)
	balance = fields.Monetary(currency_field='currency_id',readonly="1", string='Budget',compute='_compute_balance')
	sale_budget = fields.Monetary(currency_field='currency_id',string='Budget')
	customer_name = fields.Many2one('res.partner','Customer',readonly="1")
	delivery_type = fields.Selection([('p','Pick up'),('d','Delivery')],default='d',string="Delivery Type")
	date_approved = fields.Date()
	completion_date = fields.Date('Due Date')
	job_status = fields.Selection([('w','Waiting Approval'),('d','In Designing'),('p','In Production'),('f','Finished')],default="w",string="Job Status")
	invoiced_job = fields.Selection([('y','Yes'),('n','No')],string="Job Invoiced")
	filled_job = fields.Selection([('y','Yes'),('n','No')],string="Job Filed")
	varient = fields.Float('Variant')
	varient = fields.One2many('sale.badel.variant','var_id','Variation')
	payment = fields.One2many('sale.badel.line','sale_id')
	urgent = fields.Selection([('Yes','Yes'),('No','No')],default="No",string="Urgent")
	notes = fields.Text()
	today = fields.Date().today()
	total_budget = fields.Monetary('Total Amount',currency_field='currency_id',readonly = "1",compute='_compute_budget')

	@api.depends('varient')
	def _compute_budget(self):
		self.total_budget = self.sale_budget
		if self.varient:
			for x in self.varient:
				self.total_budget = self.total_budget + x.varient

	@api.multi
	@api.depends('varient','payment')
	def _compute_balance(self):
		self.balance = self.sale_budget
		if self.varient:
			for x in self.varient:
				self.balance = self.balance + x.varient

		if self.payment:
			for x in self.payment:
				self.balance = self.balance - x.payment

	@api.multi
	def action_confirm(self):
		design = self.env['design.badel']
		design.create({
            'name': self.name,
            'sales_person': self.sale_person.id,
            'customer_name': self.customer_name.id,
            'urgent': self.urgent,
            'start_date': self.today,
            'completion_date': self.completion_date
        })

	sequence = fields.Integer(string ='Job')
	_order   = 'sequence'

class SalebadelTree(models.Model):
	_name='sale.badel.line'
	date = fields.Date()
	payment = fields.Float()
	sale_id = fields.Many2one('sale.badel',ondelete='cascade', required=True)

class SalebadelVariant(models.Model):
	_name='sale.badel.variant'
	date = fields.Date()
	varient = fields.Float('Variant')
	var_id = fields.Many2one('sale.badel',ondelete='cascade', required=True)