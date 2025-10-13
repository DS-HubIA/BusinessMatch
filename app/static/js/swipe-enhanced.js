// Business Match - Swipe System (Tinder-style)
class SwipeManager {
    constructor() {
        this.currentIndex = 0;
        this.opportunities = [];
        this.isAnimating = false;
        this.init();
    }

    async init() {
        await this.loadOpportunities();
        this.renderCurrentCard();
        this.setupSwipeListeners();
        this.setupKeyboardListeners();
    }

    async loadOpportunities() {
        try {
            const response = await fetch('/api/opportunities');
            this.opportunities = await response.json();
            this.updateCounter();
        } catch (error) {
            this.showError('Erro ao carregar oportunidades');
        }
    }

    renderCurrentCard() {
        const container = document.getElementById('swipe-container');
        
        if (this.opportunities.length === 0) {
            container.innerHTML = this.getEmptyState();
            return;
        }

        const opp = this.opportunities[this.currentIndex];
        container.innerHTML = this.createCardHTML(opp);
        this.updateCounter();
    }

    createCardHTML(opportunity) {
        const badgeClass = opportunity.type === 'OFERTA' ? 'bg-success' : 'bg-warning';
        const icon = opportunity.type === 'OFERTA' ? 'fa-hand-holding' : 'fa-handshake';
        
        return `
            <div class="card business-card" id="current-card">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <span class="badge ${badgeClass}">
                        <i class="fas ${icon} me-1"></i>${opportunity.type}
                    </span>
                    <small class="text-muted">${opportunity.category}</small>
                </div>
                <div class="card-body">
                    <h4 class="card-title">${opportunity.title}</h4>
                    <p class="card-text">${opportunity.description}</p>
                    <div class="tags mt-3">
                        <span class="badge bg-light text-dark border">
                            <i class="fas fa-tag me-1"></i>${opportunity.category}
                        </span>
                    </div>
                </div>
                <div class="card-footer">
                    <div class="text-center">
                        <button class="btn btn-danger btn-lg me-4 swipe-btn" data-action="dislike">
                            <i class="fas fa-times"></i>
                        </button>
                        <button class="btn btn-success btn-lg swipe-btn" data-action="like">
                            <i class="fas fa-heart"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    setupSwipeListeners() {
        document.addEventListener('click', (e) => {
            if (e.target.closest('.swipe-btn') && !this.isAnimating) {
                const action = e.target.closest('.swipe-btn').dataset.action;
                this.handleSwipe(action);
            }
        });
    }

    setupKeyboardListeners() {
        document.addEventListener('keydown', (e) => {
            if (this.isAnimating) return;
            
            if (e.key === 'ArrowLeft') {
                this.handleSwipe('dislike');
            } else if (e.key === 'ArrowRight') {
                this.handleSwipe('like');
            }
        });
    }

    async handleSwipe(action) {
        if (this.isAnimating) return;
        
        this.isAnimating = true;
        const currentOpp = this.opportunities[this.currentIndex];
        const card = document.getElementById('current-card');

        // Animação visual
        card.classList.add(action === 'like' ? 'swipe-right' : 'swipe-left');

        try {
            const response = await fetch(`/swipe/${currentOpp.id}/${action}`);
            const result = await response.json();
            
            this.showFeedback(result.message, action);
            
            setTimeout(() => {
                this.nextCard();
                this.isAnimating = false;
            }, 500);
            
        } catch (error) {
            this.showFeedback('Erro ao processar', 'error');
            this.isAnimating = false;
        }
    }

    nextCard() {
        this.currentIndex++;
        if (this.currentIndex >= this.opportunities.length) {
            this.currentIndex = 0;
        }
        this.renderCurrentCard();
    }

    updateCounter() {
        const counter = document.getElementById('opportunity-counter');
        if (counter && this.opportunities.length > 0) {
            counter.textContent = 
                `${this.currentIndex + 1} de ${this.opportunities.length} oportunidades`;
        }
    }

    showFeedback(message, type) {
        // Implementar toast notification
        console.log(`${type}: ${message}`);
    }

    showError(message) {
        console.error(message);
    }

    getEmptyState() {
        return `
            <div class="card">
                <div class="card-body text-center py-5">
                    <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
                    <h4>Nenhuma oportunidade disponível</h4>
                    <p class="text-muted">Todas as oportunidades foram visualizadas</p>
                    <button class="btn btn-primary mt-3" onclick="location.reload()">
                        <i class="fas fa-redo me-2"></i>Recarregar
                    </button>
                </div>
            </div>
        `;
    }
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    window.swipeManager = new SwipeManager();
});
