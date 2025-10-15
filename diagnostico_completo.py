#!/usr/bin/env python3
"""
DIAGNÓSTICO COMPLETO DO MVP ORIGINAL
Extrai todas as funcionalidades, estrutura e requisitos
"""
import os
import re
import json
from collections import Counter

def analisar_mvp_completo(arquivo_html):
    print("🔍 ANALISANDO MVP ORIGINAL - FUNCIONALIDADES COMPLETAS")
    print("=" * 60)
    
    with open(arquivo_html, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 1. FUNCIONALIDADES IDENTIFICADAS
    print("\n🎯 FUNCIONALIDADES ENCONTRADAS:")
    
    funcionalidades = {
        'Admin Dashboard': any(keyword in content.lower() for keyword in ['admin', 'dashboard', 'administrativo']),
        'Cadastro Produtos': any(keyword in content.lower() for keyword in ['cadastro', 'produto', 'product', 'cadastrar']),
        'Autenticação': any(keyword in content.lower() for keyword in ['login', 'register', 'signup', 'entrar']),
        'Swipe/Match': any(keyword in content.lower() for keyword in ['swipe', 'match', 'like', 'dislike']),
        'Chat/WhatsApp': any(keyword in content.lower() for keyword in ['chat', 'whatsapp', 'mensagem', 'conversar']),
        'Perfil Usuário': any(keyword in content.lower() for keyword in ['perfil', 'profile', 'usuário', 'user']),
        'Busca/Filtros': any(keyword in content.lower() for keyword in ['busca', 'search', 'filtrar', 'filter'])
    }
    
    for func, existe in funcionalidades.items():
        status = "✅" if existe else "❌"
        print(f"  {status} {func}")
    
    # 2. ESTRUTURA DE PÁGINAS
    print("\n📄 PÁGINAS/SEÇÕES IDENTIFICADAS:")
    paginas = re.findall(r'<(?:h1|h2|title)[^>]*>([^<]+)</', content, re.IGNORECASE)
    if paginas:
        for pagina in set(paginas[:10]):
            print(f"  📍 {pagina.strip()}")
    
    # 3. FORMULÁRIOS E INPUTS
    print("\n📝 FORMULÁRIOS E CAMPOS:")
    forms = re.findall(r'<input[^>]*name="([^"]*)"', content) + \
            re.findall(r'<select[^>]*name="([^"]*)"', content) + \
            re.findall(r'<textarea[^>]*name="([^"]*)"', content)
    
    for campo in set(forms[:15]):
        print(f"  ✏️  {campo}")
    
    # 4. BOTÕES E AÇÕES
    print("\n🔄 AÇÕES/BOTÕES PRINCIPAIS:")
    botoes = re.findall(r'<button[^>]*>([^<]+)</button>', content) + \
             re.findall(r'btn-[^"\' ]+', content) + \
             re.findall(r'onclick="([^"]*)"', content)
    
    for btn in set(botoes[:15]):
        if len(btn) > 2 and len(btn) < 50:
            print(f"  🔘 {btn}")
    
    # 5. ESTRUTURA TÉCNICA
    print("\n⚙️  ESTRUTURA TÉCNICA:")
    
    # Frameworks CSS
    css_frameworks = {
        'Bootstrap': 'bootstrap' in content.lower(),
        'Tailwind': 'tailwind' in content.lower(), 
        'CSS Puro': '<style>' in content,
        'JavaScript': '<script>' in content
    }
    
    for framework, usa in css_frameworks.items():
        if usa:
            print(f"  🛠️  Usa {framework}")
    
    # 6. RECOMENDAÇÕES PARA MIGRAÇÃO
    print("\n🎯 PLANO DE MIGRAÇÃO PARA FLASK:")
    print("  1. Manter todas as funcionalidades identificadas ✅")
    print("  2. Recriar estrutura de templates Flask")
    print("  3. Implementar backend para cada formulário")
    print("  4. Manter frontend responsivo")
    print("  5. Adicionar autenticação Flask-Login")
    print("  6. Implementar banco PostgreSQL")
    
    # 7. SALVAR RESUMO PARA PRÓXIMO CHAT
    resumo = {
        'funcionalidades': [f for f, existe in funcionalidades.items() if existe],
        'formularios': list(set(forms)),
        'botoes_principais': [b for b in set(botoes) if len(b) > 2 and len(b) < 50],
        'tecnicas': [f for f, usa in css_frameworks.items() if usa]
    }
    
    with open('resumo_mvp.json', 'w') as f:
        json.dump(resumo, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resumo salvo em: resumo_mvp.json")
    print("📋 Cole este JSON no próximo chat para continuarmos!")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        analisar_mvp_completo(sys.argv[1])
    else:
        print("Uso: python diagnostico_completo.py caminho/do/mvp_original.html")
        print("\nExemplo: python diagnostico_completo.html ~/Downloads/mvp_completo.html")
