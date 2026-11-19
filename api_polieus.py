r"""Polieus | API dos modelos de Inteligência Artificial
Global Solution FIAP 2026/2 · Artificial Intelligence & Chatbot · 1TDSPH

INÍCIO RÁPIDO | Execute na pasta do ZIP extraído

Antes de começar no Windows
   A entrega usa Python 3.12 para reproduzir o ambiente dos modelos. O 3.14 pode
   continuar instalado. Abra a pasta que contém api_polieus.py e requirements.txt.
   Se aparecer bash ou MINGW64, escolha o Prompt de Comando (cmd) para seguir
   os exemplos Windows abaixo, que usam barras invertidas.
   VS Code: Terminal → seta ao lado de + → Command Prompt (Prompt de Comando).
   PyCharm: File → Settings → Tools → Terminal → Shell path → cmd.exe.
   Confirme e abra uma nova aba de terminal.

   Confira a versão:
       py -3.12 --version
   Se o Python 3.12 estiver ausente, instale:
       winget install --id Python.Python.3.12 --exact
   Após instalar, reabra o editor e o cmd e repita a verificação da versão.

1. Quando aparecer Python 3.12.x, prepare o ambiente uma vez.
   Windows (cmd):
       py -3.12 -m venv .venv
       .venv\Scripts\python -m pip install -r requirements.txt
   Linux ou macOS: abra o terminal na pasta extraída.
       python3.12 -m venv .venv
       .venv/bin/python -m pip install -r requirements.txt
   O pip instala todas as bibliotecas nas versões do projeto em um só comando.

2. Inicie o Flask sempre que quiser usar os modelos.
   Windows:       .venv\Scripts\python api_polieus.py
   Linux/macOS:   .venv/bin/python api_polieus.py

3. Mantenha o terminal aberto e acesse http://127.0.0.1:5000/demonstracao
   Clique em “Estimar duração” ou “Consultar perfil”. Para sair, use Ctrl+C.
   O guia explica os exemplos na seção 4.3 e os testes opcionais na seção 4.4.

Equipe Politech
    Isabelle Ferreira Neri Feitoza — RM 573507
    Marina Fernandes Gomes Mesquita — RM 571265
    Milena Silva Conegin — RM 568923
    Murilo Almeida Rodrigues de Souza — RM 573977
    Henrique Bonachela de Carvalho Carabante — RM 573620

O Polieus foi criado para que moradores possam registrar problemas urbanos e
acompanhar o atendimento, e para que gestores possam examinar essas demandas.
Uma solicitação de tapa-buraco exemplifica duas escalas de análise. Para o
chamado individual, o modelo de regressão estima quantos dias podem decorrer
até sua finalização administrativa. Para o distrito inteiro, o modelo de
agrupamento identifica que combinação de serviços aparece nos pedidos do mês.
A base de estudo é o SP156 da Prefeitura de São Paulo. A cobertura dos modelos
abrange oito serviços na capital. Uma previsão de duração é uma estimativa
histórica. Confirmar que uma obra foi concluída exige evidência de execução.

Como esta API funciona
    O site ou um programa de testes envia uma solicitação a um endereço
    chamado rota. O Flask lê os campos enviados em JSON, formato que associa
    nomes a valores. O Python verifica os campos, consulta o modelo treinado
    nos notebooks e o Flask devolve a resposta em JSON. Para experimentar
    esta entrega, basta usar os modelos e a tabela que acompanham o ZIP.

Bibliotecas instaladas pelo pip
    Flask recebe as consultas. pandas organiza os campos em tabelas e NumPy
    representa valores ausentes. joblib abre os modelos gravados pelos notebooks.
    scikit-learn executa as previsões e usa operações científicas da SciPy.
    Matplotlib gera os gráficos dos notebooks e integra o ambiente do projeto.
    As versões exatas das sete bibliotecas estão em requirements.txt. Módulos
    como json, datetime e pathlib já acompanham o Python.

"""

from datetime import date
import json
import math
import os
from pathlib import Path
import re
from unicodedata import normalize

