# -*- coding: utf-8 -*-
from odoo import models, fields, api

class RepairBrand(models.Model):
    _name = 'repair.brand'
    _description = 'Marca de Dispositivo'
    _order = 'name'
    
    name = fields.Char(
        string='Marca',
        required=True,
        help='Nome da marca do dispositivo (ex: Samsung, Apple, Motorola)'
    )
    
    active = fields.Boolean(
        string='Ativo',
        default=True
    )
    
    device_model_ids = fields.One2many(
        'repair.device.model',
        'brand_id',
        string='Modelos'
    )
    
    device_count = fields.Integer(
        string='Quantidade de Modelos',
        compute='_compute_device_count'
    )
    
    @api.depends('device_model_ids')
    def _compute_device_count(self):
        for brand in self:
            brand.device_count = len(brand.device_model_ids)
    
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'O nome da marca deve ser único!')
    ]