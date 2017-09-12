# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Productbadel(models.Model):
	_name = "production.badel"

	name = fields.Char('Sequence',readonly="1")
	cutting_date = fields.Date()
	edging_date = fields.Date()
	assembly_date = fields.Date()
	poly_picked_date = fields.Date()
	poly_dropped_date = fields.Date()
	quality_control_date = fields.Date()
	completion_date = fields.Date('Due Date',readonly="1")
	
	urgent = fields.Selection([('Yes','Yes'),('No','No')],string="Urgent",readonly="1")
	job_status = fields.Selection([('q','Queue'),('f','Finished'),('in','In Production')],string="Job status")
	start_date = fields.Date()
	department = fields.Selection([('c','Cutting'),('e','Edging'),('a','Assembly'),('p','Poly Picked'),('q','Quality Control')],string="Departement")
	notes = fields.Text()

	@api.multi
	def action_confirm(self):
		design = self.env['sale.badel'].search([('name' ,'=',self.name)])
		design.write({'job_status': self.job_status})


