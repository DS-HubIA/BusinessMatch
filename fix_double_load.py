with open('app/templates/opportunities.html', 'r') as f:
    content = f.read()

# Remover uma das chamadas duplicadas
content = content.replace(
    'document.addEventListener(\'DOMContentLoaded\', loadOpportunities);',
    '// document.addEventListener(\'DOMContentLoaded\', loadOpportunities);'
)

with open('app/templates/opportunities.html', 'w') as f:
    f.write(content)

print("✅ Duplo carregamento corrigido")
