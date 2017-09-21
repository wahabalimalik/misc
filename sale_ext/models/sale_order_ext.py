# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrderLineExt(models.Model):

	_inherit = 'sale.order.line'
	percentage_allownce = fields.Float()

	@api.depends('percentage_allownce')
	def _compute_amount(self):
		super(SaleOrderLineExt, self)._compute_amount()
		self.price_subtotal = float(self.price_subtotal) + (float(self.percentage_allownce / 100) * float(self.price_subtotal))