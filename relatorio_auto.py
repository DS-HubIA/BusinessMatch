import json
from datetime import datetime
import os
os.makedirs('status', exist_ok=True)

with open('status/status_continuacao.json', 'r') as f:
    s = json.load(f)
    
with open('status/RELATORIO_ATUAL.md', 'w') as f:
    f.write(f"# BUSINESS MATCH - {datetime.now().strftime('%H:%M')}\\n")
    f.write(f"**Backend:** {s['status_geral']['backend']}\\n")
    f.write(f"**Frontend:** {s['status_geral']['frontend']}\\n\\n")
    f.write("## 🔴 PROBLEMAS:\\n")
    for p in s['problemas_atuais']:
        f.write(f"- {p}\\n")
    f.write("\\n## 🎯 PRÓXIMOS: CSS → Admin → Produtos → Deploy\\n")
print("✅ RELATORIO_ATUAL.md gerado em status/")
