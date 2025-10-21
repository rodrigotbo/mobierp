#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de inicialização do MobiERP
Configura o sistema após a primeira instalação
"""

import xmlrpc.client
import time
import sys

# Configurações de conexão
url = "http://localhost:8069"
db = "mobierp"
username = "admin"
password = "admin"

def wait_for_odoo():
    """Aguarda o Odoo estar pronto"""
    max_attempts = 30
    for i in range(max_attempts):
        try:
            common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
            version = common.version()
            print(f"✓ Odoo {version['server_version']} está rodando!")
            return True
        except:
            print(f"Aguardando Odoo iniciar... ({i+1}/{max_attempts})")
            time.sleep(5)
    return False

def setup_mobierp():
    """Configura o MobiERP após instalação"""
    
    # Conectar ao Odoo
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    
    if not uid:
        print("❌ Erro: Não foi possível autenticar. Verifique as credenciais.")
        return False
    
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    print("✓ Conectado ao Odoo com sucesso!")
    
    # 1. Desinstalar módulos desnecessários
    print("\n📦 Limpando módulos desnecessários...")
    unnecessary_modules = [
        'crm', 'website', 'mass_mailing', 'survey', 'hr', 
        'fleet', 'lunch', 'maintenance', 'quality_control',
        'mrp', 'sign', 'website_sale', 'website_blog',
        'hr_holidays', 'hr_expense', 'project', 'helpdesk',
        'documents', 'planning', 'marketing_automation'
    ]
    
    for module_name in unnecessary_modules:
        try:
            module_ids = models.execute_kw(db, uid, password,
                'ir.module.module', 'search',
                [[['name', '=', module_name], ['state', '=', 'installed']]])
            
            if module_ids:
                models.execute_kw(db, uid, password,
                    'ir.module.module', 'button_immediate_uninstall', [module_ids])
                print(f"  ✓ Desinstalado: {module_name}")
        except:
            pass  # Módulo não existe ou não está instalado
    
    # 2. Instalar módulos do MobiERP
    print("\n🚀 Instalando módulos MobiERP...")
    mobierp_modules = ['repair_service', 'mobile_parts']
    
    for module_name in mobierp_modules:
        module_ids = models.execute_kw(db, uid, password,
            'ir.module.module', 'search',
            [[['name', '=', module_name]]])
        
        if module_ids:
            models.execute_kw(db, uid, password,
                'ir.module.module', 'button_immediate_install', [module_ids])
            print(f"  ✓ Instalado: {module_name}")
    
    # 3. Configurar empresa padrão
    print("\n🏢 Configurando empresa...")
    company_id = models.execute_kw(db, uid, password,
        'res.company', 'search',
        [[['id', '=', 1]]], {'limit': 1})
    
    if company_id:
        models.execute_kw(db, uid, password,
            'res.company', 'write',
            [company_id, {
                'name': 'MobiERP Assistência Técnica',
                'street': 'Rua Principal, 123',
                'city': 'São Paulo',
                'state_id': 25,  # São Paulo
                'country_id': 31,  # Brasil
                'zip': '01000-000',
                'phone': '(11) 3000-0000',
                'email': 'contato@mobierp.com.br',
                'website': 'www.mobierp.com.br',
                'currency_id': 6,  # BRL
                'vat': '00.000.000/0001-00'
            }])
        print("  ✓ Empresa configurada: MobiERP Assistência Técnica")
    
    # 4. Configurar usuário admin
    print("\n👤 Configurando usuário administrador...")
    admin_id = models.execute_kw(db, uid, password,
        'res.users', 'search',
        [[['login', '=', 'admin']]], {'limit': 1})
    
    if admin_id:
        models.execute_kw(db, uid, password,
            'res.users', 'write',
            [admin_id, {
                'name': 'Administrador MobiERP',
                'email': 'admin@mobierp.com.br',
                'tz': 'America/Sao_Paulo',
                'lang': 'pt_BR'
            }])
        print("  ✓ Usuário admin configurado")
    
    # 5. Criar usuário demo (técnico)
    print("\n👥 Criando usuário de demonstração...")
    try:
        demo_user_id = models.execute_kw(db, uid, password,
            'res.users', 'create',
            [{
                'name': 'João Técnico',
                'login': 'tecnico',
                'password': 'tecnico123',
                'email': 'tecnico@mobierp.com.br',
                'tz': 'America/Sao_Paulo',
                'lang': 'pt_BR',
                'groups_id': [(6, 0, [
                    models.execute_kw(db, uid, password,
                        'res.groups', 'search',
                        [[['name', '=', 'Técnico']]], {'limit': 1})[0]
                ])]
            }])
        print("  ✓ Usuário técnico criado (login: tecnico, senha: tecnico123)")
    except:
        print("  ⚠ Usuário técnico já existe ou não pôde ser criado")
    
    # 6. Criar produtos/serviços padrão
    print("\n📦 Criando produtos e serviços padrão...")
    
    services = [
        {'name': 'Troca de Tela', 'list_price': 150.00, 'type': 'service'},
        {'name': 'Troca de Bateria', 'list_price': 80.00, 'type': 'service'},
        {'name': 'Troca de Conector de Carga', 'list_price': 60.00, 'type': 'service'},
        {'name': 'Formatação e Backup', 'list_price': 50.00, 'type': 'service'},
        {'name': 'Desbloqueio', 'list_price': 100.00, 'type': 'service'},
        {'name': 'Diagnóstico', 'list_price': 30.00, 'type': 'service'},
    ]
    
    for service in services:
        try:
            models.execute_kw(db, uid, password,
                'product.template', 'create',
                [{
                    'name': service['name'],
                    'list_price': service['list_price'],
                    'type': service['type'],
                    'categ_id': 1,
                    'sale_ok': True,
                    'purchase_ok': False,
                }])
            print(f"  ✓ Serviço criado: {service['name']}")
        except:
            pass
    
    # 7. Limpar menus desnecessários
    print("\n🧹 Limpando interface...")
    menus_to_hide = [
        'Vendas', 'CRM', 'Website', 'eCommerce', 'Fabricação',
        'Projeto', 'Recursos Humanos', 'Marketing', 'Eventos'
    ]
    
    for menu_name in menus_to_hide:
        try:
            menu_ids = models.execute_kw(db, uid, password,
                'ir.ui.menu', 'search',
                [[['name', '=', menu_name]]])
            
            if menu_ids:
                models.execute_kw(db, uid, password,
                    'ir.ui.menu', 'write',
                    [menu_ids, {'active': False}])
                print(f"  ✓ Menu ocultado: {menu_name}")
        except:
            pass
    
    print("\n✅ Configuração concluída com sucesso!")
    print("\n📝 Informações de acesso:")
    print(f"  URL: http://localhost:8069")
    print(f"  Admin: admin / admin")
    print(f"  Técnico: tecnico / tecnico123")
    print("\n🎉 MobiERP está pronto para uso!")
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("MobiERP - Script de Inicialização")
    print("=" * 60)
    
    if wait_for_odoo():
        time.sleep(10)  # Aguarda um pouco mais para garantir que tudo está pronto
        if setup_mobierp():
            sys.exit(0)
    
    print("❌ Falha na inicialização do MobiERP")
    sys.exit(1)