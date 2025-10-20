# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class RepairOrder(models.Model):
    _name = 'repair.order'
    _description = 'Ordem de Serviço'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    
    # Informações Básicas
    name = fields.Char(
        string='Número da OS',
        required=True,
        readonly=True,
        default=lambda self: _('Novo'),
        copy=False
    )
    
    partner_id = fields.Many2one(
        'res.partner',
        string='Cliente',
        required=True,
        tracking=True
    )
    
    partner_phone = fields.Char(
        string='Telefone',
        related='partner_id.phone',
        readonly=False,
        store=True
    )
    
    partner_mobile = fields.Char(
        string='Celular',
        related='partner_id.mobile',
        readonly=False,
        store=True
    )
    
    partner_email = fields.Char(
        string='E-mail',
        related='partner_id.email',
        readonly=False,
        store=True
    )
    
    # Informações do Dispositivo
    brand_id = fields.Many2one(
        'repair.brand',
        string='Marca',
        required=True,
        tracking=True
    )
    
    device_model_id = fields.Many2one(
        'repair.device.model',
        string='Modelo',
        required=True,
        domain="[('brand_id', '=', brand_id)]",
        tracking=True
    )
    
    device_imei = fields.Char(
        string='IMEI/Serial',
        help='Número IMEI ou serial do dispositivo'
    )
    
    device_color = fields.Char(
        string='Cor',
        help='Cor do dispositivo'
    )
    
    device_password = fields.Char(
        string='Senha/PIN',
        help='Senha ou PIN do dispositivo (será mantido em sigilo)'
    )
    
    accessories = fields.Text(
        string='Acessórios',
        help='Acessórios recebidos com o dispositivo (carregador, capa, etc)'
    )
    
    # Problema e Diagnóstico
    problem_description = fields.Text(
        string='Problema Relatado',
        required=True,
        tracking=True,
        help='Descrição do problema relatado pelo cliente'
    )
    
    diagnosis = fields.Text(
        string='Diagnóstico Técnico',
        tracking=True,
        help='Diagnóstico técnico do problema'
    )
    
    internal_notes = fields.Text(
        string='Observações Internas',
        help='Observações internas, visíveis apenas para a equipe técnica'
    )
    
    # Datas
    date_entry = fields.Datetime(
        string='Data de Entrada',
        required=True,
        default=fields.Datetime.now,
        tracking=True
    )
    
    date_expected = fields.Datetime(
        string='Previsão de Entrega',
        required=True,
        default=lambda self: fields.Datetime.now() + timedelta(days=3),
        tracking=True
    )
    
    date_completed = fields.Datetime(
        string='Data de Conclusão',
        tracking=True,
        readonly=True
    )
    
    date_delivered = fields.Datetime(
        string='Data de Entrega',
        tracking=True,
        readonly=True
    )
    
    # Status
    state = fields.Selection([
        ('draft', 'Rascunho'),
        ('received', 'Recebido'),
        ('diagnosis', 'Em Análise'),
        ('waiting_parts', 'Aguardando Peças'),
        ('waiting_approval', 'Aguardando Aprovação'),
        ('in_repair', 'Em Reparo'),
        ('testing', 'Em Teste'),
        ('done', 'Concluído'),
        ('delivered', 'Entregue'),
        ('cancelled', 'Cancelado')
    ], string='Status', default='draft', required=True, tracking=True)
    
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Urgente'),
        ('2', 'Muito Urgente'),
    ], string='Prioridade', default='0', tracking=True)
    
    # Técnico
    technician_id = fields.Many2one(
        'res.users',
        string='Técnico Responsável',
        tracking=True,
        default=lambda self: self.env.user
    )
    
    # Garantia
    warranty_days = fields.Integer(
        string='Dias de Garantia',
        default=90,
        help='Número de dias de garantia do serviço'
    )
    
    warranty_expire_date = fields.Date(
        string='Garantia até',
        compute='_compute_warranty_expire',
        store=True
    )
    
    # Linhas de Serviço
    service_line_ids = fields.One2many(
        'repair.order.line',
        'repair_id',
        string='Serviços e Peças'
    )
    
    # Valores
    amount_untaxed = fields.Monetary(
        string='Subtotal',
        compute='_compute_amounts',
        store=True,
        currency_field='currency_id'
    )
    
    amount_tax = fields.Monetary(
        string='Impostos',
        compute='_compute_amounts',
        store=True,
        currency_field='currency_id'
    )
    
    amount_total = fields.Monetary(
        string='Total',
        compute='_compute_amounts',
        store=True,
        currency_field='currency_id'
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Moeda',
        default=lambda self: self.env.company.currency_id.id,
        required=True
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Empresa',
        default=lambda self: self.env.company.id,
        required=True
    )
    
    # Anexos
    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Anexos',
        help='Fotos ou documentos relacionados ao reparo'
    )
    
    attachment_count = fields.Integer(
        string='Número de Anexos',
        compute='_compute_attachment_count'
    )
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('Novo')) == _('Novo'):
            vals['name'] = self.env['ir.sequence'].next_by_code('repair.order') or _('Novo')
        return super().create(vals)
    
    @api.depends('service_line_ids.price_subtotal')
    def _compute_amounts(self):
        for order in self:
            amount_untaxed = sum(order.service_line_ids.mapped('price_subtotal'))
            amount_tax = sum(order.service_line_ids.mapped('price_tax'))
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax,
            })
    
    @api.depends('date_delivered', 'warranty_days')
    def _compute_warranty_expire(self):
        for order in self:
            if order.date_delivered and order.warranty_days:
                order.warranty_expire_date = order.date_delivered.date() + timedelta(days=order.warranty_days)
            else:
                order.warranty_expire_date = False
    
    @api.depends('attachment_ids')
    def _compute_attachment_count(self):
        for order in self:
            order.attachment_count = len(order.attachment_ids)
    
    def action_confirm(self):
        self.write({'state': 'received'})
        return True
    
    def action_start_diagnosis(self):
        self.write({'state': 'diagnosis'})
        return True
    
    def action_start_repair(self):
        self.write({'state': 'in_repair'})
        return True
    
    def action_done(self):
        self.write({
            'state': 'done',
            'date_completed': fields.Datetime.now()
        })
        return True
    
    def action_deliver(self):
        self.write({
            'state': 'delivered',
            'date_delivered': fields.Datetime.now()
        })
        return True
    
    def action_cancel(self):
        self.write({'state': 'cancelled'})
        return True
    
    def action_print_receipt(self):
        return self.env.ref('repair_service.action_report_repair_receipt').report_action(self)
    
    @api.onchange('brand_id')
    def _onchange_brand_id(self):
        if self.brand_id:
            self.device_model_id = False


