"""Sistema especialista explicável com encadeamento para trás."""
REGRAS=[({"solo_seco","temperatura_alta"},"irrigar","Solo seco e temperatura alta indicam irrigação."),({"praga"},"aplicar_controle","Praga observada requer controle."),({"chuva_prevista"},"adiar_irrigacao","Chuva prevista: adiar irrigação."),({"folhas_amareladas","solo_seco"},"adubar","Folhas amareladas e solo seco sugerem adubação.")]
def encadeamento_para_tras(objetivo,fatos,regras=None,caminho=None):
    regras=REGRAS if regras is None else regras;caminho=[] if caminho is None else caminho
    if objetivo in fatos:return True
    for prem,con,exp in regras:
        if con==objetivo and all(encadeamento_para_tras(p,fatos,regras,caminho) for p in prem):caminho.append(exp);return True
    return False
def recomendar(fatos):
    out=[]
    for _,con,exp in REGRAS:
        c=[]
        if encadeamento_para_tras(con,set(fatos),caminho=c):out.append({"acao":con,"explicacao":c[0] if c else exp})
    return out