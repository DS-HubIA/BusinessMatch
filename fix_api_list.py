with open('app/routes/business.py', 'r') as f:
    content = f.read()

# Encontrar a parte problemática (retorna apenas o primeiro item)
import re

# Substituir o bloco que retorna apenas um item por um que retorna lista
old_pattern = r'if opportunities:\s*opp = opportunities\[0\].*?return jsonify\(opportunity_data\)'
new_code = '''if opportunities:
            opportunity_list = []
            for opp in opportunities:
                business = Business.query.get(opp.business_id)
                user = User.query.get(opp.user_id)
                
                opportunity_data = {
                    'id': opp.id,
                    'title': opp.title,
                    'description': opp.description,
                    'business_name': business.name if business else 'Negócio',
                    'business_type': business.business_sector if business else '',
                    'user_name': user.name if user else 'Usuário',
                    'user_phone': user.phone if user else '',
                    'user_company': user.company if user else '',
                    'user_id': user.id if user else None
                }
                opportunity_list.append(opportunity_data)
            
            return jsonify(opportunity_list)'''

content = re.sub(old_pattern, new_code, content, flags=re.DOTALL)

with open('app/routes/business.py', 'w') as f:
    f.write(content)

print("✅ API corrigida para retornar lista completa")
