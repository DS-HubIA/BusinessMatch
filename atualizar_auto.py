import json
from datetime import datetime
import os
os.makedirs('status', exist_ok=True)

with open('status/status_continuacao.json', 'r') as f:
    data = json.load(f)
data['data_backup'] = datetime.now().isoformat()
with open('status/status_continuacao.json', 'w') as f:
    json.dump(data, f, indent=2)
print("✅ Status atualizado em status/")
