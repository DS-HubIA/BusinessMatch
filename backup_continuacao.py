#!/usr/bin/env python3
"""
BACKUP COMPLETO PARA PRÓXIMO CHAT
Salva status atual e informações críticas
"""
import json
import os
from datetime import datetime

def criar_backup_completo():
    status = {
        "data_backup": datetime.now().isoformat(),
        "projeto": "Business Match SEBRAE",
        
        "status_geral": {
            "backend": "100% funcional",
            "frontend": "70% (precisa ajustes visuais)",
            "banco_dados": "PostgreSQL configurado",
            "deploy": "Render preparado"
        },
        
        "funcionalidades_implementadas": [
            "Sistema completo de autenticação",
            "Cadastro/edição de negócios com CNPJ", 
            "Sistema de swipe com like/dislike",
            "Matching automático (interesse mútuo)",
            "Integração WhatsApp",
            "Dashboard básico",
            "Gestão de matches e interesses"
        ],
        
        "problemas_atuais": [
            "CSS não responsivo - botões não clicáveis no mobile",
            "Roteamento: / vai para opportunities em vez de dashboard",
            "Visual diferente do MVP original"
        ],
        
        "arquivos_principais": {
            "models": "app/models.py",
            "routes": "app/routes/",
            "templates": "app/templates/", 
            "config": "config.py",
            "requirements": "requirements.txt",
            "mvp_original": "BusinessMatch.html"
        },
        
        "comandos_reinicio": [
            "cd business-match-sebrae",
            "source venv/bin/activate", 
            "python run.py",
            "http://127.0.0.1:5000/"
        ],
        
        "usuarios_teste": [
            {"email": "tech@empresa.com", "senha": "123456", "negocio": "sim"},
            {"email": "consultoria@empresa.com", "senha": "123456", "negocio": "sim"},
            {"email": "novo@empresa.com", "senha": "123456", "negocio": "nao"}
        ]
    }
    
    with open('status_continuacao.json', 'w', encoding='utf-8') as f:
        json.dump(status, f, indent=2, ensure_ascii=False)
    
    print("✅ BACKUP CRIADO: status_continuacao.json")
    print("📋 Cole este arquivo + resumo_mvp.json no próximo chat!")

if __name__ == "__main__":
    criar_backup_completo()
