// Business Match - Sistema de Swipe
class SwipeManager {
    constructor() {
        this.currentOpportunityIndex = 0;
        this.opportunities = [];
        this.init();
    }

    async init() {
        await this.loadOpportunities();
        this.renderCurrentOpportunity();
        this.setupEventListeners();
    }

    async loadOpportunities() {
        try {
            const response = await fetch('/api/opportunities');
            this.opportunities = await response.json();
            console.log('Oportunidades carregadas:', this.opportunities);
        } catch (error) {
            console.error('Erro ao carregar oportunidades:', error);
        }
    }

    renderCurrentOpportunity() {
        const container = document.getElementById('swipe-container');
        
        if (!container) {
            console.error('Container de swipe não encontrado!');
            return;
        }

        if (this.opportunities.length === 0) {
            container.innerHTML = `
                <div class="card">
                    <div class="card-body text-center py-5">
                        <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
                        <h4>Nenhuma oportunidade disponível</h4>
                        <p class="text-muted">Volte mais tarde para novas conexões</p>
                    </div>
                </div>
            `;
            this.hideSwipeButtons();
            return;
        }

        const opp = this.opportunities[this.currentOpportunityIndex];
        const badgeClass = opp.type === 'OFERTA' ? 'bg-success' : 'bg-warning';
        
        container.innerHTML = `
            <div class="card business-card" id="current-card">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <span class="badge ${badgeClass}">${opp.type}</span>
                    <small class="text-muted">${opp.category}</small>
                </div>
                <div class="card-body">
                    <h5 class="card-title">${opp.title}</h5>
                    <p class="card-text">${opp.description}</p>
                    <div class="tags mt-3">
                        <span class="badge bg-secondary">${opp.category}</span>
                    </div>
                </div>
                <div class="card-footer">
                    <div class="text-center">
                        <button class="btn btn-danger btn-lg me-3" id="dislikeBtn">
                            <i class="fas fa-times"></i>
                        </button>
                        <button class="btn btn-success btn-lg" id="likeBtn">
                            <i class="fas fa-heart"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;

        this.showSwipeButtons();
    }

    setupEventListeners() {
        // Os event listeners serão adicionados após cada render
        setTimeout(() => {
            const likeBtn = document.getElementById('likeBtn');
            const dislikeBtn = document.getElementById('dislikeBtn');
            
            if (likeBtn) {
                likeBtn.addEventListener('click', () => this.handleSwipe('like'));
            }
            if (dislikeBtn) {
                dislikeBtn.addEventListener('click', () => this.handleSwipe('dislike'));
            }
        }, 100);
    }

    async handleSwipe(action) {
        const currentOpp = this.opportunities[this.currentOpportunityIndex];
        
        if (!currentOpp) return;

        try {
            const response = await fetch(`/swipe/${currentOpp.id}/${action}`);
            const result = await response.json();
            
            this.showFeedback(result.message, action);
            
            // Próxima oportunidade após breve delay
            setTimeout(() => {
                this.nextOpportunity();
            }, 1000);
            
        } catch (error) {
            console.error('Erro ao processar swipe:', error);
            this.showFeedback('Erro ao processar. Tente novamente.', 'error');
        }
    }

    showFeedback(message, action) {
        // Feedback visual simples
        const feedback = document.createElement('div');
        feedback.className = `alert alert-${action === 'like' ? 'success' : 'info'} alert-dismissible fade show position-fixed`;
        feedback.style.cssText = 'top: 20px; right: 20px; z-index: 1000; min-width: 300px;';
        feedback.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(feedback);
        
        // Auto-remove após 3 segundos
        setTimeout(() => {
            if (feedback.parentNode) {
                feedback.remove();
            }
        }, 3000);
    }

    nextOpportunity() {
        this.currentOpportunityIndex++;
        
        if (this.currentOpportunityIndex >= this.opportunities.length) {
            this.currentOpportunityIndex = 0; // Voltar ao início
        }
        
        this.renderCurrentOpportunity();
    }

    hideSwipeButtons() {
        const buttonsContainer = document.querySelector('.card-footer');
        if (buttonsContainer) {
            buttonsContainer.style.display = 'none';
        }
    }

    showSwipeButtons() {
        const buttonsContainer = document.querySelector('.card-footer');
        if (buttonsContainer) {
            buttonsContainer.style.display = 'block';
        }
    }
}

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    console.log('Inicializando Business Match Swipe...');
    window.swipeManager = new SwipeManager();
});
