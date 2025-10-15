#!/usr/bin/env python3
"""
SISTEMA COMPLETO DE ATUALIZAÇÃO
Atualiza status_continuacao.json E gera relatório
"""
import json
from datetime import datetime

def atualizar_tudo(problemas_resolvidos=None, novas_funcionalidades=None, problemas_novos=None):
    # 1. ATUALIZAR STATUS_COTINUACAO.JSON
    with open('status_continuacao.json', 'r') as f:
        status = json.load(f)
    
    status['data_backup'] = datetime.now().isoformat()
    
    # Atualizar problemas
    if problemas_resolvidos:
        status['problemas_atuais'] = [p for p in status['problemas_atuais'] if p not in problemas_resolvidos]
    
    if problemas_novos:
        status['problemas_atuais'].extend(problemas_novos)
    
    # Atualizar funcionalidades
    if novas_funcionalidades:
        status['funcionalidades_implementadas'].extend(novas_funcionalidades)
    
    with open('status_continuacao.json', 'w') as f:
        json.dump(status, f, indent=2, ensure_ascii=False)
    
    print("✅ status_continuacao.json ATUALIZADO")
    
    # 2. GERAR RELATÓRIO_PROGRESSO.MD
    with open('resumo_mvp.json', 'r') as f:
        mvp = json.load(f)
    
    relatorio = {
        "data_geracao": datetime.now().isoformat(),
        "estado_atual": f"Sistema {status['status_geral']['frontend']} - Backend {status['status_geral']['backend']}",
        
        "progresso_recente": {
            "problemas_resolvidos": problemas_resolvidos or [],
            "novas_funcionalidades": novas_funcionalidades or [],
            "funcionalidades_totais": len(status['funcionalidades_implementadas'])
        },
        
        "problemas_ativos": status['problemas_atuais'],
        
        "proximos_passos_sugeridos": [
            "1. CORRIGIR CSS - Implementar Bootstrap responsivo (botões clicáveis)",
            "2. IMPLEMENTAR Admin Dashboard do MVP original", 
            "3. IMPLEMENTAR Cadastro de Produtos do MVP",
            "4. TESTAR responsividade mobile", 
            "5. DEPLOY no Render"
        ],
        
        "prioridade_recomendada": "CSS responsivo → Admin Dashboard → Cadastro Produtos"
    }
    
    with open('RELATORIO_PROGRESSO.md', 'w', encoding='utf-8') as f:
        f.write("# RELATÓRIO DE PROGRESSO - BUSINESS MATCH\\n\\n")
        f.write(f"**Data:** {relatorio['data_geracao']}\\n\\n")
        
        f.write("## 📊 ESTADO ATUAL\\n")
        f.write(f"{relatorio['estado_atual']}\\n\\n")
        
        f.write("## ✅ PROGRESSO RECENTE\\n")
        if relatorio['progresso_recente']['problemas_resolvidos']:
            f.write("**Problemas Resolvidos:**\\n")
            for item in relatorio['progresso_recente']['problemas_resolvidos']:
                f.write(f"- {item}\\n")
        if relatorio['progresso_recente']['novas_funcionalidades']:
            f.write("**Novas Funcionalidades:**\\n")
            for item in relatorio['progresso_recente']['novas_funcionalidades']:
                f.write(f"- {item}\\n")
        f.write(f"**Funcionalidades totais:** {relatorio['progresso_recente']['funcionalidades_totais']}\\n\\n")
        
        f.write("## 🔴 PROBLEMAS ATIVOS\\n")
        for problema in relatorio['problemas_ativos']:
            f.write(f"- {problema}\\n")
        
        f.write("\\n## 🎯 PRÓXIMOS PASSOS SUGERIDOS\\n")
        for passo in relatorio['proximos_passos_sugeridos']:
            f.write(f"{passo}\\n")
        
        f.write(f"\\n## 🚀 PRIORIDADE RECOMENDADA\\n")
        f.write(f"{relatorio['prioridade_recomendada']}\\n")
    
    print("✅ RELATORIO_PROGRESSO.md GERADO")
    
    return relatorio

# EXEMPLOS DE USO:
if __name__ == "__main__":
    print("🔄 SISTEMA DE ATUALIZAÇÃO COMPLETA")
    print("Como usar:")
    print("1. python sistema_atualizacao_completo.py")
    print("2. Editar manualmente a função chamada abaixo")
    print("")
    print("📝 EXEMPLO - Se resolver CSS:")
    print('   atualizar_tudo(')
    print('     problemas_resolvidos=["CSS não responsivo"],')
    print('     novas_funcionalidades=["CSS Bootstrap responsivo"]')
    print('   )')
    
    # ⚠️ EDITAR ESTA CHAMADA SEMPRE QUE PRECISAR:
    atualizar_tudo(
        problemas_resolvidos=["Roteamento: / vai para opportunities em vez de dashboard"],
        novas_funcionalidades=["Roteamento corrigido - / vai para dashboard"]
    )
