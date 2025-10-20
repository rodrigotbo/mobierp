# -*- coding: utf-8 -*-
from odoo import models, fields, api

class MobilePartCategory(models.Model):
    _name = 'mobile.part.category'
    _description = 'Categoria de Peça de Celular'
    _parent_name = 'parent_id'
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'
    
    name = fields.Char(
        string='Nome da Categoria',
        required=True,
        index=True
    )
    
    complete_name = fields.Char(
        string='Nome Completo',
        compute='_compute_complete_name',
        store=True
    )
    
    parent_id = fields.Many2one(
        'mobile.part.category',
        string='Categoria Pai',
        index=True,
        ondelete='cascade'
    )
    
    parent_path = fields.Char(index=True)
    
    child_id = fields.One2many(
        'mobile.part.category',
        'parent_id',
        string='Categorias Filhas'
    )
    
    product_count = fields.Integer(
        string='Quantidade de Produtos',
        compute='_compute_product_count'
    )
    
    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name
    
    @api.depends('parent_id')
    def _compute_product_count(self):
        for category in self:
            category.product_count = self.env['product.template'].search_count([
                ('mobile_part_category_id', 'child_of', category.id)
            ])
    
    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('Erro: Você não pode criar categorias recursivas.'))