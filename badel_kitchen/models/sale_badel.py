# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Salebadel(models.Model):
	_name='sale.badel'


	name = fields.Char('Sequence',readonly="1")
	sale_approved_date = fields.Date()
	sale_person = fields.Many2one('res.users','Sale Person')
	payment_type = fields.Selection([('dd','DD'),('cc','CC')],default='dd',string="Payment Type")
	balance = fields.Integer(readonly = "1",compute='_compute_balance')
	sale_budget = fields.Integer('Sale Budget')
	customer_name = fields.Many2one('res.partner','Customer',readonly="1")
	delivery_type = fields.Selection([('p','Pick up'),('d','Delivery')],default='d',string="Delivery Type")
	# date_approved = fields.Date()
	completion_date = fields.Date('Due Date')
	job_status = fields.Selection([('w','Waiting Approval'),('d','In Designing'),('p','In Production'),('f','Finished')],default="w",string="Job Status")
	invoiced_job = fields.Selection([('y','Yes'),('n','No')],string="Job Invoiced")
	filled_job = fields.Selection([('y','Yes'),('n','No')],string="Job Filled")
	# varient = fields.Float('Variant')
	varient = fields.One2many('sale.badel.variant','var_id','Variant')
	payment = fields.One2many('sale.badel.line','sale_id')
	urgent = fields.Selection([('Yes','Yes'),('No','No')],default="No",string="Urgent")
	notes = fields.Text()
	today = fields.Date().today()
	total_budget = fields.Integer(readonly = "1",compute='_compute_budget')

	@api.depends('varient')
	def _compute_budget(self):
		for y in self:
			y.total_budget = y.sale_budget
			if y.varient:
				for x in y.varient:
					y.total_budget = y.total_budget + x.varient

	@api.multi
	@api.depends('varient','payment')
	def _compute_balance(self):
		for y in self:
			y.balance = y.sale_budget
			if y.varient:
				for x in y.varient:
					y.balance = y.balance + x.varient

			if y.payment:
				for x in y.payment:
					y.balance = y.balance - x.payment

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

	sequence = fields.Integer(string ='Sequence')
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