#!/usr/bin/env python3
"""
Script de diagnóstico completo do Business Match
"""
import os
import re

def analisar_templates():
    print("🎯 ANÁLISE DOS TEMPLATES E CSS")
    print("=" * 50)
    
    templates_dir = "app/templates"
    css_files = list(os.listdir("app/static/css")) if os.path.exists("app/static/css") else []
    
    print(f"📁 CSS disponíveis: {css_files}")
    print("")
    
    templates = []
    for file in os.listdir(templates_dir):
        if file.endswith(".html"):
            filepath = os.path.join(templates_dir, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verificar referências CSS
            css_refs = re.findall(r'static/css/([^"]+)', content)
            style_tags = len(re.findall(r'<style>', content))
            
            templates.append({
                'arquivo': file,
                'css_externo': css_refs,
                'css_inline': style_tags > 0,
                'usa_base': '{% extends' in content,
                'linhas': len(content.split('\n'))
            })
    
    print("📊 RESUMO POR TEMPLATE:")
    print("-" * 80)
    for tpl in templates:
        status = "✅" if tpl['css_externo'] or tpl['css_inline'] else "❌"
        print(f"{status} {tpl['arquivo']:25} | CSS: {tpl['css_externo'] or 'NENHUM'} | Inline: {tpl['css_inline']} | Base: {tpl['usa_base']}")
    
    # Estatísticas
    sem_css = sum(1 for t in templates if not t['css_externo'] and not t['css_inline'])
    com_base = sum(1 for t in templates if t['usa_base'])
    
    print("")
    print("📈 ESTATÍSTICAS:")
    print(f"   Total de templates: {len(templates)}")
    print(f"   ❌ Sem CSS referenciado: {sem_css}")
    print(f"   ✅ Com template base: {com_base}")
    print(f"   📝 Com CSS inline: {sum(1 for t in templates if t['css_inline'])}")
    
    return templates, sem_css

def recomendar_acao(templates, sem_css):
    print("")
    print("💡 RECOMENDAÇÕES DE AÇÃO:")
    print("=" * 50)
    
    if sem_css == len(templates):
        print("🚨 CRÍTICO: Nenhum template está referenciando CSS!")
        print("   Ação: Criar base.html e refatorar todos os templates")
    elif sem_css > len(templates) * 0.5:
        print("⚠️  ALERTA: Mais da metade dos templates sem CSS!")
        print("   Ação: Criar base.html e refatorar templates críticos")
    else:
        print("✅ CONTROLADO: A maioria tem CSS, ajustar específicos")
    
    # Templates críticos (core business)
    criticos = ['opportunities.html', 'matches.html', 'dashboard.html', 'profile.html']
    templates_criticos_sem_css = [t for t in templates if t['arquivo'] in criticos and not t['css_externo']]
    
    if templates_criticos_sem_css:
        print("")
        print("🎯 TEMPLATES CRÍTICOS QUE PRECISAM DE CSS URGENTE:")
        for tpl in templates_criticos_sem_css:
            print(f"   • {tpl['arquivo']}")

if __name__ == "__main__":
    templates, sem_css = analisar_templates()
    recomendar_acao(templates, sem_css)
