with open('app/templates/opportunities.html', 'r') as f:
    content = f.read()

# Manter apenas o JavaScript essencial
import re

# Encontrar o script principal
script_match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
if script_match:
    old_script = script_match.group(1)
    
    # Script limpo e funcional
    new_script = '''
    let currentOpportunities = [];
    let currentCardIndex = 0;

    async function loadOpportunities() {
        try {
            console.log("Carregando oportunidades...");
            const response = await fetch('/api/opportunities');
            console.log("Status:", response.status);
            
            currentOpportunities = await response.json();
            console.log("Dados recebidos:", currentOpportunities);
            
            currentCardIndex = 0;
            renderCards();
        } catch (error) {
            console.error("Erro:", error);
        }
    }

    function renderCards() {
        const container = document.getElementById('cardsContainer');
        container.innerHTML = '';

        if (currentOpportunities.length === 0) {
            container.innerHTML = '<div class="no-opportunities">Nenhuma oportunidade</div>';
            return;
        }

        for (let i = 0; i < Math.min(3, currentOpportunities.length - currentCardIndex); i++) {
            const opportunity = currentOpportunities[currentCardIndex + i];
            const card = createOpportunityCard(opportunity, i);
            container.appendChild(card);
        }
    }

    function createOpportunityCard(opportunity, zIndex) {
        const card = document.createElement('div');
        card.className = 'opportunity-card';
        card.style.zIndex = 100 - zIndex;
        
        card.innerHTML = `
            <div class="card-header">
                ${opportunity.business_type || 'Oportunidade'}
            </div>
            <div class="card-content">
                <h2 class="business-name">${opportunity.business_name}</h2>
                <p class="business-description">${opportunity.description}</p>
            </div>
        `;

        return card;
    }

    async function handleSwipe(action) {
        if (currentCardIndex >= currentOpportunities.length) {
            await loadOpportunities();
            return;
        }

        const currentOpportunity = currentOpportunities[currentCardIndex];
        const card = document.querySelector('.opportunity-card');

        card.classList.add(action === 'like' ? 'swipe-right' : 'swipe-left');

        try {
            await fetch('/api/swipe', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    opportunity_id: currentOpportunity.id,
                    action: action
                })
            });
        } catch (error) {
            console.error("Erro no swipe:", error);
        }

        setTimeout(() => {
            currentCardIndex++;
            renderCards();
        }, 300);
    }

    // Inicializar
    document.addEventListener('DOMContentLoaded', loadOpportunities);
    '''
    
    content = content.replace(old_script, new_script)

with open('app/templates/opportunities.html', 'w') as f:
    f.write(content)

print("✅ JavaScript limpo e funcional instalado")
