# Relatório — Sprint 1

**Aluno(s):** Raniely Sabrina — 24114057  , Kaynã Filipe — 24114038
**Disciplina/turma:** Inteligência Artificial - Prof. Ronierison Maciel - UniRios - 2026.2

## Parte 1 - O agente antes do código

**1.1 Ficha PEAS**
*   **Performance:** Tempo total de inspeção humana poupado (em horas) e/ou Custo total da rota minimizado (em unidades de energia).
*   **Ambiente (Environment):** Pomar de manga mapeado em grade 12x12, contendo carreadores (custo 1), solos encharcados (custo 4) e bloqueios (#).
*   **Atuadores:** Sistema de movimentação nas quatro direções ortogonais (Norte, Sul, Leste, Oeste).
*   **Sensores:** Sensor óptico de detecção de pragas e sensor de posição (GPS) na grade.

**1.2 Classificação do Ambiente**
*   **Observável (Totalmente):** "O pomar é uma grade de 12 × 12 talhões... Cada talhão é de um dos três tipos". O terreno é conhecido antecipadamente para planejar a rota. *(Discutível)*.
*   **Determinístico:** "Custo do caminho = soma do custo dos talhões em que ele entra". Cada ação de movimento tem consequência garantida.
*   **Sequencial (Não-Episódico):** A rota depende de múltiplos passos encadeados onde uma ação passada afeta posições futuras e a viabilidade da rota.
*   **Estático:** O pomar não se altera fisicamente por conta própria durante o deslocamento. *(Discutível)*.
*   **Discreto:** A movimentação se dá numa matriz e em turnos.
*   **Agente Único:** "um agente que percorre um pomar".

*Dimensões Discutíveis:* 
1) **Observável**: Para a rota, o ambiente é 100% observável. Para achar pragas, ele é *parcialmente observável* (o sensor falha, escondendo a verdade). A informação faltante que decide a questão é: O foco principal em análise é a patrulha física ou a confiabilidade biológica?
2) **Estático**: Assume-se terreno fixo, mas chuva transforma terra (1) em lama (4). A informação faltante: As condições meteorológicas variam no tempo de *uma* patrulha isolada?

**1.3 Tipo de Agente**
*   **Agente Baseado em Utilidade.** Justificativa: O agente não precisa só chegar a (11,11). Distintos caminhos têm penalidades de combustíveis desiguais (custo 1 vs 4). O agente precisa quantificar o custo numérico usando função de utilidade para discernir a rota mais proveitosa.

**1.4 Métrica Perversa**
*   **Proposta:** "Maximizar o número de talhões reportados como suspeitos de praga."
*   **Comportamento (Onde e como):** O agente aprenderá o atalho perigoso de sinalizar os 144 talhões da propriedade como suspeitos para inflar sua pontuação. O erro ocorrerá globalmente. O produtor teria que deslocar agrônomos para investigar tudo, tornando o agente inútil.
*   **Correção:** "Maximizar verdadeiros positivos abatendo uma penalidade financeira brutal no score por cada Falso Positivo investigado à toa."

---

## Parte 2 - Formulação e busca cega

**2.1 Formulação do Problema**
*   **Estado Inicial:** `(0, 0)`.
*   **Ações:** Mover (Norte, Sul, Leste, Oeste).
*   **Modelo de Transição:** `T((r, c), ação) = (nr, nc)` (apenas vizinhos válidos sem `#`).
*   **Teste de Objetivo:** O estado é igual a `(11, 11)`?
*   **Custo do caminho:** Soma cumulativa (1 para carreador firme e 4 para lama).
*   **Espaço de Estados:** Grade 12x12 resulta em 144 posições possíveis. A semente `24114057` gerou exatamente 31 bloqueios `#`. O espaço tem **113 estados**.

**2.2 Tabela de Buscas**
| Estratégia | Custo da rota | Nº de passos | Nós expandidos | Fronteira máx. | Rota ótima em custo? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| BFS | 34 | 22 | 111 | 10 | Não |
| DFS | 74 | 38 | 49 | 31 | Não |
| UCS | 28 | 22 | 95 | 14 | Sim |

