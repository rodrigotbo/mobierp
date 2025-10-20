# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    repair_order_ids = fields.One2many(
        'repair.order',
        'partner_id',
        string='Ordens de Serviço'
    )
    
    repair_order_count = fields.Integer(
        string='Quantidade de OS',
        compute='_compute_repair_order_count'
    )
    
    total_repairs = fields.Monetary(
        string='Total em Reparos',
        compute='_compute_repair_totals',
        currency_field='currency_id'
    )
    
    @api.depends('repair_order_ids')
    def _compute_repair_order_count(self):
        for partner in self:
            partner.repair_order_count = len(partner.repair_order_ids)
    
    @api.depends('repair_order_ids.amount_total', 'repair_order_ids.state')
    def _compute_repair_totals(self):
        for partner in self:
            delivered_orders = partner.repair_order_ids.filtered(lambda r: r.state == 'delivered')
            partner.total_repairs = sum(delivered_orders.mapped('amount_total'))
    
    def action_view_repair_orders(self):
        action = self.env.ref('repair_service.action_repair_order').read()[0]
        action['domain'] = [('partner_id', '=', self.id)]
        action['context'] = {'default_partner_id': self.id}
        return action