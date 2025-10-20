# MobiERP - Sistema de Gestão para Assistência Técnica de Celulares

Sistema ERP completo baseado no Odoo Community Edition, desenvolvido especificamente para lojas de conserto de celulares, venda de peças e acessórios.

## 📱 Sobre o Sistema

MobiERP é uma solução completa de gestão empresarial que integra:
- Controle de ordens de serviço e assistência técnica
- Gestão de estoque de peças e acessórios
- Vendas de balcão (PDV)
- Controle financeiro
- Relacionamento com clientes
- Relatórios gerenciais

## 🚀 Requisitos

- Odoo Community 17.0+
- Python 3.10+
- PostgreSQL 13+
- wkhtmltopdf (para geração de PDFs)

## 📦 Módulos Inclusos

### Módulos Principais
- **repair_service**: Gestão de ordens de serviço e assistência técnica
- **mobile_parts**: Controle de peças e acessórios
- **store_dashboard**: Painel de controle customizado
- **communication**: Integração com WhatsApp (opcional)

### Módulos Odoo Utilizados
- sales
- stock
- purchase
- account
- contacts
- point_of_sale

## 🛠️ Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/rodrigotbo/mobierp.git
cd mobierp
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure o Odoo
```bash
# Copie os módulos para o diretório de addons do Odoo
cp -r addons/* /path/to/odoo/addons/

# Ou adicione o caminho no arquivo de configuração do Odoo
# addons_path = /path/to/mobierp/addons,/path/to/odoo/addons
```

### 4. Atualize a lista de aplicações
- Acesse o Odoo
- Vá em Apps > Update Apps List
- Procure por "MobiERP" e instale os módulos

## 🎨 Funcionalidades

### Ordem de Serviço
- Cadastro completo de OS com cliente, equipamento e problema
- Controle de status (análise, reparo, concluído, entregue)
- Histórico por cliente e aparelho
- Impressão de comprovantes
- Controle de garantia

### Estoque
- Controle de peças e acessórios
- Alertas de estoque mínimo
- Rastreabilidade de uso em reparos
- Localização física

### Vendas
- PDV simplificado
- Emissão de recibos
- Controle por vendedor
- Relatórios de vendas

### Financeiro
- Contas a pagar e receber
- Controle de caixa
- Múltiplas formas de pagamento
- Relatórios de lucro

### Comunicação
- Notificações via WhatsApp
- Templates personalizados
- Avisos automáticos de status

## 📊 Relatórios

- Dashboard com métricas principais
- Serviços em andamento
- Vendas diárias
- Produtos com estoque baixo
- Análise de rentabilidade

## 🔐 Licença

Este projeto é baseado no Odoo Community Edition e segue a licença LGPL v3.
Módulos customizados podem ter licenças proprietárias.

## 👥 Suporte

Para suporte e questões comerciais:
- Email: contato@mobierp.com.br
- WhatsApp: (11) 99999-9999

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, leia o arquivo CONTRIBUTING.md para detalhes sobre nosso código de conduta e processo de submissão de pull requests.

## 📝 Changelog

### v1.0.0 (2025-01-20)
- Lançamento inicial
- Módulos básicos de OS, estoque e vendas
- Dashboard customizado
- Tradução pt_BR

---

Desenvolvido com ❤️ para o mercado de assistência técnica brasileiro