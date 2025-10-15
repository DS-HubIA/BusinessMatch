with open('app/routes/business.py', 'r') as f:
    content = f.read()

# Corrigir o subquery para selecionar apenas opportunity_id
old_query = "seen_opportunities = db.session.query(Interest.opportunity_id).filter("
new_query = "seen_opportunities = db.session.query(Interest.opportunity_id).filter("

# Garantir que está correto
if old_query in content:
    print("Query já está correta")
else:
    # Encontrar e corrigir a query problemática
    import re
    content = re.sub(
        r'seen_opportunities = db\.session\.query\(Interest\)\.filter\(.*?\)',
        "seen_opportunities = db.session.query(Interest.opportunity_id).filter(Interest.user_id == current_user.id)",
        content
    )

with open('app/routes/business.py', 'w') as f:
    f.write(content)

print("✅ Query da API corrigida")