from flask import Flask, jsonify, render_template, request
import joblib
import numpy as np
import pandas as pd


# O Flask recebe as consultas. Os pequenos formulários JSON cabem em 32 KiB.
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 32_768

# Usar a pasta deste arquivo permite localizar os dados mesmo quando o servidor
# é iniciado de outra pasta. Os modelos são carregados uma vez na inicialização.
raiz = Path(__file__).resolve().parent
modelos = raiz / "modelos_polieus"
reg = joblib.load(modelos / "modelo_duracao_administrativa.joblib")
agr = joblib.load(modelos / "modelo_perfis_territoriais.joblib")

# A ficha guarda os nomes e a ordem das colunas que o modelo aprendeu a ler.
# No catálogo mostramos o nome municipal do serviço. Na tabela usada pelo
# modelo, cada coluna começa com "proporcao_" e guarda a fração daquele serviço.
ficha = json.loads((modelos / "ficha_perfis_territoriais.json").read_text(encoding="utf-8"))
campos = ficha["entradas"]
servicos = [campo.removeprefix("proporcao_") for campo in campos]
historico = pd.read_csv(raiz / "dados_polieus" / "02_perfis_por_distrito_e_mes.csv")


def padronizar(texto):
    """Permite procurar, por exemplo, ‘Sacomã’ e ‘SACOMA’ no mesmo catálogo."""
    if not isinstance(texto, str):
        return ""
    sem_acentos = normalize("NFKD", texto.strip()).encode("ascii", "ignore")
    return sem_acentos.decode().upper()


# A chave facilita a busca. O valor mantém a grafia usada no treinamento.
distritos = {padronizar(nome): nome for nome in historico.distrito.unique()}


@app.get("/demonstracao")
def demonstracao():
    """Abre a página que consulta o catálogo e envia os pedidos aos modelos."""
    return render_template("demonstracao.html")


@app.get("/")
def catalogo():
    """GET consulta as opções que podem preencher o formulário do site."""
    return jsonify(
        municipio="São Paulo", uf="SP", servicos=servicos,
        distritos=sorted(distritos.values()), meses=sorted(historico.mes.unique()),
        rotas=["/regressao", "/agrupamento"],
    )


def ler_pedido():
    """As duas análises recebem um objeto JSON e cobrem a capital paulista."""
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        raise ValueError("Envie um objeto JSON com Content-Type application/json.")
    if padronizar(dados.get("municipio")) != "SAO PAULO" or padronizar(dados.get("uf")) != "SP":
        raise ValueError("Cobertura disponível para o município de São Paulo, SP.")
    return dados


@app.errorhandler(ValueError)
def entrada_invalida(erro):
    # O site pode exibir a mensagem do campo "erro" para orientar a correção.
    return jsonify(erro=str(erro)), 422


