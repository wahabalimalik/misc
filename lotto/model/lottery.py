# -*- coding: utf-8 -*-

from odoo import models, fields, api,exceptions,_

class lotto(models.Model):

	_name = 'lottery.lotto'

	name = fields.Many2one('lottery.name','Lottery Name')
	winning_num  = fields.Char('Winning Number', compute='_compute_lottery_win_num')
	start_date = fields.Datetime('Start Date')
	end_date = fields.Datetime('End Date')
	winning_count = fields.Char('Total Wins')
	blacklist = fields.One2many('res.blacklist','list_id','BlackList Numbers')
	total_lottery_sale = fields.Integer('Lotteries Sold',compute='_compute_lottery_counts')
	bets = fields.One2many('res.betsfrombranch','bet_id','Lottery Bets')
	winlist = fields.One2many('win.list','win_id')
	status = fields.Boolean(default = False)
	state = fields.Selection([('open', 'Open'), ('close', 'Close')],default='open')
	bet_counts = fields.One2many('bet.count', 'count_id')
	change_default_limit = fields.Boolean(default = False)
	max_limit = fields.Integer(default=1000)
	ez2 = fields.Char("EZ2")
	d4 = fields.Char("4D")
	swetres = fields.Char()
	fields_selector = fields.Selection([('ez2', 'Ez2'),('d4', 'D4'), ('swetres', 'Swetres')])

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


	@api.onchange('name')
	def onchange_bet(self):
		if self.name:
			if self.name.name == 'ez2':
				self.fields_selector = 'ez2'
			elif self.name.name == '4D':
				self.fields_selector = 'd4'
			elif self.name.name == 'swetres':
				self.fields_selector = 'swetres'

	@api.depends('ez2','d4','swetres')
	def _compute_lottery_win_num(self):
		if self.ez2 or self.d4 or self.swetres:
			self.winning_num = self.ez2 or self.d4 or self.swetres


	@api.multi
	def action_confirm(self):
		if self.winning_num:
			self.write({'status': True,'state' : 'close'})
		else:
			raise exceptions.ValidationError(_('Before closing bet you should have to enter winning number'))

	@api.multi
	def action_update(self):
		self.winlist.unlink()
		rec = self.bets.search([('name', '=', self.winning_num),('bet_id', '=', self.id)])

		for x in rec:
			self.winlist.create({
				'name': x.name,
	            'bet_amount' : x.bet_amount,
	            'branch':x.branch,
	            'bet_unique': x.bet_unique,
	            'win_id' : self.id
				})
		self.winning_count = len(rec)

	@api.depends('bets')
	def _compute_lottery_counts(self):
		for x in self:
			total_bets = len(x.bets)
			x.total_lottery_sale = total_bets

	def record_count(self,vals):
		rec = self.bets.search([('name', '=', vals),('bet_id', '=', self.id)])
		count = self.bet_counts.search([('name', '=', vals),('count_id', '=', self.id)])
		if count:
			count.bet_nubmer = len(rec)
		else:
			count.create({
				'name': vals,
				'bet_nubmer' : len(rec),
				'count_id' : self.id
				})
		self.checklimit()

	def checklimit(self):
		count = self.bet_counts.search([('bet_nubmer', '>=', self.max_limit),('count_id', '=', self.id)])
		if count:
			self.blacklist.create({
				'name': count.name,
				'list_id' :self.id
				})


class LotteryName(models.Model):
	_name = 'lottery.name'

	name = fields.Char()
	num_limit = fields.Integer()

class blacklist(models.Model):
	_name = 'res.blacklist'
	name = fields.Char()
	list_id = fields.Many2one('lottery.lotto',ondelete='cascade', required=True)

class lottery_bets_placing(models.Model):
	_name = 'res.betsfrombranch'
	name = fields.Char('Bets')
	bet_amount = fields.Float('Bet Amount')
	bet_unique = fields.Char('Bet Unique')
	branch = fields.Char('Branch')
	bet_id = fields.Many2one('lottery.lotto',ondelete='cascade')

class WinList(models.Model):
	_name = 'win.list'
	name = fields.Char('Bets')
	bet_amount = fields.Float('Bet Amount')
	bet_unique = fields.Char('Bet Unique')
	branch = fields.Char('Branch')
	win_id = fields.Many2one('lottery.lotto',ondelete='cascade')

class BetCount(models.Model):
	_name = 'bet.count'
	name = fields.Char()
	bet_nubmer = fields.Integer()
	count_id = fields.Many2one('lottery.lotto',ondelete='cascade')