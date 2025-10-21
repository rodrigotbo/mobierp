# MobiERP - Docker Image
FROM odoo:17.0

USER root

# Instalar dependências adicionais
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    npm \
    nodejs \
    wkhtmltopdf \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements customizados
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Criar diretórios necessários
RUN mkdir -p /mnt/extra-addons \
    && mkdir -p /var/lib/odoo \
    && mkdir -p /etc/odoo \
    && mkdir -p /opt/scripts

# Copiar arquivos de configuração
COPY ./config/odoo.conf /etc/odoo/odoo.conf
COPY ./addons /mnt/extra-addons
COPY ./scripts /opt/scripts

# Dar permissões corretas
RUN chown -R odoo:odoo /mnt/extra-addons \
    && chown -R odoo:odoo /var/lib/odoo \
    && chown -R odoo:odoo /etc/odoo \
    && chmod -R 755 /opt/scripts

# Configurar locale para pt_BR
RUN apt-get update && apt-get install -y locales \
    && echo "pt_BR.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=pt_BR.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=pt_BR.UTF-8
ENV LANGUAGE=pt_BR:pt
ENV LC_ALL=pt_BR.UTF-8

USER odoo

# Expor porta padrão do Odoo
EXPOSE 8069

# Comando padrão
CMD ["odoo"]