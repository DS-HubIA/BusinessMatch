with open('app/templates/opportunities.html', 'r') as f:
    content = f.read()

# Encontrar e corrigir o problema de escape
import re

# Encontrar a linha com erro de escape
problem_line = re.search(r".*\\\\.*", content)
if problem_line:
    print(f"Linha problemática encontrada: {problem_line.group()}")
    
    # Substituir escapes problemáticos
    content = content.replace('\\\\', '\\')

with open('app/templates/opportunities.html', 'w') as f:
    f.write(content)

print("✅ Erro de syntax corrigido")

# Verificar se ainda há problemas
print("Verificando problemas restantes...")
python -c "
with open('app/templates/opportunities.html', 'r') as f:
    content = f.read()
    lines = content.split('\\n')
    for i, line in enumerate(lines, 1):
        if '\\\\\\\\' in line:
            print(f'Linha {i}: Possível problema - {line[:50]}...')
"

