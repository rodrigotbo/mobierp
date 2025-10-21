# 📦 Guia de Instalação MobiERP

Este guia vai te ajudar a instalar e rodar o MobiERP no seu computador usando Docker.

## 🚀 Instalação Rápida (Recomendado)

### Pré-requisitos

#### 1️⃣ Instalar o Docker Desktop

**Windows / Mac:**
1. Acesse: https://www.docker.com/products/docker-desktop/
2. Clique em "Download for Windows" ou "Download for Mac"
3. Execute o instalador baixado
4. Siga as instruções na tela (pode deixar tudo padrão)
5. Reinicie o computador se solicitado
6. Abra o Docker Desktop e aguarde inicializar (ícone da baleia na bandeja)

**Linux (Ubuntu/Debian):**
```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo apt-get update
sudo apt-get install docker-compose-plugin
```

#### 2️⃣ Instalar o Git

**Windows:**
1. Acesse: https://git-scm.com/download/win
2. Baixe e execute o instalador
3. Durante instalação, pode deixar todas opções padrão

**Mac:**
```bash
# Se tiver Homebrew instalado:
brew install git

# Ou baixe de: https://git-scm.com/download/mac
```

**Linux:**
```bash
sudo apt-get install git
```

### 🎯 Instalação do MobiERP

#### Passo 1: Baixar o MobiERP

Abra o Terminal (Mac/Linux) ou Command Prompt/PowerShell (Windows) e execute:

```bash
# Navegue para onde quer salvar (exemplo: pasta Documentos)
cd ~/Documents  # Mac/Linux
cd C:\Users\SeuNome\Documents  # Windows

# Clone o repositório
git clone https://github.com/rodrigotbo/mobierp.git

# Entre na pasta do projeto
cd mobierp
```

#### Passo 2: Iniciar o MobiERP

**🪟 Windows:**
```bash
# Dê duplo clique no arquivo:
start.bat

# Ou execute no PowerShell/CMD:
.\start.bat
```

**🐧 Linux / 🍎 Mac:**
```bash
# Torne o script executável
chmod +x start.sh

# Execute
./start.sh
```

#### Passo 3: Primeira Execução

1. Quando abrir o menu, escolha a opção **1** (Iniciar MobiERP - primeira vez)
2. Aguarde o download das imagens e configuração (5-10 minutos na primeira vez)
3. O sistema será configurado automaticamente
4. Quando terminar, você verá as credenciais de acesso

### 🌐 Acessar o Sistema

Após a instalação, abra seu navegador e acesse:

**URL:** http://localhost:8069

**Credenciais padrão:**
- 👤 **Admin:** admin / admin
- 👷 **Técnico:** tecnico / tecnico123

---

## 🎮 Usando o Sistema

### Menu de Controle

Execute `start.bat` (Windows) ou `./start.sh` (Linux/Mac) para ver o menu:

- **Opção 1:** Primeira instalação (use apenas uma vez)
- **Opção 2:** Iniciar o sistema (uso diário)
- **Opção 3:** Parar o sistema
- **Opção 4:** Reiniciar o sistema
- **Opção 5:** Reset completo (⚠️ apaga todos os dados)
- **Opção 6:** Ver logs do sistema
- **Opção 7:** Sair

### Comandos Manuais (Avançado)

```bash
# Iniciar o sistema
docker-compose up -d

# Parar o sistema
docker-compose stop

# Ver logs
docker-compose logs -f

# Resetar tudo
docker-compose down -v
```

---

## 🔧 Solução de Problemas

### Docker não está instalado
- **Solução:** Instale o Docker Desktop seguindo o passo 1

### Porta 8069 já está em uso
- **Solução:** Edite `docker-compose.yml` e mude `8069:8069` para `8070:8069`
- Depois acesse http://localhost:8070

### Sistema muito lento
- **Windows/Mac:** Abra Docker Desktop → Settings → Resources
- Aumente Memory para pelo menos 4GB
- Aumente CPUs para pelo menos 2

### Erro de permissão (Linux)
```bash
# Adicione seu usuário ao grupo docker
sudo usermod -aG docker $USER
# Faça logout e login novamente
```

### Reset completo
Se algo der muito errado:
```bash
# Para e remove tudo
docker-compose down -v
docker system prune -af

# Começar do zero
./start.sh  # Escolha opção 1
```

---

## 📱 Funcionalidades Principais

### Módulo de Assistência Técnica
- ✅ Ordens de serviço completas
- ✅ Controle de status (recebido, em reparo, concluído)
- ✅ Gestão de garantia
- ✅ Histórico por cliente
- ✅ Impressão de comprovantes

### Módulo de Peças e Acessórios
- ✅ Controle de estoque
- ✅ Alertas de estoque mínimo
- ✅ Compatibilidade com modelos
- ✅ Categorização de peças

### Interface Limpa
- ✅ Apenas módulos necessários
- ✅ Menu simplificado
- ✅ Em português brasileiro
- ✅ Dashboard focado

---

## 🆘 Suporte

**Problemas ou dúvidas?**

1. Verifique a seção de Solução de Problemas acima
2. Abra uma issue em: https://github.com/rodrigotbo/mobierp/issues
3. Entre em contato: contato@mobierp.com.br

---

## 🎉 Pronto!

Seu MobiERP está instalado e configurado. Aproveite o sistema!

**Dicas finais:**
- Faça backup regular dos seus dados
- Mantenha o Docker Desktop atualizado
- Para parar o sistema: use a opção 3 do menu
- Para iniciar novamente: use a opção 2 do menu

Bom trabalho! 🚀