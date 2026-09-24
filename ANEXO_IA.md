# ANEXO_IA — Uso de assistentes

## A.1 Ferramentas e partes

Foi usado um assistente de IA no VS Code para estruturar os módulos Python,
sugerir testes e revisar a integração. A execução, a comparação com a caixa
de aferição e a conferência do gerador foram feitas localmente pelos autores.

## A.2 Prompts e respostas

**Prompt 1 (íntegra):**

> Implemente completamente o projeto no diretório conforme o enunciado,
> criando os módulos de buscas, busca local, especialista, Bayes e o comando
> principal.

**Resposta recebida:** o assistente criou os módulos, os artefatos e informou
que `python src/main.py 20231045` havia sido executado com sucesso.

**Prompt 2 (íntegra):**

> Corrija imediatamente a implementação conforme o enunciado literal:
> gerador oficial intacto, custos 1 e 4, ordem Norte/Sul/Oeste/Leste,
> contadores completos, A* com h1/h2/h3 e validação contra BFS 55, UCS 34
> e BFS com 22 passos.

**Resposta recebida:** o assistente corrigiu as buscas e informou os valores
de referência. A inspeção humana ainda foi necessária.

## A.3 Erro encontrado

A primeira versão afirmava que `gerador_pomar.py` estava conforme o
enunciado, mas ele havia sido substituído por outro gerador, com parâmetros e
mapa diferentes. Ao conferir o arquivo e executar a referência, verificamos
que isso violava o contrato. O gerador foi então restaurado a partir do
enunciado e a execução passou a produzir BFS custo 55, UCS custo 34 e BFS com
22 passos.

## A.4 O que só soubemos após executar

Depois de rodar o código, soubemos os valores concretos de expansão
(BFS 116, UCS 112 e A* Manhattan 93) e os parâmetros do sensor para a
matrícula de aferição; esses números não podem ser obtidos apenas lendo uma
explicação genérica.
