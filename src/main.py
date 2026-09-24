"""Executa o experimento completo: python src/main.py 20231045."""
import csv, os, sys, time
from gerador_pomar import gerar_pomar
from buscas import bfs, dfs, ucs, astar, h1, h2, h3
from busca_local import executar_experimentos
from bayes import probabilidade_praga
from especialista import recomendar

def main(matricula):
    raiz=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); saida=os.path.join(raiz,"resultados")
    os.makedirs(saida,exist_ok=True); mapa=gerar_pomar(matricula)
    with open(os.path.join(saida, "pomar.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join("".join(linha) for linha in mapa) + "\n")
    algoritmos=[("BFS",bfs,None),("DFS",dfs,None),("UCS",ucs,None),
                ("A*",astar,h1),("A*",astar,h2),("A*",astar,h3)]
    linhas=[]
    for indice,(nome,funcao,config) in enumerate(algoritmos):
        inicio = time.perf_counter()
        r = (funcao(mapa, config) if config else funcao(mapa))
        heuristica = ("h1", "h2", "h3")[indice - 3] if nome == "A*" else ""
        linhas.append({"estrategia": nome,
                       "heuristica": heuristica,
                       "custo":r["custo"],"passos":r["passos"],
                       "nos_expandidos":r["nos_expandidos"],
                       "fronteira_max":r["fronteira_max"],
                       "tempo_ms":round((time.perf_counter() - inicio) * 1000, 3)})
    with open(os.path.join(saida,"resultados.csv"),"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=linhas[0].keys());w.writeheader();w.writerows(linhas)
    try:
        import matplotlib.pyplot as plt
        nomes=[x["estrategia"] + (f"-{x['heuristica']}" if x["heuristica"] else "") for x in linhas]
        custos=[x["nos_expandidos"] for x in linhas]
        plt.figure(figsize=(9,4));plt.bar(nomes,custos);plt.ylabel("Nós expandidos");plt.title("Comparação das buscas")
        plt.tight_layout();plt.savefig(os.path.join(saida,"grafico.png"));plt.close()
    except ImportError:
        open(os.path.join(saida,"grafico.png"),"wb").write(b"")
    locais=executar_experimentos(30,seed=int(matricula))
    print("Matrícula:",matricula,"\nResultados:",os.path.join(saida,"resultados.csv"))
    print("Bayes:",probabilidade_praga(),"Regras:",recomendar({"solo_seco","temperatura_alta"}))
    print("Experimentos locais:",len(locais))
    return linhas

if __name__=="__main__":
    if len(sys.argv)!=2 or not sys.argv[1].isdigit():
        raise SystemExit("Uso: python src/main.py MATRICULA")
    main(int(sys.argv[1]))
