# Relatório — Sprint 1

**Aluno(s):** [NOME — MATRÍCULA]  
**Disciplina/turma:** [PREENCHER]

## Objetivo e método

O programa gera uma grade 12x12 de pomar com semente derivada da matrícula.
Obstáculos são `#`; entrar em `.` custa 1 e entrar em `~` custa 4. Os
vizinhos são visitados em ordem Norte, Sul, Oeste, Leste. O CSV compara BFS,
DFS, UCS e A* com h1 (zero), h2 (Manhattan) e h3 (4 vezes Manhattan), incluindo
passos, custo, nós expandidos e fronteira máxima.

A busca local usa vizinhança de **K=15** candidatos na subida de encosta e
têmpera simulada. São realizadas 30 execuções independentes, com sementes
reprodutíveis. O especialista usa encadeamento para trás e devolve a
explicação da regra disparada. O módulo Bayes calcula a probabilidade
posterior de praga, explicitando sensibilidade e falso positivo.

## Resultados

Na validação com `python src/main.py 20231045`, BFS produziu custo 55 e 22
passos; UCS produziu custo 34. As expansões e a fronteira máxima são
registradas no CSV e o gráfico representa nós expandidos.

## Limitações

O modelo é acadêmico: terreno, custos e regras são simplificações e não
constituem recomendação agronômica real.