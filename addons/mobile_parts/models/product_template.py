# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    is_mobile_part = fields.Boolean(
        string='É Peça de Celular',
        default=False,
        help='Marque se este produto é uma peça ou acessório de celular'
    )
    
    mobile_part_category_id = fields.Many2one(
        'mobile.part.category',
        string='Categoria de Peça',
        help='Categoria específica para peças de celular'
    )
    
    part_type = fields.Selection([
        ('screen', 'Tela/Display'),
        ('battery', 'Bateria'),
        ('camera', 'Câmera'),
        ('speaker', 'Alto-falante'),
        ('mic', 'Microfone'),
        ('charging_port', 'Conector de Carga'),
        ('button', 'Botão'),
        ('flex', 'Flex/Cabo'),
        ('board', 'Placa'),
        ('housing', 'Carcaça/Tampa'),
        ('sim_tray', 'Bandeja SIM'),
        ('accessory', 'Acessório'),
        ('tool', 'Ferramenta'),
        ('other', 'Outro')
    ], string='Tipo de Peça')
    
    compatible_brand_ids = fields.Many2many(
        'repair.brand',
        'product_brand_compatibility_rel',
        'product_id',
        'brand_id',
        string='Marcas Compatíveis'
    )
    
    compatible_model_ids = fields.Many2many(
        'repair.device.model',
        'product_model_compatibility_rel',
        'product_id',
        'model_id',
        string='Modelos Compatíveis'
    )
    
    part_quality = fields.Selection([
        ('original', 'Original'),
        ('oem', 'OEM'),
        ('premium', 'Premium/AAA'),
        ('standard', 'Padrão'),
        ('generic', 'Genérico')
    ], string='Qualidade', default='standard')
    
    warranty_months = fields.Integer(
        string='Garantia (meses)',
        default=3,
        help='Período de garantia em meses'
    )
    
    stock_location = fields.Char(
        string='Localização no Estoque',
        help='Ex: Gaveta A3, Prateleira B2'
    )
    
    min_stock_alert = fields.Float(
        string='Estoque Mínimo',
        default=5.0,
        help='Quantidade mínima para alerta de reposição'
    )
    
    repair_time_estimate = fields.Float(
        string='Tempo Estimado de Reparo (min)',
        help='Tempo médio necessário para instalação desta peça'
    )
    
    @api.onchange('is_mobile_part')
    def _onchange_is_mobile_part(self):
        if self.is_mobile_part:
            self.type = 'product'
            self.tracking = 'lot'
        else:
            self.mobile_part_category_id = False
            self.part_type = False
            self.compatible_brand_ids = False
            self.compatible_model_ids = False
    
    @api.depends('qty_available', 'min_stock_alert')
    def _compute_stock_alert(self):
        for product in self:
            if product.is_mobile_part and product.qty_available <= product.min_stock_alert:
                # Trigger alert (can be customized to send notification)
                product.message_post(
                    body=f"⚠️ Alerta de Estoque Baixo: {product.name} - Quantidade atual: {product.qty_available}"
                )