"""Subida de encosta e têmpera simulada (K=15, 30 execuções)."""
import math, random
K=15
def qualidade(x,alvo=.7):return -abs(x-alvo)
def subida_encosta(inicial=None,passos=100,rng=None):
    rng=rng or random.Random();x=rng.random() if inicial is None else inicial
    for i in range(passos):
        y=max(0,min(1,max((x+rng.uniform(-.1,.1) for _ in range(K)),key=qualidade)))
        if qualidade(y)<=qualidade(x):break
        x=y
    return {"solucao":x,"qualidade":qualidade(x),"iteracoes":i+1}
def tempera_simulada(inicial=None,passos=1000,temperatura=1.,resfriamento=.995,rng=None):
    rng=rng or random.Random();x=rng.random() if inicial is None else inicial;melhor=x
    for i in range(passos):
        t=max(1e-9,temperatura*resfriamento**i);y=max(0,min(1,x+rng.uniform(-.15,.15)));delta=qualidade(y)-qualidade(x)
        if delta>0 or rng.random()<math.exp(delta/t):x=y
        if qualidade(x)>qualidade(melhor):melhor=x
    return {"solucao":melhor,"qualidade":qualidade(melhor),"iteracoes":passos}
def executar_experimentos(exec=30,seed=0):
    return [{"execucao":i+1,"subida":subida_encosta(rng=random.Random(seed+i))["qualidade"],"tempera":tempera_simulada(rng=random.Random(seed+i))["qualidade"]} for i in range(exec)]