**2.3 Rota mais cara na BFS**
Não é um bug. A BFS garante sempre o menor *número de arestas/passos*. De acordo com a Aula 03, isso só equivale ao menor custo se os "passos tiverem custo uniforme". Nossa hipótese uniforme foi violada pelas frentes de custo 4, fazendo com que a rota mais curta em metros fosse a pior em eficiência.

**2.4 Limites (Aumento de n)**
Aumentando `n` para grandezas severas (ex: `n=2000` em diante), as buscas explodem em **Limite de Memória (Out of Memory)** antes mesmo da CPU estagnar. Relaciona-se com a barreira limite da complexidade $O(b^d)$, visto que os algoritmos mantêm todos os nós visitados/explorados na fronteira em memória primária.

---

## Parte 3 - Busca informada

**3.1 Tabela A\***
| Heurística | Custo da rota | Nós expandidos | Admissível? (prove) |
| :--- | :--- | :--- | :--- |
| h1 | 28 | 95 | Sim |
| h2 | 28 | 51 | Sim |
| h3 | 28 | 23 | Não |

**3.2 Provas de Admissibilidade**
*   **h2 (Admissível):** Manhattan conta o número mínimo de células distantes. Já que o custo mínimo possível da grade para entrar em qualquer talhão é 1, `h2(n)` nunca excederá o valor real de deslocamento. É otimista por definição.
*   **h3 (Superestimada):** Tomando a coordenada inicial `(0,0)` para o fim `(11,11)`. A distância bruta (h2) é 22. A fórmula h3 prevê `22 * 4 = 88`. Todavia, nós já medimos o custo exato dessa travessia na UCS, que foi de **28**. Se h(n) estimou 88 e o real era 28, ela quebrou a premissa admissível.

**3.3 h3 comparado com UCS**
O custo devolvido foi igualzinho (28). **Isso prova que ela é admissível? Não!** 
A matemática não perdoa: para provar admissibilidade a hipótese não pode falhar *em nenhuma semente possível do universo*. O fato de termos achado o ótimo para este mapa provou apenas que os obstáculos do nosso cenário obrigaram o robô a seguir um afunilamento comum. 
*   *Situação de negócio:* A troca de exatidão teórica por velocidade é essencial caso o AGV colheitadeira se depare com uma vaca na plantação; ele precisa evitar o bloqueio em *ms*. Usar a UCS processaria 95 nós, engasgando o CPU interno, mas a h3 foi quase 4 vezes mais eficiente (23 nós expandidos), liberando o freio a tempo.

**3.4 Busca Local (K=15)**
Realizados 30 ensaios com variação randomizada.
*   **Subida de Encosta:** Média = -0.00355, Desvio = 0.00301, Melhor = -0.00010
*   **Têmpera Simulada:** Média = -0.00012, Desvio = 0.00015, Melhor = -0.000001
*   **Piora de Propósito:** O algoritmo Hill Climbing sempre travou num patamar falso porque só aceitava melhoras. A Aula 04 evidencia que a temperatura de derretimento da Têmpera a faz tolerar pioras calculadas na subida. Ao pular ladeira abaixo temporariamente, nossa Têmpera descolou dos ótimos locais medíocres de `-0.003` para encostar no ótimo global de `10^-6`.

---

## Parte 4 - Lógica e Bayes

**4.1 e 4.2 Especialista e Quebra de Base**
Ver a execução no `src/especialista.py`. Implementamos uma cadeia encadeada para trás que refuta um falso diagnóstico de praga pela constatação de chuva pesada recém passada (sujeira na lente).

**4.3 Bayes**
*(Semente: Prevalência = 0.0093, Sensibilidade = 0.99, Falso Positivo = 0.08, Consultas = 800)*

