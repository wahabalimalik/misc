# # -*- coding: utf-8 -*-

# from odoo import models, fields, api

# class lotto(models.Model):
# 	_name = 'lottery.old'

# 	name = fields.Many2one('res.lottery','Lottery Name')
# 	winning_num  = fields.Char('Winning Number')
# 	start_date = fields.Datetime('Start Date')
# 	end_date = fields.Datetime('End Date')
# 	winning_count = fields.Char('Total Wins')
# 	blacklist = fields.One2many('res.blacklist','list_id','BlackList Numbers')
# 	total_lottery_sale = fields.Char('Lotteries Sold')
# 	bets = fields.One2many('res.bets','bet_id','Lottery Bets')
# 	single_bet = fields.Char('Bet')
# 	branch_name = fields.Char()
# 	status = fields.Boolean(default = False)

# class blacklist(models.Model):
# 	_name = 'res.blacklist'
# 	name = fields.Char()
# 	list_id = fields.Many2one('lottery.lotto',ondelete='cascade', required=True)

# class lottery_name(models.Model):
# 	_name = 'res.lottery'
# 	name = fields.Char()

# class lottery_bets(models.Model):
# 	_name = 'res.bets'
# 	name = fields.Char('Bets')
# 	bet_id = fields.Many2one('lottery.lotto',ondelete='cascade', required=True)
