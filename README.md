# Caatinga.AI — Sprint 1

**Disciplina:** Inteligência Artificial - Prof. Ronierison Maciel - UniRios - 2026.2
**Dupla:** [SEU NOME AQUI] e [NOME DA SUA DUPLA AQUI]
**Semente usada nos artefatos versionados:** `24114057`

O projeto gera deterministicamente um pomar 12 × 12 a partir da matrícula de um dos alunos, encontra uma rota entre `(0, 0)` e `(11, 11)` e compara BFS, DFS, UCS e A* com três heurísticas. Também contém os módulos de busca local, especialista explicável (Encadeamento para Trás) e cálculos de Teorema de Bayes referentes ao Sprint 1.

## Como executar

Requer Python 3.10 ou superior:

```bash
pip install -r requirements.txt
python src/main.py 24114057
```

O comando recria os artefatos `resultados/pomar.txt`, `resultados/resultados.csv` e `resultados/grafico.png` baseado exclusivamente na matrícula parametrizada. 

## Tabela-Resumo dos Resultados (Matrícula: 24114057)

A ordem de expansão dos vizinhos adotada em todas as buscas é **Norte, Sul, Oeste, Leste**. 
*O algoritmo A\* implementado **reabre um estado** caso encontre um caminho novo de custo estritamente menor que o anterior.*

| Estratégia | Heurística | Custo | Passos | Nós expandidos | Fronteira máxima |
|---|---|---:|---:|---:|---:|
| BFS | — | 34 | 22 | 111 | 10 |
| DFS | — | 74 | 38 | 49 | 31 |
| UCS | — | 28 | 22 | 95 | 14 |
| A* | h1 = 0 | 28 | 22 | 95 | 14 |
| A* | h2 Manhattan | 28 | 22 | 51 | 17 |
| A* | h3 = 4 × Manhattan | 28 | 22 | 23 | 20 |

*Os dados exatos de tempo e milissegundos variam dependendo da CPU que executa e estão dispostos no CSV gerado internamente.*

## Mapa do repositório

- [RELATORIO.md](RELATORIO.md): Respostas e análises teóricas das Partes 1 a 5 da atividade.
- [ANEXO_IA.md](ANEXO_IA.md): Registro obrigatório e específico do uso de assistentes de Inteligência Artificial.
- [src/gerador_pomar.py](src/gerador_pomar.py): Contrato oficial do gerador da grade (Matriz Intocável).
- [src/buscas.py](src/buscas.py): Motores de BFS, DFS, UCS e A* instrumentados.
- [src/busca_local.py](src/busca_local.py): Subida de encosta (Hill Climbing) e Têmpera Simulada (Simulated Annealing).
- [src/especialista.py](src/especialista.py): Regras de decisão do produtor com Encadeamento para Trás.
- [src/bayes.py](src/bayes.py): Motor e cálculos de probabilidade (A Priori e A Posteriori).
- [src/main.py](src/main.py): Ponto de execução único e orquestrador de gráficos.
- [resultados/resultados.csv](resultados/resultados.csv): Tabela reprodutível (saída padrão).
- [resultados/grafico.png](resultados/grafico.png): Plot de nós expandidos (matplotlib).
- [resultados/pomar.txt](resultados/pomar.txt): Plotagem em texto puro da grade usada.

## Limitações conhecidas

- Devido à filosofia acadêmica de validação, algumas métricas físicas na função da busca local são generalizações numéricas e não mapeiam perfeitamente dados de laboratórios agronômicos. 
- O A* foi programado em cima de otimização estrita, permitindo reabertura de frentes custosas que, a depender da volumetria `n > 2000`, engole o limite primário computacional de RAM sem paginação.
