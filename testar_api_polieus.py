"""Polieus · verificação automática opcional da API Flask.

Para usar os dois modelos pelo navegador, siga as seções 4.2 e 4.3 do guia.
Este script serve a quem deseja repetir os testes técnicos da seção 4.4.
Ele envia exemplos à aplicação em memória, sem abrir uma porta de rede.
"""
from api_polieus import app, agr, reg, historico, campos, servicos
import pandas as pd

def testar():
    # O cliente simula as requisições que chegariam do navegador.
    cliente = app.test_client()
    cidade = dict(municipio="São Paulo", uf="SP")
    # Uma solicitação individual alimenta a regressão. Um distrito e um mês identificam o perfil histórico.
    pedido = dict(**cidade, distrito="Sacomã", servico="Tapa-buraco", abertura="2026-09-01")
    perfil = dict(**cidade, distrito="Água Rasa", mes="2026-08")
    # Esta linha do histórico permite conferir a previsão diretamente com o modelo salvo.
    exemplo = historico[(historico.distrito == "AGUA RASA") & (historico.mes == perfil["mes"])]
    entrada = pd.DataFrame([dict(servico="Tapa-buraco", distrito="SACOMA", dia_semana="1")])
    # Também testamos o envio das oito proporções por um sistema externo.
    completo = dict(**perfil, total_solicitacoes=int(exemplo.total_solicitacoes.iloc[0]),
                    proporcoes=dict(zip(servicos, exemplo[campos].iloc[0])))
    # Cada caso define a rota, os dados e a resposta esperada: 200 para sucesso ou 422 para entrada inválida.
    for rota, dados, esperado in [
        ("/regressao", pedido, 200), ("/agrupamento", perfil, 200), ("/agrupamento", completo, 200),
        ("/regressao", dict(pedido, distrito=None), 200),
        ("/regressao", dict(pedido, municipio="Campinas"), 422),
        ("/regressao", dict(pedido, servico="Iluminação"), 422),
        ("/regressao", dict(pedido, abertura="2026-02-30"), 422),
        ("/agrupamento", dict(perfil, mes="2026-01"), 422),
        ("/agrupamento", dict(completo, proporcoes={}), 422),
    ]:
        resposta = cliente.post(rota, json=dados)
        assert resposta.status_code == esperado, resposta.get_json()
        # Conferimos os valores previstos para detectar diferenças entre a API e os modelos.
        if dados == pedido:
            assert resposta.json["dias_estimados"] == round(float(reg.predict(entrada)[0]), 2)
        if rota == "/agrupamento" and esperado == 200:
            assert resposta.json["grupo"] == int(agr.predict(exemplo[campos])[0])
        print(rota, resposta.status_code, resposta.json)
    # Verificamos a permissão de acesso pelo site local e os oito serviços do catálogo.
    pre = cliente.options("/regressao", headers={"Origin":"http://localhost:5173"})
    assert pre.headers["Access-Control-Allow-Origin"] == "http://localhost:5173"
    assert len(cliente.get("/").json["servicos"]) == 8
    print("Verificações concluídas.")

if __name__ == "__main__":
    testar()
