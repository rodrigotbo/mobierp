#!/bin/bash

# ====================================================================
# MobiERP - Script de Inicialização Rápida
# ====================================================================

echo "==============================================="
echo "       MobiERP - Sistema de Gestão"
echo "    Assistência Técnica de Celulares"
echo "==============================================="
echo ""

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado!"
    echo "Por favor, instale o Docker Desktop primeiro:"
    echo "👉 https://www.docker.com/products/docker-desktop/"
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose não está instalado!"
    echo "Por favor, instale o Docker Compose."
    exit 1
fi

echo "✓ Docker encontrado!"
echo ""

# Função para usar docker-compose ou docker compose
docker_compose_cmd() {
    if command -v docker-compose &> /dev/null; then
        docker-compose "$@"
    else
        docker compose "$@"
    fi
}

# Opções do menu
echo "O que você deseja fazer?"
echo ""
echo "1) 🚀 Iniciar MobiERP (primeira vez)"
echo "2) ▶️  Iniciar MobiERP (já configurado)"
echo "3) ⏸️  Parar MobiERP"
echo "4) 🔄 Reiniciar MobiERP"
echo "5) 🧹 Limpar tudo (reset completo)"
echo "6) 📊 Ver logs"
echo "7) ❌ Sair"
echo ""
read -p "Escolha uma opção [1-7]: " choice

case $choice in
    1)
        echo ""
        echo "🚀 Iniciando MobiERP pela primeira vez..."
        echo "Isso pode demorar alguns minutos na primeira execução."
        echo ""
        
        # Parar e remover containers antigos se existirem
        docker_compose_cmd down -v 2>/dev/null
        
        # Construir e iniciar
        docker_compose_cmd build --no-cache
        docker_compose_cmd up -d
        
        echo ""
        echo "⏳ Aguardando serviços iniciarem..."
        sleep 30
        
        # Executar script de configuração
        docker exec mobierp-odoo python3 /opt/scripts/init_mobierp.py
        
        echo ""
        echo "✅ MobiERP está pronto!"
        echo ""
        echo "📝 Acesse o sistema:"
        echo "   URL: http://localhost:8069"
        echo "   👤 Admin: admin / admin"
        echo "   👷 Técnico: tecnico / tecnico123"
        echo ""
        echo "💡 Dica: Use Ctrl+C para parar quando quiser"
        ;;
        
    2)
        echo ""
        echo "▶️ Iniciando MobiERP..."
        docker_compose_cmd up -d
        echo ""
        echo "✅ MobiERP está rodando!"
        echo "   URL: http://localhost:8069"
        ;;
        
    3)
        echo ""
        echo "⏸️ Parando MobiERP..."
        docker_compose_cmd stop
        echo "✅ MobiERP parado!"
        ;;
        
    4)
        echo ""
        echo "🔄 Reiniciando MobiERP..."
        docker_compose_cmd restart
        echo "✅ MobiERP reiniciado!"
        echo "   URL: http://localhost:8069"
        ;;
        
    5)
        echo ""
        echo "⚠️  ATENÇÃO: Isso vai apagar todos os dados!"
        read -p "Tem certeza? (s/N): " confirm
        if [[ $confirm == [sS] ]]; then
            echo "🧹 Limpando tudo..."
            docker_compose_cmd down -v
            docker system prune -af
            echo "✅ Limpeza completa!"
        else
            echo "Operação cancelada."
        fi
        ;;
        
    6)
        echo ""
        echo "📊 Mostrando logs (Ctrl+C para sair)..."
        echo ""
        docker_compose_cmd logs -f
        ;;
        
    7)
        echo "Até logo! 👋"
        exit 0
        ;;
        
    *)
        echo "❌ Opção inválida!"
        exit 1
        ;;
esac