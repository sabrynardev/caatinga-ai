"""Cálculos bayesianos sem dependências externas."""
def bayes(prior,verossimilhanca,evidencia):
    if evidencia==0:raise ValueError("A evidência não pode ser zero")
    return prior*verossimilhanca/evidencia
def probabilidade_praga(prior_praga=.2,sensibilidade=.85,falso_positivo=.1):
    e=prior_praga*sensibilidade+(1-prior_praga)*falso_positivo
    return {"evidencia":e,"posterior":bayes(prior_praga,sensibilidade,e)}
def teorema_bayes(prior,p_e_dado_h,p_e_dado_nao_h):
    return bayes(prior,p_e_dado_h,prior*p_e_dado_h+(1-prior)*p_e_dado_nao_h)