#!/bin/bash

echo "======================================="
echo "   MobiERP - Diagnóstico do Sistema"
echo "======================================="
echo ""

# Função para usar docker-compose ou docker compose
docker_compose_cmd() {
    if command -v docker-compose &> /dev/null; then
        docker-compose "$@"
    else
        docker compose "$@"
    fi
}

echo "1. Verificando logs do Odoo..."
echo "----------------------------------------"
docker logs --tail 50 mobierp-odoo 2>&1 | head -100
echo ""

echo "2. Verificando status dos containers..."
echo "----------------------------------------"
docker ps -a | grep mobierp
echo ""

echo "3. Verificando conexão com banco de dados..."
echo "----------------------------------------"
docker exec mobierp-db psql -U odoo -d postgres -c "SELECT version();" 2>&1
echo ""

echo "4. Verificando rede Docker..."
echo "----------------------------------------"
docker network inspect mobierp_mobierp-network --format '{{json .Containers}}' | python3 -m json.tool 2>/dev/null || echo "Rede OK"
echo ""

echo "5. Verificando arquivos montados..."
echo "----------------------------------------"
docker exec mobierp-odoo ls -la /mnt/extra-addons/ 2>&1 || echo "Container não está rodando"
echo ""

echo "6. Últimas linhas de erro do Odoo..."
echo "----------------------------------------"
docker logs mobierp-odoo 2>&1 | grep -i "error\|critical\|fatal\|failed" | tail -20
echo ""

echo "======================================="
echo "Diagnóstico concluído!"
echo ""
echo "Possíveis soluções:"
echo "1. Se há erro de conexão com DB: aguarde mais tempo"
echo "2. Se há erro de permissão: verificar volumes"
echo "3. Se há erro de módulo: verificar addons"
echo "======================================="