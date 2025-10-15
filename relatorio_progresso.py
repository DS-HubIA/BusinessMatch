#!/usr/bin/env python3
"""
SISTEMA DE RELATÓRIO DE PROGRESSO - Versão Simplificada
Gera: Onde estamos + Progresso + Próximos passos
"""
import json
from datetime import datetime

def gerar_relatorio():
    # Carrega arquivos existentes
    with open('status_continuacao.json', 'r') as f:
        status = json.load(f)
    
    with open('resumo_mvp.json', 'r') as f:
        mvp = json.load(f)
    
    # Gera relatório consolidado
    relatorio = {
        "data_geracao": datetime.now().isoformat(),
        "estado_atual": f"Sistema {status['status_geral']['frontend']} - Backend {status['status_geral']['backend']}",
        
        "progresso_recente": {
            "problemas_resolvidos": [
                "Roteamento corrigido - / vai para dashboard"
            ],
            "funcionalidades_implementadas": status['funcionalidades_implementadas']
        },
        
        "problemas_ativos": status['problemas_atuais'],
        
        "proximos_passos_sugeridos": [
            "1. CORRIGIR CSS - Implementar Bootstrap responsivo (botões clicáveis)",
            "2. IMPLEMENTAR Admin Dashboard do MVP original", 
            "3. IMPLEMENTAR Cadastro de Produtos do MVP",
            "4. TESTAR responsividade mobile",
            "5. DEPLOY no Render"
        ],
        
        "prioridade_recomendada": "CSS responsivo → Admin Dashboard → Cadastro Produtos",
        
        "contexto_anexos": [
            "resumo_mvp.json (funcionalidades desejadas)",
            "status_continuacao.json (status atual)",
            "contexto_proximo_chat.json (método trabalho)"
        ]
    }
    
    # Salva relatório
    with open('RELATORIO_PROGRESSO.md', 'w', encoding='utf-8') as f:
        f.write("# RELATÓRIO DE PROGRESSO - BUSINESS MATCH\n\n")
        f.write(f"**Data:** {relatorio['data_geracao']}\n\n")
        
        f.write("## 📊 ESTADO ATUAL\n")
        f.write(f"{relatorio['estado_atual']}\n\n")
        
        f.write("## ✅ PROGRESSO RECENTE\n")
        for item in relatorio['progresso_recente']['problemas_resolvidos']:
            f.write(f"- {item}\n")
        f.write(f"\n**Funcionalidades ativas:** {len(relatorio['progresso_recente']['funcionalidades_implementadas'])}\n\n")
        
        f.write("## 🔴 PROBLEMAS ATIVOS\n")
        for problema in relatorio['problemas_ativos']:
            f.write(f"- {problema}\n")
        
        f.write("\n## 🎯 PRÓXIMOS PASSOS SUGERIDOS\n")
        for passo in relatorio['proximos_passos_sugeridos']:
            f.write(f"{passo}\n")
        
        f.write(f"\n## 🚀 PRIORIDADE RECOMENDADA\n")
        f.write(f"{relatorio['prioridade_recomendada']}\n")
        
        f.write("\n## 📁 CONTEXTO ANEXADO\n")
        for arquivo in relatorio['contexto_anexos']:
            f.write(f"- {arquivo}\n")
    
    print("✅ RELATÓRIO GERADO: RELATORIO_PROGRESSO.md")
    return relatorio

if __name__ == "__main__":
    relatorio = gerar_relatorio()
    print(f"\n📋 RESUMO:")
    print(f"Estado: {relatorio['estado_atual']}")
    print(f"Problemas ativos: {len(relatorio['problemas_ativos'])}")
    print(f"Próximos passos: {len(relatorio['proximos_passos_sugeridos'])}")
    print(f"\n🎯 NO PRÓXIMO CHAT: Cole o arquivo RELATORIO_PROGRESSO.md")
