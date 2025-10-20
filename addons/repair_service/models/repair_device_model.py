# -*- coding: utf-8 -*-
from odoo import models, fields, api

class RepairDeviceModel(models.Model):
    _name = 'repair.device.model'
    _description = 'Modelo de Dispositivo'
    _order = 'brand_id, name'
    
    name = fields.Char(
        string='Modelo',
        required=True,
        help='Nome do modelo do dispositivo (ex: Galaxy S23, iPhone 14)'
    )
    
    brand_id = fields.Many2one(
        'repair.brand',
        string='Marca',
        required=True,
        ondelete='cascade'
    )
    
    active = fields.Boolean(
        string='Ativo',
        default=True
    )
    
    display_name = fields.Char(
        string='Nome Completo',
        compute='_compute_display_name',
        store=True
    )
    
    @api.depends('name', 'brand_id.name')
    def _compute_display_name(self):
        for model in self:
            if model.brand_id:
                model.display_name = f'{model.brand_id.name} {model.name}'
            else:
                model.display_name = model.name
    
    _sql_constraints = [
        ('name_brand_unique', 'unique(name, brand_id)', 'Este modelo já existe para esta marca!')
    ]