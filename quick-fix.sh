#!/bin/bash

echo "======================================="
echo "   MobiERP - Correção Rápida"
echo "======================================="
echo ""

# Parar containers antigos
echo "1. Parando containers..."
docker stop mobierp-odoo mobierp-db 2>/dev/null
docker rm mobierp-odoo mobierp-db 2>/dev/null

echo ""
echo "2. Limpando volumes antigos..."
docker volume rm mobierp_mobierp-odoo-data mobierp_mobierp-odoo-filestore mobierp_mobierp-db-data 2>/dev/null

echo ""
echo "3. Usando configuração simplificada..."
echo ""

# Usar docker-compose ou docker compose
if command -v docker-compose &> /dev/null; then
    DC_CMD="docker-compose"
else
    DC_CMD="docker compose"
fi

echo "4. Iniciando com docker-compose.simple.yml..."
$DC_CMD -f docker-compose.simple.yml up -d

echo ""
echo "5. Aguardando serviços iniciarem (30 segundos)..."
sleep 30

echo ""
echo "6. Verificando status..."
docker ps | grep mobierp

echo ""
echo "======================================="
echo "Sistema iniciado com configuração simplificada!"
echo ""
echo "Acesse: http://localhost:8069"
echo ""
echo "Para criar o banco de dados na primeira vez:"
echo "1. Acesse http://localhost:8069"
echo "2. Master Password: admin123"
echo "3. Database: mobierp"
echo "4. Email: admin@mobierp.com"
echo "5. Password: admin"
echo "6. Language: Portuguese (BR)"
echo "7. Country: Brazil"
echo ""
echo "Depois instale os módulos:"
echo "- Apps > Update Apps List"
echo "- Procure: repair_service"
echo "- Instale o módulo"
echo "======================================="