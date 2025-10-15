#!/usr/bin/env python3
"""
SCRIPT PARA ATUALIZAR STATUS_CONTINUACAO.JSON
Execute sempre que houver progresso significativo
"""
import json
from datetime import datetime

def atualizar_status(novos_itens=None, problemas_resolvidos=None):
    # Ler status atual
    with open('status_continuacao.json', 'r') as f:
        status = json.load(f)
    
    # Atualizar data
    status['data_backup'] = datetime.now().isoformat()
    
    # Adicionar novos itens se fornecidos
    if novos_itens:
        if 'funcionalidades_implementadas' not in status:
            status['funcionalidades_implementadas'] = []
        status['funcionalidades_implementadas'].extend(novos_itens)
    
    # Remover problemas resolvidos
    if problemas_resolvidos:
        status['problemas_atuais'] = [p for p in status['problemas_atuais'] if p not in problemas_resolvidos]
    
    # Salvar atualizado
    with open('status_continuacao.json', 'w', encoding='utf-8') as f:
        json.dump(status, f, indent=2, ensure_ascii=False)
    
    print("✅ STATUS ATUALIZADO!")
    print(f"   Data: {status['data_backup']}")
    if novos_itens:
        print(f"   Novas funcionalidades: {novos_itens}")
    if problemas_resolvidos:
        print(f"   Problemas resolvidos: {problemas_resolvidos}")

# Exemplo de uso:
if __name__ == "__main__":
    print("Como usar:")
    print("1. Para adicionar funcionalidade:")
    print('   atualizar_status(novos_itens=["Funcionalidade X"])')
    print("2. Para marcar problema resolvido:")
    print('   atualizar_status(problemas_resolvidos=["Problema Y"])')
    print("3. Para ambos:")
    print('   atualizar_status(novos_itens=["X"], problemas_resolvidos=["Y"])')
