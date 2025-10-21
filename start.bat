@echo off
REM ====================================================================
REM MobiERP - Script de Inicialização Rápida (Windows)
REM ====================================================================

cls
echo ===============================================
echo        MobiERP - Sistema de Gestao
echo     Assistencia Tecnica de Celulares
echo ===============================================
echo.

REM Verificar se Docker está instalado
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Docker nao esta instalado!
    echo Por favor, instale o Docker Desktop primeiro:
    echo https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

echo [OK] Docker encontrado!
echo.

echo O que voce deseja fazer?
echo.
echo 1) Iniciar MobiERP (primeira vez)
echo 2) Iniciar MobiERP (ja configurado)
echo 3) Parar MobiERP
echo 4) Reiniciar MobiERP
echo 5) Limpar tudo (reset completo)
echo 6) Ver logs
echo 7) Sair
echo.

set /p choice="Escolha uma opcao [1-7]: "

if "%choice%"=="1" goto first_start
if "%choice%"=="2" goto start
if "%choice%"=="3" goto stop
if "%choice%"=="4" goto restart
if "%choice%"=="5" goto clean
if "%choice%"=="6" goto logs
if "%choice%"=="7" goto exit

echo [ERRO] Opcao invalida!
pause
exit /b 1

:first_start
echo.
echo Iniciando MobiERP pela primeira vez...
echo Isso pode demorar alguns minutos na primeira execucao.
echo.

REM Parar e remover containers antigos se existirem
docker-compose down -v 2>nul

REM Construir e iniciar
docker-compose build --no-cache
docker-compose up -d

echo.
echo Aguardando servicos iniciarem (30 segundos)...
timeout /t 30 /nobreak >nul

REM Executar script de configuração
docker exec mobierp-odoo python3 /opt/scripts/init_mobierp.py

echo.
echo ===============================================
echo MobiERP esta pronto!
echo.
echo Acesse o sistema:
echo   URL: http://localhost:8069
echo   Admin: admin / admin
echo   Tecnico: tecnico / tecnico123
echo ===============================================
echo.
pause
goto end

:start
echo.
echo Iniciando MobiERP...
docker-compose up -d
echo.
echo MobiERP esta rodando!
echo URL: http://localhost:8069
echo.
pause
goto end

:stop
echo.
echo Parando MobiERP...
docker-compose stop
echo MobiERP parado!
echo.
pause
goto end

:restart
echo.
echo Reiniciando MobiERP...
docker-compose restart
echo MobiERP reiniciado!
echo URL: http://localhost:8069
echo.
pause
goto end

:clean
echo.
echo ATENCAO: Isso vai apagar todos os dados!
set /p confirm="Tem certeza? (s/N): "
if /i "%confirm%"=="s" (
    echo Limpando tudo...
    docker-compose down -v
    docker system prune -af
    echo Limpeza completa!
) else (
    echo Operacao cancelada.
)
echo.
pause
goto end

:logs
echo.
echo Mostrando logs (Ctrl+C para sair)...
echo.
docker-compose logs -f
goto end

:exit
echo Ate logo!
exit /b 0

:end