with open('app/templates/opportunities.html', 'r') as f:
    content = f.read()

old_card = '''card.innerHTML = `
            <div class="card-header">
                ${opportunity.business_type || 'Oportunidade'}
            </div>
            <div class="card-content">
                <h2 class="business-name">${opportunity.business_name}</h2>
                <p class="business-description">${opportunity.description}</p>
            </div>
        `;'''

new_card = '''card.innerHTML = `
            <div class="card-header">
                ${opportunity.business_type || 'Oportunidade'}
            </div>
            <div class="card-content">
                <h2 class="business-name">${opportunity.business_name}</h2>
                <p class="business-description">${opportunity.description}</p>
                <div class="card-details">
                    <div class="detail-item">
                        <span class="detail-label">Empresa:</span>
                        <span class="detail-value">${opportunity.user_company}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Contato:</span>
                        <span class="detail-value">${opportunity.user_name}</span>
                    </div>
                </div>
            </div>
        `;'''

content = content.replace(old_card, new_card)

with open('app/templates/opportunities.html', 'w') as f:
    f.write(content)

print("Cards melhorados")