**a)** `P(Infestado | Positivo)` = `(P(Pos|Inf) * P(Inf)) / (P(Pos|Inf)*P(Inf) + P(Pos|~Inf)*P(~Inf))`  
= `(0.99 * 0.0093) / (0.99 * 0.0093 + 0.08 * 0.9907)` = `0.009207 / (0.009207 + 0.079256)` = **10,41%**
**b)** A cada 100 alertas do meu sistema, cerca de **90 serão falsos**.
**c)** Em 800 talhões sondados, há ~70,8 alertas totais. Com ~89,6% de falsidade, sobram **63,4 falsos alertas** semanais. A 12 minutos cada, a fazenda desperdiça **12,68 horas por semana**.
**d)** Turbinar o sensor para 99.9% mal reverteu o VPP (subiu para apenas **10,49%**). O problema persiste. Eu reengenharia a **Taxa de Falsos Positivos**: Como doentes são só 0.9%, o número mastodôntico de plantas sadias (99.1%) vezes 8% de falso positivo abarrota a linha cruzada, engolindo os raros verdadeiros positivos.

**4.4 Regra que salva o modelo**
*   **Decisão Explicita:** "SE for emitido alarme civil para ventos ciclônicos/raios severos ENTÃO abortar inspeção e trancar nos galpões limítrofes".
*   **Justificativa (Sem Citar Acurácia):** Essa regra blinda o consórcio fabricante e atende regulamentos ISO e seguradoras (auditabilidade/compliance legal). Redes Neurais geram predições estocásticas baseadas em peso que não podem ser comprovadas a priori no tribunal se a máquina matar um funcionário sob temporal. Regras duras protegem a responsabilidade corporativa.

---

## Parte 5 - Auditoria do laudo do fornecedor (AgroVision)

1.  **Incorreta.** A métrica de multiplicar `Manhattan x 4` acaba de quebrar a barreira de admissibilidade, já que o A* com `h3` julga custar 88 onde só custa 28. O laudo vende falsamente o algoritmo como perfeitamente ótimo ao cliente.
2.  **Parcialmente correta.** De fato o custo derreteu 38% (de 55 para 34 ou inferior). Todavia, não é mérito primário da "Heurística". Foi a BFS padrão que estragou tudo ignorando os terrenos enlameados. Mesmo sem usar métricas complexas (ex: h1 que vale nulo e replica a UCS), a melhora da qualidade de solução apareceria do mesmo modo pela virtude de focar no peso (Uniform Cost).
3.  **Incorreta.** Argumento falacioso clichê batendo contra a Taxa Base. Uma Sensibilidade incrível não opera sozinha. Com apenas `0.93%` dos pés de manga realmente sofrendo de pragas nos nossos testes, nós aferimos cabalmente que a chance exata de infestação cruzada no alerta luminoso se limita a vergonhosos **10,41%**.
4.  **Incorreta.** Aplicar bayes duplamente pede uma fortíssima garantia da Teoria de Probabilidades de que as avaliações são genuinamente indepedentes estatisticamente (ex: se for uma poeira pregada na lente óptica, ambos os tiros emitirão alarmes simultâneos falsos, zerando o isolamento).
5.  **Incorreta.** A memória diminui pela filosofia da expansão profunda, contudo, a DFS devolveu nos testes locais o custo repulsivo absurdo de **74 pontos** de energia, muito maior que as opções competentes (28). Adotar DFS torrará a bateria das viaturas pela ganância cega de memória.

**Recomendação Final para a Diretoria:**
**Recusar a proposta.** O laudo da AgroVision demonstra profundo desconhecimento técnico-matemático de IA, prometendo otimalidade onde não há (A* h3) e cometendo a Falácia da Taxa Base (confundindo sensibilidade com VPP, gerando alarmes 90% falsos). A única condição técnica que mudaria nossa recomendação para "contratar com ressalvas" seria se eles re-arquitetassem a heurística para h1 ou h2 garantindo a segurança de custo, e propusessem um novo modelo Bayesiano com drástica redução da Taxa de Falsos Positivos do sensor para compensar a baixa prevalência da praga.
