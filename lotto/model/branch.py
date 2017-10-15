# -*- coding: utf-8 -*-

from odoo import models,fields,api,exceptions,_
import random

class branch_lottery(models.Model):
	_name = 'branch.lottery'

	@api.constrains('ez2','d4','swetres')
	def _check_size(self):
		if self.ez2:
			if "_" in self.ez2:
				raise exceptions.ValidationError(_('Not valid number'))
		if self.d4:
			if "_" in self.d4:
				raise exceptions.ValidationError(_('Not valid number'))
		if self.swetres:
			if "_" in self.swetres:
				raise exceptions.ValidationError(_('Not valid number'))
				
	name = fields.Many2one('lottery.name','Lottery Name')
	branch_name = fields.Many2one('res.branch','Branch Name', default=lambda self: self.env.user.branch_name)
	bet = fields.Char('Bet', size=18)
	bet_code = fields.Char('Bet Unique Code', default=lambda self: self.genrate_code())
	bet_amount = fields.Float('Bet Amount')
	date = fields.Datetime(default=fields.Datetime.now)
	ez2 = fields.Char("EZ2")
	d4 = fields.Char("4D")
	swetres = fields.Char()
	fields_selector = fields.Selection([('ez2', 'Ez2'),('d4', 'D4'), ('swetres', 'Swetres')])

	@api.onchange('name')
	def onchange_bet(self):
		if self.name:
			if self.name.name == 'ez2':
				self.fields_selector = 'ez2'
			elif self.name.name == '4D':
				self.fields_selector = 'd4'
			elif self.name.name == 'swetres':
				self.fields_selector = 'swetres'

	def genrate_code(self):
		code = ""
		nums = "1234567890QWERTYUIOPASDFGHJKLASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm"
		pw_length = 16

		for i in range(pw_length):
		    next_index = random.randrange(len(nums))
		    code = code + nums[next_index]
		return code

	@api.model
	def create(self,vals):
		design = self.env['lottery.lotto'].search([
			('name','=',vals['name']),
			('state','=','open'),
			('start_date','<',vals['date']),
			('end_date','>',vals['date']),
		])
		vals['bet'] = vals['ez2'] or vals['d4'] or vals['swetres']

		if design:
			for rec in design.blacklist:
				if rec.name == vals['bet']:
					raise exceptions.ValidationError(_('This Bet is block.Try some other one'))
					return True

			design.bets.create({
	            'name': vals['bet'],
	            'bet_amount' : vals['bet_amount'],
	            "bet_id" : design.id,
	            'branch':vals['branch_name'],
	            'bet_unique': vals['bet_code'],
	            })

			design.record_count(vals['bet'])

		else:
			raise exceptions.ValidationError(_('This bet is not available.Try some other one'))
			return True

		return super(branch_lottery,self).create(vals)