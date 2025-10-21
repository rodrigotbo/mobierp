#!/bin/bash

echo "======================================="
echo "   MobiERP - Correção e Reset"
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

echo "1. Parando containers..."
docker_compose_cmd down

echo ""
echo "2. Removendo volumes antigos..."
docker volume rm mobierp_mobierp-odoo-data mobierp_mobierp-odoo-filestore 2>/dev/null

echo ""
echo "3. Reconstruindo imagem Docker..."
docker_compose_cmd build --no-cache

echo ""
echo "4. Iniciando banco de dados..."
docker_compose_cmd up -d db

echo ""
echo "5. Aguardando banco estar pronto..."
sleep 10

echo ""
echo "6. Iniciando Odoo..."
docker_compose_cmd up -d odoo

echo ""
echo "7. Aguardando Odoo iniciar (60 segundos)..."
sleep 60

echo ""
echo "8. Verificando status..."
docker ps | grep mobierp

echo ""
echo "9. Verificando logs..."
docker logs --tail 20 mobierp-odoo

echo ""
echo "======================================="
echo "Correção aplicada!"
echo ""
echo "Tente acessar: http://localhost:8069"
echo ""
echo "Se ainda houver problemas, execute:"
echo "  ./diagnose.sh"
echo ""
echo "Para ver logs em tempo real:"
echo "  docker logs -f mobierp-odoo"
echo "======================================="