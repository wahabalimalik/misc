# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Productbadel(models.Model):
	_name = "production.badel"

	name = fields.Char()
	cutting_date = fields.Date()
	edging_date = fields.Date()
	assembly_date = fields.Date()
	poly_picked_date = fields.Date()
	poly_dropped_date = fields.Date()
	quality_control_date = fields.Date()
	delivery_date = fields.Date()
	ready_to_invoice = fields.Selection([('y','Yes'),('n','No')],string="Ready To Invoice")
	invoiced = fields.Selection([('y','Yes'),('n','No')],string="Invoiced")
	urgent = fields.Selection([('y','Yes'),('n','No')],string="Urgent")
	job_status = fields.Selection([('q','Queue'),('f','Finished'),('in','In Production')],string="Job status")
	start_date = fields.Date()
	department = fields.Selection([('c','Cutting'),('e','Edging'),('a','Assembly'),('p','Poly Picked'),('q','Quality Control')],string="Departement")
	notes = fields.Text()