class RepairOrderLine(models.Model):
    _name = 'repair.order.line'
    _description = 'Linha de Ordem de Serviço'
    
    repair_id = fields.Many2one(
        'repair.order',
        string='Ordem de Serviço',
        required=True,
        ondelete='cascade'
    )
    
    product_id = fields.Many2one(
        'product.product',
        string='Produto/Serviço',
        required=True
    )
    
    description = fields.Text(
        string='Descrição'
    )
    
    quantity = fields.Float(
        string='Quantidade',
        default=1.0,
        required=True
    )
    
    price_unit = fields.Float(
        string='Preço Unitário',
        required=True
    )
    
    discount = fields.Float(
        string='Desconto (%)',
        default=0.0
    )
    
    tax_ids = fields.Many2many(
        'account.tax',
        string='Impostos'
    )
    
    price_subtotal = fields.Monetary(
        string='Subtotal',
        compute='_compute_amount',
        store=True,
        currency_field='currency_id'
    )
    
    price_tax = fields.Monetary(
        string='Impostos',
        compute='_compute_amount',
        store=True,
        currency_field='currency_id'
    )
    
    price_total = fields.Monetary(
        string='Total',
        compute='_compute_amount',
        store=True,
        currency_field='currency_id'
    )
    
    currency_id = fields.Many2one(
        related='repair_id.currency_id',
        string='Moeda',
        readonly=True
    )
    
    @api.depends('quantity', 'price_unit', 'discount', 'tax_ids')
    def _compute_amount(self):
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_ids.compute_all(
                price, 
                line.currency_id, 
                line.quantity, 
                product=line.product_id, 
                partner=line.repair_id.partner_id
            )
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.price_unit = self.product_id.lst_price
            self.description = self.product_id.get_product_multiline_description_sale()