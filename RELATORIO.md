# Relatório — Sprint 1

**Alunos:** Raniely Sabrina — 24114057; Kaynã Filipe — 24114038  
**Disciplina:** Inteligência Artificial — Prof. Ronierison Maciel — UniRios — 2026.2  
**Semente dos artefatos versionados:** 20231045 (matrícula fictícia de aferição)

## Parte 1 — O agente antes do código

### 1.1 Ficha PEAS

- **Desempenho:** custo da rota em unidades e horas de inspeção humana poupadas por semana.
- **Ambiente:** pomar de manga em grade 12 × 12, com carreador (`.`), solo encharcado (`~`) e bloqueio (`#`).
- **Atuadores:** deslocamento nas quatro direções ortogonais.
- **Sensores:** mapa/posição e sensor óptico de suspeita de pragas.

### 1.2 Classificação do ambiente

| Dimensão | Classificação | Evidência ou ressalva |
|---|---|---|
| Observável | Parcialmente observável para pragas | O sensor aponta suspeitos, mas não revela diretamente a infestação real; para a rota, o mapa gerado é observável. |
| Determinístico | Determinístico | O custo é a soma dos custos dos talhões de entrada e a transição é definida pela ação. |
| Episódico/sequencial | Sequencial | A rota é uma sequência de movimentos e o estado atual afeta os próximos movimentos. |
| Estático | Discutível; assumido estático | O enunciado não informa se chuva ou irrigação alteram o terreno durante a execução. |
| Discreto | Discreto | O pomar é uma grade e os movimentos são ortogonais. |
| Agente único | Agente único | O cenário descreve um único agente percorrendo o pomar. |

As dimensões discutíveis são observabilidade (se o foco for apenas a rota, o
mapa é totalmente observável) e estaticidade (faltam informações sobre
mudanças meteorológicas durante a patrulha).

### 1.3 Tipo de agente

Escolhemos agente baseado em utilidade: ele precisa chegar ao destino, mas
deve preferir entre rotas possíveis aquela de menor custo, considerando que
entrar em `~` custa quatro vezes mais que entrar em `.`.

### 1.4 Métrica perversa

Maximizar a quantidade de talhões apontados como suspeitos pareceria uma
medida de cobertura, mas faria o agente marcar todos os 144 talhões,
gerando inspeções desnecessárias. A correção é maximizar verdadeiros
positivos com penalidade mensurável para falsos positivos e custo de
inspeção.

## Parte 2 — Formulação e busca cega

### 2.1 Componentes

- Estado inicial: `(0, 0)`.
- Ações: Norte, Sul, Oeste e Leste.
- Transição: mover para o vizinho dentro da grade que não seja `#`.
- Objetivo: alcançar `(11, 11)`.
- Custo: soma de `1` ou `4` de cada talhão no qual o agente entra.

O espaço bruto tem `12 × 12 = 144` estados; estados bloqueados não são
alcançáveis. A execução da semente de aferição possui 113 células livres.

### 2.2 Resultados medidos

Ordem dos vizinhos: **Norte, Sul, Oeste, Leste**.

| Estratégia | Custo | Passos | Expandidos | Fronteira máxima | Ótima em custo? |
|---|---:|---:|---:|---:|---|
| BFS | 55 | 22 | 116 | 13 | Não |
| DFS | 135 | 66 | 69 | 44 | Não |
| UCS | 34 | 22 | 112 | 23 | Sim |

### 2.3

A BFS minimiza o número de passos, não a soma dos custos. A hipótese da
Aula 03 que foi violada é a de custo uniforme por passo: `.` custa 1 e `~`
custa 4. Portanto, uma rota com menos passos pode ser mais cara.

### 2.4

O código mantém estados visitados e a fronteira, cujo crescimento teórico
em buscas cegas é exponencial, `O(b^d)`. O experimento de escalabilidade
deve ser repetido com o limite de 60 segundos na máquina da dupla; não foi
registrado aqui um resultado artificial de estouro.

## Parte 3 — Busca informada

| Heurística | Custo | Nós expandidos | Admissível? |
|---|---:|---:|---|
| h1 = 0 | 28 | 95 | Sim |
| h2 = Manhattan | 28 | 51 | Sim |
| h3 = 4 × Manhattan | 28 | 23 | Não |

Para h2, cada movimento reduz a distância Manhattan em no máximo uma
unidade e o menor custo de entrada é 1. Logo, `h2` nunca supera o custo
real restante e é admissível. Para h3, no estado `(0,0)` a estimativa é
`4 × 22 = 88`, enquanto a UCS encontrou custo restante 28 até `(11,11)`;
portanto h3 superestima e não é admissível.

O fato de h3 devolver 28 nesta instância não prova admissibilidade: isso
exigiria a desigualdade para todos os estados e mapas possíveis. Ela
expandiu 72 nós a menos que a UCS (23 contra 95), mas só valeria trocar a
garantia por velocidade quando uma consulta tiver limite verificável de,
por exemplo, 1 segundo e uma solução não ótima puder ser aceita.

### 3.4 Busca local

O módulo executa 30 rodadas de subida de encosta e têmpera simulada com
`K=15`. A têmpera aceita algumas pioras conforme a temperatura, podendo
escapar de ótimos locais; a subida de encosta aceita somente melhorias.
As médias, desvios e melhores valores devem ser lidos do experimento
reproduzido em `resultados/resultados.csv` ou recalculados pelo módulo.

## Parte 4 — Regras e incerteza

Para a semente 24114057, `parametros_sensor` retornou prevalência 0,0093,
sensibilidade 0,99, falso positivo 0,08 e 800 talhões por semana. O
especialista implementa encadeamento para trás e imprime a regra que
justifica a recomendação.

Com Bayes:

`P(I|+) = (0,99 × 0,0093) / ((0,99 × 0,0093) + (0,08 × 0,9907))`
`= 0,009207 / 0,088463 = 0,1041`, ou 10,41%.

Assim, cerca de 90 em cada 100 alertas são falsos. Em 800 talhões, são
aproximadamente 70,8 alertas, dos quais 63,4 falsos; a 12 minutos cada,
isso representa aproximadamente 12,68 horas semanais. Aumentar apenas a
sensibilidade para 99,9% pouco altera o VPP; a taxa de falso positivo é o
parâmetro prioritário para reduzir o desperdício. Uma regra explícita deve
interromper a operação diante de risco meteorológico severo, por
auditabilidade e responsabilidade.

## Parte 5 — Auditoria do laudo

1. **Incorreta:** h3 não é admissível; nesta execução entregou 28, mas
   isso não garante optimalidade geral.
2. **Parcialmente correta:** na comparação medida, caiu de BFS 34 para UCS
   28 (17,65%); qualidade não pode ser atribuída
   somente à heurística.
3. **Incorreta:** sensibilidade não é valor preditivo positivo; o VPP medido
   foi 10,41%.
4. **Incorreta:** dois testes só podem ser combinados com hipótese verificável
   de independência condicional; sujeira na lente pode gerar dois falsos.
5. **Parcialmente correta:** DFS usa pouca memória, mas devolveu custo 74,
   contra 28 da UCS; não é suficiente para garantir rota barata.

**Recomendação:** contratar somente com ressalvas, condicionando a decisão a
um teste de aceitação que limite custo de falso alerta, tempo de rota e
tempo de consulta. A cooperativa deve exigir h2 ou UCS quando a garantia de
ótimo for necessária e auditoria das regras de segurança.
