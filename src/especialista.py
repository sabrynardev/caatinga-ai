"""Sistema especialista explicável com encadeamento para trás (Backward Chaining).
O programa decide o manejo de um talhão a partir de fatos baseados no clima e sensor."""

# 5 a 8 Regras Estruturadas
# Formato: (premissas_necessarias, conclusao, texto_explicativo)
REGRAS = [
    # Regra 1
    ({"sensor_positivo", "folha_amarelada"}, "praga_fungo", 
     "SE sensor apita E folha está amarelada ENTÃO há alta chance de praga fúngica."),
    
    # Regra 2
    ({"praga_fungo"}, "aplicar_fungicida", 
     "SE praga fúngica detectada ENTÃO tratamento requer aplicar fungicida."),
    
    # Regra 3
    ({"umidade_alta", "solo_encharcado"}, "suspender_irrigacao", 
     "SE a umidade está alta E o solo está encharcado ENTÃO suspender a irrigação de imediato."),
    
    # Regra 4
    ({"aplicar_fungicida", "suspender_irrigacao"}, "inspecionar_urgencia", 
     "SE fungicida foi recomendado E irrigação está suspensa ENTÃO marcar talhão para inspeção humana com urgência."),
    
    # Regra 5
    ({"temperatura_alta", "solo_seco"}, "ativar_irrigacao_extra", 
     "SE temperatura está alta E solo seco ENTÃO ativar gotejamento de irrigação extra."),
    
    # Regra 6 (Regra baseada na Parte 4.4 de negócio/auditabilidade)
    ({"alerta_raios_civis"}, "recolher_robo", 
     "SE alarme de tempestade elétrica ou raios emitido ENTÃO recolher imediatamente o agente.")
]

def encadeamento_para_tras(objetivo, fatos_conhecidos, regras, arvore_explicacao):
    """
    Tenta provar o 'objetivo' recursivamente checando se já é um fato.
    Caso não seja, procura uma regra onde a conclusão seja o objetivo e
    tenta provar recursivamente todas as premissas dessa regra.
    """
    # 1. Base: Se o objetivo já for um fato conhecido, é verdade direto.
    if objetivo in fatos_conhecidos:
        return True
    
    # 2. Passo Recursivo: Procurar regras que provem o objetivo
    for premissas, conclusao, explicacao in regras:
        if conclusao == objetivo:
            todas_premissas_verdadeiras = True
            
            for p in premissas:
                # Checa se a premissa pode ser provada
                if not encadeamento_para_tras(p, fatos_conhecidos, regras, arvore_explicacao):
                    todas_premissas_verdadeiras = False
                    break
            
            # Se conseguimos provar todas as premissas, a regra é acionada!
            if todas_premissas_verdadeiras:
                if explicacao not in arvore_explicacao:
                    arvore_explicacao.append(explicacao)
                return True

    return False

def recomendar(fatos_conhecidos):
    """
    Roda os objetivos principais do negócio e retorna a resposta de 
    'por que o agente tomou a decisão'.
    """
    objetivos_finais = ["inspecionar_urgencia", "recolher_robo", "ativar_irrigacao_extra", "aplicar_fungicida", "suspender_irrigacao"]
    
    recomendacoes_finais = []
    
    for objetivo in objetivos_finais:
        arvore = []
        if encadeamento_para_tras(objetivo, set(fatos_conhecidos), REGRAS, arvore):
            # Se provou, junta o raciocínio encadeado na string final
            traco_decisao = " -> ".join(arvore)
            recomendacoes_finais.append({"acao": objetivo, "explicacao": traco_decisao})
            
    return recomendacoes_finais

if __name__ == "__main__":
    # CASO DE TESTE (Para testar se o encadeamento está imprimindo o rastro).
    fatos_do_talhao = ["sensor_positivo", "folha_amarelada", "umidade_alta", "solo_encharcado"]
    print("Fatos captados:", fatos_do_talhao)
    
    resultados = recomendar(fatos_do_talhao)
    print("\nDecisões Tomadas e Porquê (Encadeamento Para Trás):")
    for r in resultados:
        print(f"\nAÇÃO: {r['acao']}")
        print(f"POR QUE CONCLUIU ISSO? Cadeia Lógica: {r['explicacao']}")