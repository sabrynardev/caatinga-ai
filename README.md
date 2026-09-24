# Caatinga.AI — Sprint 1

**Disciplina:** Inteligência Artificial — UniRios 2026.2  
**Dupla:** [preencher nomes completos e matrículas]  
**Semente usada nos artefatos versionados:** `20231045` (matrícula fictícia de aferição)

O projeto gera deterministicamente um pomar 12 × 12 a partir da matrícula,
encontra uma rota entre `(0, 0)` e `(11, 11)` e compara BFS, DFS, UCS e A*
com três heurísticas. Também contém os módulos de busca local, especialista
explicável e cálculos de Bayes pedidos na atividade.

## Como executar

Python 3.10 ou superior:

```bash
pip install -r requirements.txt
python src/main.py 20231045
```

O comando recria `resultados/pomar.txt`, `resultados/resultados.csv` e
`resultados/grafico.png`. Para outra dupla, substitua a matrícula pelo valor
do integrante mais velho.

## Resultados da aferição

| Estratégia | Heurística | Custo | Passos | Nós expandidos | Fronteira máxima |
|---|---|---:|---:|---:|---:|
| BFS | — | 55 | 22 | 116 | 13 |
| DFS | — | 135 | 66 | 69 | 44 |
| UCS | — | 34 | 22 | 112 | 23 |
| A* | h1 = 0 | 34 | 22 | 112 | 23 |
| A* | h2 Manhattan | 34 | 22 | 93 | 26 |
| A* | h3 = 4 × Manhattan | 34 | 22 | 25 | 20 |

Os tempos medidos em cada execução também ficam no CSV. A ordem de expansão
é **Norte, Sul, Oeste, Leste**. O A* reabre um estado quando encontra um
caminho de custo menor.

## Mapa do repositório

- [RELATORIO.md](RELATORIO.md): respostas e análise das Partes 1 a 5.
- [ANEXO_IA.md](ANEXO_IA.md): registro específico do uso de assistentes.
- [src/gerador_pomar.py](src/gerador_pomar.py): contrato oficial do gerador.
- [src/buscas.py](src/buscas.py): BFS, DFS, UCS e A* instrumentados.
- [src/busca_local.py](src/busca_local.py): subida de encosta e têmpera.
- [src/especialista.py](src/especialista.py): regras e encadeamento para trás.
- [src/bayes.py](src/bayes.py): cálculos de probabilidade posterior.
- [src/main.py](src/main.py): entrada única e geração dos artefatos.
- [resultados/resultados.csv](resultados/resultados.csv): tabela reproduzível.
- [resultados/grafico.png](resultados/grafico.png): gráfico de nós expandidos.
- [resultados/pomar.txt](resultados/pomar.txt): grade usada na aferição.

## Limitações conhecidas

Os experimentos de busca local são uma abstração numérica para permitir
execução sem dados de campo; não representam uma recomendação agronômica.
Nomes, matrículas reais, URL do GitHub e histórico de commits devem ser
preenchidos pela dupla antes da entrega.
