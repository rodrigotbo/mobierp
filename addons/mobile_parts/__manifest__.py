# -*- coding: utf-8 -*-
{
    'name': 'MobiERP - Peças e Acessórios',
    'version': '17.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Gestão de peças e acessórios para celulares',
    'description': """
        Módulo de Peças e Acessórios - MobiERP
        =======================================
        
        Funcionalidades:
        - Controle de estoque especializado para peças
        - Categorização por tipo de peça
        - Compatibilidade com modelos
        - Alertas de estoque mínimo
        - Rastreabilidade de uso em reparos
    """,
    'author': 'MobiERP',
    'website': 'https://github.com/rodrigotbo/mobierp',
    'depends': [
        'stock',
        'product',
        'repair_service',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/mobile_parts_data.xml',
        'views/mobile_part_views.xml',
        'views/mobile_part_category_views.xml',
        'views/mobile_parts_menu.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}