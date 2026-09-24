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
