# -*- coding: utf-8 -*-

from odoo import models,fields,api,exceptions,_
import random

class branch_lottery(models.Model):
	_name = 'branch.lottery'

	@api.constrains('bet')
	def _check_size(self):
		if len(self.bet) > self.name.num_limit:
			raise exceptions.ValidationError(_('Entered number exceed limits.It must be below or equal to %s' %(self.name.num_limit)))

	name = fields.Many2one('lottery.name','Lottery Name')
	branch_name = fields.Many2one('res.branch','Branch Name', default=lambda self: self.env.user.branch_name)
	bet = fields.Char('Bet', size=18)
	bet_code = fields.Char('Bet Unique Code', default=lambda self: self.genrate_code())
	bet_amount = fields.Float('Bet Amount')
	date = fields.Datetime(default=fields.Datetime.now)

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
		if design:
			if len(vals['bet']) > design.name.num_limit:
				raise exceptions.ValidationError(_('This Bet number is not allowed to be longer then %s' %(design.name.num_limit)))
				return True

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