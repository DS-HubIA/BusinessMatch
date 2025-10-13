// Sistema de Swipe para oportunidades
class SwipeManager {
    constructor() {
        this.currentCardIndex = 0;
        this.opportunities = [];
        this.init();
    }

    async init() {
        await this.loadOpportunities();
        this.renderCurrentCard();
        this.setupSwipeListeners();
    }

    async loadOpportunities() {
        try {
            const response = await fetch('/api/opportunities');
            this.opportunities = await response.json();
        } catch (error) {
            console.error('Erro ao carregar oportunidades:', error);
        }
    }

    renderCurrentCard() {
        const container = document.getElementById('swipe-container');
        if (!container || this.opportunities.length === 0) {
            container.innerHTML = '<div class="text-center py-5"><h4>Nenhuma oportunidade disponível</h4></div>';
            return;
        }

        const opp = this.opportunities[this.currentCardIndex];
        container.innerHTML = `
            <div class="card business-card" id="current-card">
                <div class="card-header">
                    <span class="badge bg-${opp.type === 'OFERTA' ? 'success' : 'warning'}">${opp.type}</span>
                    <small class="text-muted">${opp.category}</small>
                </div>
                <div class="card-body">
                    <h5 class="card-title">${opp.title}</h5>
                    <p class="card-text">${opp.description}</p>
                </div>
                <div class="card-footer">
                    <div class="text-center">
                        <button class="btn btn-danger btn-lg me-3" onclick="swipeManager.handleSwipe('dislike', ${opp.id})">✕</button>
                        <button class="btn btn-success btn-lg" onclick="swipeManager.handleSwipe('like', ${opp.id})">✓</button>
                    </div>
                </div>
            </div>
        `;
    }

    async handleSwipe(action, businessId) {
        try {
            const response = await fetch(`/swipe/${businessId}/${action}`);
            const result = await response.json();
            
            if (result.status === 'success') {
                this.showFeedback(result.message, result.match);
                this.nextCard();
            }
        } catch (error) {
            console.error('Erro ao processar swipe:', error);
        }
    }

    showFeedback(message, isMatch) {
        // Feedback visual simples
        alert(message);
    }

    nextCard() {
        this.currentCardIndex++;
        if (this.currentCardIndex >= this.opportunities.length) {
            this.currentCardIndex = 0; // Voltar ao início
        }
        this.renderCurrentCard();
    }

    setupSwipeListeners() {
        // Implementar swipe com touch/mouse depois
    }
}

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    window.swipeManager = new SwipeManager();
});