def dia_da_semana(abertura):
    """Converte a data no dado usado pelo modelo: segunda vale '0', domingo '6'."""
    if not isinstance(abertura, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", abertura):
        raise ValueError("Use a data de abertura no formato AAAA-MM-DD.")
    try:
        data = date.fromisoformat(abertura)
    except ValueError:
        # Uma data pode ter a escrita correta e indicar um dia inexistente.
        raise ValueError("Data de abertura inexistente.") from None
    return str(data.weekday())


@app.post("/regressao")
def estimar():
    """Recebe um chamado e estima sua duração a partir de dados da abertura."""
    dados = ler_pedido()
    if dados.get("servico") not in servicos:
        raise ValueError("Escolha um serviço do catálogo.")
    dia = dia_da_semana(dados.get("abertura"))

    # Um distrito ausente é aceito pelo modelo. Se a pessoa informar um nome,
    # conferimos o catálogo para que um erro de digitação possa ser corrigido.
    nome = dados.get("distrito")
    distrito = distritos.get(padronizar(nome))
    if nome is not None and distrito is None:
        raise ValueError("Selecione um distrito do catálogo ou envie null.")

    # O modelo recebe uma tabela com uma linha. O primeiro valor da previsão
    # corresponde a esse chamado. A resposta expressa o tempo em dias corridos.
    entrada = pd.DataFrame([{
        "servico": dados["servico"],
        "distrito": np.nan if distrito is None else distrito,
        "dia_semana": dia,
    }])
    dias = float(reg.predict(entrada)[0])
    return jsonify(
        dias_estimados=round(dias, 2),
        significado="Duração administrativa histórica estimada em dias corridos.",
    )


def perfil_para_agrupar(dados, distrito, mes):
    """Obtém as oito participações, o total de chamados e a origem da composição."""
    if "proporcoes" not in dados:
        # Na consulta histórica, uma linha reúne todos os chamados do distrito
        # naquele mês que pertencem aos oito serviços selecionados.
        perfil = historico.loc[(historico.distrito == distrito) & (historico.mes == mes)]
        if perfil.empty:
            raise ValueError("Sem perfil histórico para esse distrito e mês.")
        return perfil[campos], int(perfil.total_solicitacoes.iloc[0]), "Histórico SP156"

    # O site também pode enviar sua própria contagem e composição. Por exemplo,
    # 5 pedidos em um total de 20 representam uma proporção de 0,25. Montamos
    # as colunas na ordem do treino, independentemente da ordem do JSON recebido.
    proporcoes = dados["proporcoes"]
    if not isinstance(proporcoes, dict) or set(proporcoes) != set(servicos):
        raise ValueError("Envie as oito proporções, identificadas pelos serviços do catálogo.")
    valores = [proporcoes[servico] for servico in servicos]
    for valor in valores:
        if type(valor) not in (int, float) or not 0 <= valor <= 1:
            raise ValueError("As oito proporções devem estar entre 0 e 1 e somar 1.")
    # A pequena tolerância acomoda o arredondamento da aritmética decimal.
    if not math.isclose(sum(valores), 1, abs_tol=1e-8):
        raise ValueError("As oito proporções devem estar entre 0 e 1 e somar 1.")
    total = dados.get("total_solicitacoes")
    if type(total) is not int or total <= 0:
        raise ValueError("Informe um total inteiro positivo de solicitações.")
    return pd.DataFrame([valores], columns=campos), total, "Composição informada pelo sistema solicitante"


@app.post("/agrupamento")
def agrupar():
    """Identifica qual grupo aprendido apresenta composição próxima à informada."""
    dados = ler_pedido()
    distrito = distritos.get(padronizar(dados.get("distrito")))
    mes = dados.get("mes")
    if distrito is None or not isinstance(mes, str) or not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", mes):
        raise ValueError("Informe distrito do catálogo e mês AAAA-MM.")

    entrada, total, origem = perfil_para_agrupar(dados, distrito, mes)
    grupo = int(agr.predict(entrada)[0])
    # O número do grupo é um identificador. Os percentuais médios descrevem os
    # distritos-mês que formaram o grupo no treino e dão significado a esse número.
    return jsonify(
        grupo=grupo, distrito=distrito, mes=mes, total_solicitacoes=total, origem=origem,
        perfil_medio_percentual=ficha["perfis_medios_percentuais"][str(grupo)],
    )


@app.after_request
def permitir_react(resposta):
    """Autoriza o navegador a ler a resposta a partir das origens locais do site."""
    # Em desenvolvimento, React e Flask usam portas diferentes. Os cabeçalhos
    # CORS indicam ao navegador quais origens, métodos e cabeçalhos são aceitos.
    padrao = "http://localhost:5173,http://127.0.0.1:5173"
    origens = os.getenv("POLIEUS_ORIGENS", padrao).split(",")
    origem = request.headers.get("Origin")
    if origem in origens:
        resposta.headers["Access-Control-Allow-Origin"] = origem
        resposta.headers["Access-Control-Allow-Headers"] = "Content-Type"
        resposta.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        resposta.vary.add("Origin")
    return resposta


# Ao executar este arquivo, iniciamos o servidor. Ao importá-lo pelo script de
# testes, o Flask recebe as mesmas consultas internamente, sem ocupar a porta.
if __name__ == "__main__":
    app.run(port=5000)
