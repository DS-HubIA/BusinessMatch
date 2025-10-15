#!/bin/bash
echo "Atualizando status..."
cp status_continuacao.json status_backup.json

# Substituir data
sed -i '' 's/"data_backup": "[^"]*"/"data_backup": "'$(date -Iseconds)'"/' status_continuacao.json

echo "✅ Status atualizado com nova data"
echo "Edite manualmente os arrays de problemas e funcionalidades"
