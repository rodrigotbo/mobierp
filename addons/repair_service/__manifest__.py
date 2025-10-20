# -*- coding: utf-8 -*-
{
    'name': 'MobiERP - Assistência Técnica',
    'version': '17.0.1.0.0',
    'category': 'Services',
    'summary': 'Gestão completa de ordens de serviço para assistência técnica de celulares',
    'description': """
        Módulo de Assistência Técnica - MobiERP
        ========================================
        
        Funcionalidades:
        - Cadastro de ordens de serviço
        - Controle de equipamentos (marca, modelo, IMEI)
        - Status de serviços
        - Controle de garantia
        - Histórico por cliente
        - Impressão de comprovantes
        - Anexo de fotos e documentos
    """,
    'author': 'MobiERP',
    'website': 'https://github.com/rodrigotbo/mobierp',
    'depends': [
        'base',
        'sale',
        'stock',
        'account',
        'mail',
        'contacts',
    ],
    'data': [
        'security/repair_security.xml',
        'security/ir.model.access.csv',
        'data/repair_sequence.xml',
        'data/repair_data.xml',
        'views/repair_order_views.xml',
        'views/repair_device_views.xml',
        'views/repair_brand_views.xml',
        'views/repair_menu.xml',
        'reports/repair_order_report.xml',
        'reports/repair_receipt_template.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'repair_service/static/src/css/repair_style.css',
            'repair_service/static/src/js/repair_widget.js',
        ],
    },
    'demo': [
        'data/repair_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'icon': '/repair_service/static/description/icon.png',
}