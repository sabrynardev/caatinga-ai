# ANEXO_IA — Uso de assistentes

## A.1 Ferramentas e partes

Foi usado um assistente de IA integrado ao VS Code para estruturar os
módulos Python, revisar a ficha PEAS, sugerir testes e conferir cálculos de
Bayes. A execução do programa e a conferência dos valores de referência
foram feitas localmente.

## A.2 Prompts e respostas

**Prompt 1 (íntegra):**

> Analise meu problema de busca em uma matriz 12x12 onde andar no chão seco
> custa 1 e atolar na lama custa 4. Preciso de uma heurística admissível
> para A*. Para h3 quero multiplicar Manhattan por 4. Essa heurística
> continua admissível? Responda formalmente.

**Resposta recebida:** não. Multiplicar Manhattan por 4 pode superestimar o
custo real e viola `h(n) <= h*(n)`, retirando a garantia de optimalidade.

**Prompt 2 (íntegra):**

> Audite este cálculo de Bayes de um sensor agrícola com prevalência 0,93%,
> sensibilidade 99% e falso positivo 8%. Quero saber o VPP e quantos falsos
> alertas aparecem em 800 inspeções semanais.

**Resposta recebida:** aplicando a taxa-base, o VPP é aproximadamente 10,41%;
portanto a maioria dos alertas é falsa, apesar da alta sensibilidade.

## A.3 Erro encontrado

A primeira implementação gerada pelo assistente substituiu o gerador oficial
por outro gerador, usando parâmetros diferentes e até símbolos de início e
fim. A conferência com o contrato do enunciado detectou o erro. O arquivo
foi restaurado e os valores foram conferidos pela caixa de aferição: para
20231045, BFS custou 34 e UCS custou 28 na primeira aferição oficial; na execução da
semente da dupla, BFS custou 34 e UCS custou 28.

## A.4 O que só soubemos após executar

Só depois de executar soubemos os números concretos de expansão do nosso
mapa, como UCS = 95 e A* Manhattan = 51 na semente da dupla; esses
valores não poderiam ser confirmados apenas pela resposta textual.
