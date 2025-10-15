with open('app/templates/opportunities.html', 'r') as f:
    content = f.read()

# Adicionar console.log para debug
debug_code = '''
        console.log("🔄 Carregando oportunidades...");
        console.log("Response status:", response.status);
        console.log("Dados recebidos:", currentOpportunities);
'''

content = content.replace(
    'currentOpportunities = await response.json();',
    'currentOpportunities = await response.json();' + debug_code
)

with open('app/templates/opportunities.html', 'w') as f:
    f.write(content)

print("✅ Debug adicionado ao JavaScript")
