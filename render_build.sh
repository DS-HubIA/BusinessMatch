#!/bin/bash
echo "=== Business Match SEBRAE - Build Script ==="

# Instalar dependências
pip install -r requirements.txt

# Configurar database se necessário
# flask db upgrade

echo "=== Build completo! ==="
