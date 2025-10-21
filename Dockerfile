# MobiERP - Docker Image
FROM odoo:17.0

USER root

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-dev \
    build-essential \
    postgresql-client \
    curl \
    wkhtmltopdf \
    fonts-liberation \
    locales \
    && rm -rf /var/lib/apt/lists/*

# Configurar locale para pt_BR
RUN echo "pt_BR.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=pt_BR.UTF-8

ENV LANG=pt_BR.UTF-8
ENV LANGUAGE=pt_BR:pt
ENV LC_ALL=pt_BR.UTF-8

# Criar diretórios necessários com permissões corretas
RUN mkdir -p /mnt/extra-addons \
    && mkdir -p /var/lib/odoo \
    && mkdir -p /etc/odoo \
    && mkdir -p /opt/scripts \
    && chown -R odoo:odoo /mnt/extra-addons \
    && chown -R odoo:odoo /var/lib/odoo \
    && chown -R odoo:odoo /etc/odoo \
    && chown -R odoo:odoo /opt/scripts

# Copiar e instalar requirements Python (se houver necessidade de libs extras)
COPY --chown=odoo:odoo requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir --break-system-packages \
    num2words==0.5.13 \
    && rm /tmp/requirements.txt

# Copiar configuração (será sobrescrito pelo volume se existir)
COPY --chown=odoo:odoo ./config/odoo.conf /etc/odoo/odoo.conf

# Copiar addons e scripts com permissões corretas
COPY --chown=odoo:odoo ./addons /mnt/extra-addons
COPY --chown=odoo:odoo ./scripts /opt/scripts
RUN chmod +x /opt/scripts/*.py

USER odoo

# Expor porta padrão do Odoo
EXPOSE 8069 8072

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:8069/web/database/selector || exit 1

# Comando padrão
CMD ["odoo", "-c", "/etc/odoo/odoo.conf"]