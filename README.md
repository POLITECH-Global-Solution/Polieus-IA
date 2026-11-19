
<p align="center">
  <img src="https://raw.githubusercontent.com/POLITECH-Global-Solution/Polieus/main/public/favicons/logo_polieus.png" width="180" alt="Logo do Polieus">
</p>

<h1 align="center">POLIEUS — Inteligência Artificial & Chatbot</h1>

<p align="center">
  <strong>Inteligência Artificial aplicada à análise de demandas urbanas, acessibilidade e participação cidadã.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white" alt="scikit-learn">
  <img src="https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white" alt="NumPy">
  <img src="https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white" alt="Jupyter">
  <img src="https://img.shields.io/badge/Google_Colab-F9AB00?style=flat-square&logo=googlecolab&logoColor=white" alt="Google Colab">
</p>

<p align="center">
  <strong>Global Solution 2026/2 — CitizenTech</strong><br>
  FIAP | Análise e Desenvolvimento de Sistemas | Equipe Politech | Turma 1TDSPH
</p>

<p align="center">
  <a href="https://polieus.vercel.app"><strong>Acessar o Polieus na Vercel</strong></a>
</p>

---

## Descrição do Projeto

O **Polieus** é uma plataforma CitizenTech que busca aproximar cidadãos e gestores públicos, facilitando o registro, o acompanhamento e a análise de problemas urbanos.

O projeto propõe transformar demandas da população em informações organizadas que possam apoiar decisões relacionadas à infraestrutura, acessibilidade e transparência pública.

O município-piloto do MVP é **São Paulo (capital)**, com foco inicial em:

- **Acessibilidade urbana:** calçadas danificadas, obstáculos e dificuldades de circulação;
- **Pavimentação:** buracos, rachaduras e problemas nas vias públicas.

Este repositório apresenta o módulo de **Artificial Intelligence & Chatbot**, responsável pelo estudo e pela implementação de modelos de machine learning aplicados a dados públicos de solicitações urbanas.

A implementação contempla dois modelos principais:

1. **Agrupamento territorial:** identifica perfis semelhantes de solicitações entre distritos e meses.
2. **Regressão:** estima a duração administrativa de solicitações com base em características disponíveis no momento da abertura.

Os modelos foram desenvolvidos com dados históricos do **SP156**, serviço de atendimento da Prefeitura de São Paulo.

---

## Objetivo

Investigar como técnicas de inteligência artificial podem apoiar a compreensão de demandas urbanas e fornecer informações úteis à gestão pública.

Entre os objetivos estão:

- Explorar dados reais de solicitações registradas no SP156;
- Identificar padrões territoriais de atendimento;
- Comparar a composição das demandas por distrito e período;
- Estimar o número de dias até a finalização administrativa de chamados;
- Avaliar o desempenho e as limitações dos modelos;
- Disponibilizar os modelos treinados por meio de uma API REST;
- Criar uma interface demonstrativa para facilitar a apresentação dos resultados;
- Apoiar análises que possam contribuir para a transparência e a participação cidadã.

As previsões são experimentais e não substituem a avaliação humana nem representam garantias de prazo ou de execução de serviços.

---

## Tecnologias Utilizadas

### Python

Linguagem principal utilizada para preparação dos dados, análise exploratória, treinamento dos modelos e desenvolvimento da API.

### Pandas e NumPy

Bibliotecas utilizadas para manipulação de tabelas, limpeza de registros, cálculos estatísticos e preparação dos atributos.

### scikit-learn

Biblioteca utilizada para implementação, treinamento, comparação e avaliação dos modelos de machine learning.

### Matplotlib

Biblioteca utilizada na construção de gráficos e visualizações para a análise exploratória dos dados.

### Jupyter Notebook e Google Colab

Ambientes utilizados para organizar os experimentos, documentar as etapas e executar os notebooks.

### Joblib

Ferramenta utilizada para exportar e carregar os modelos treinados, permitindo sua reutilização na API sem repetir o treinamento.

### Flask

Framework Python utilizado para desenvolver a API REST responsável por disponibilizar as operações de regressão e agrupamento.

---

## Base de Dados — SP156

Os dados utilizados neste estudo são provenientes do **Portal de Dados Abertos da Prefeitura de São Paulo**, com registros históricos de solicitações realizadas pelo canal SP156.

O projeto utiliza dados dos seguintes períodos:

| Período | Abrangência |
|---|---|
| 4º trimestre de 2025 | Outubro a dezembro |
| 3º trimestre de 2026 | Julho a setembro |

Foram selecionados oito tipos de serviço relacionados à infraestrutura e à acessibilidade urbana:

1. Tapa-buraco;
2. Tapa-buraco em faixa exclusiva ou corredor de ônibus;
3. Avaliação de obstáculos na calçada;
4. Manutenção de calçadas públicas;
5. Denúncia de calçadas particulares danificadas ou inexistentes;
6. Solicitação de rebaixamento de guias;
7. Limpeza de bueiros e estruturas de drenagem;
8. Manutenção de equipamentos em pontos de ônibus.

### Fontes Originais

Os arquivos CSV originais podem ser obtidos nos seguintes endereços:

- [SP156 — 4º trimestre de 2025](https://dados.prefeitura.sp.gov.br/dataset/0aecfa2b-aa3a-40d4-8183-0d4351b7fd0a/resource/d3a98097-8128-45d4-b8fe-21874b81c971/download/arquivo-final-4-trim-25.csv)
- [SP156 — 3º trimestre de 2026](https://dados.prefeitura.sp.gov.br/dataset/0aecfa2b-aa3a-40d4-8183-0d4351b7fd0a/resource/f67fcc12-8da4-485f-92a3-d2af40cc771e/download/arquivo-final-3-trim-26.csv)

**Observação:** os CSVs originais não estão incluídos neste repositório devido ao seu tamanho. Os dados derivados necessários aos experimentos e à API estão disponíveis em `dados_polieus/`.

---

## Modelos de Inteligência Artificial

### 1. Agrupamento de Perfis Territoriais — K-Means

O primeiro modelo utiliza **aprendizagem não supervisionada**, por meio do algoritmo K-Means.

O objetivo é identificar grupos de distritos e meses que apresentam composições semelhantes de solicitações urbanas.

**Unidade de análise:** distrito e mês.

Os atributos representam a participação proporcional dos oito serviços selecionados no total de solicitações daquele distrito durante o período.

#### Funcionamento

1. Os registros são agrupados por distrito e mês;
2. São calculadas as proporções dos oito serviços;
3. O algoritmo K-Means identifica perfis semelhantes;
4. Cada observação recebe a identificação de um grupo;
5. As métricas são utilizadas para avaliar a separação e a estabilidade dos agrupamentos.

**Configuração selecionada:** `K = 2`.

#### Resultados

| Métrica | Resultado |
|---|---:|
| Quantidade de grupos | 2 |
| Silhueta | 0,283 |
| Davies–Bouldin | 1,613 |
| ARI em comparação com representação simplificada | 0,913 |

A silhueta indica separação relativamente limitada entre os grupos. O ARI elevado indica concordância com a divisão construída a partir de uma representação mais simples.

Os grupos representam **perfis de composição de demandas**, e não níveis automáticos de urgência ou prioridade.

**Notebook:** [`02_Agrupar_Perfis_Distrito_Mes.ipynb`](./02_Agrupar_Perfis_Distrito_Mes.ipynb)

**Modelo exportado:** `modelos_polieus/modelo_perfis_territoriais.joblib`

---

### 2. Estimativa de Duração Administrativa — Regressão

O segundo modelo utiliza **aprendizagem supervisionada**, buscando estimar o número de dias corridos entre a abertura e a finalização administrativa de um chamado.

O modelo selecionado utiliza uma abordagem de **Gradient Boosting**.

#### Atributos de entrada

- Serviço solicitado;
- Distrito, quando disponível;
- Dia da semana da abertura do chamado.

#### Saída

Estimativa da duração administrativa, expressa em dias corridos.

#### Resultados no conjunto de teste

| Métrica | Resultado |
|---|---:|
| MAE | 4,31 dias |
| RMSE | 6,74 dias |
| R² | -0,114 |

O modelo também foi comparado a uma referência baseada na mediana histórica por serviço.

**Interpretação:** o modelo apresentou melhora em MAE e RMSE em relação à referência utilizada, mas seu R² negativo indica capacidade preditiva limitada no conjunto de teste.

Os resultados não devem ser interpretados como uma previsão garantida de atendimento.

**Notebook:** [`03_Estimar_Dias_ate_Finalizacao.ipynb`](./03_Estimar_Dias_ate_Finalizacao.ipynb)

**Modelo exportado:** `modelos_polieus/modelo_duracao_administrativa.joblib`

---

## API REST — Flask

O projeto disponibiliza uma API REST desenvolvida com Flask para consumir os modelos treinados.

A API carrega os arquivos `.joblib` e utiliza os modelos para processar novas solicitações.

### Endpoints Implementados

| Método | Endpoint | Funcionalidade |
|---|---|---|
| `GET` | `/` | Consulta o catálogo de serviços e informações disponíveis |
| `GET` | `/demonstracao` | Abre a interface demonstrativa no navegador |
| `POST` | `/regressao` | Estima a duração administrativa de uma solicitação |
| `POST` | `/agrupamento` | Identifica o grupo de um perfil territorial |

As operações utilizam JSON para comunicação e retornam respostas de sucesso ou mensagens de erro de validação.

### Exemplo — Regressão

Requisição:

```json
{
  "municipio": "São Paulo",
  "uf": "SP",
  "distrito": "Sacomã",
  "servico": "Tapa-buraco",
  "abertura": "2026-09-01"
}
```

Exemplo de resposta registrada nos testes:

```json
{
  "dias_estimados": 5.63,
  "significado": "Duração administrativa histórica estimada em dias corridos."
}
```

O resultado acima é um exemplo reproduzido com os modelos exportados, não uma garantia de duração para uma solicitação real.

### Interface Demonstrativa

O arquivo `templates/demonstracao.html` apresenta formulários em português para testar os dois modelos pelo navegador.

Após iniciar a aplicação Flask, acesse:

**http://localhost:5000/demonstracao**

A interface permite experimentar a API sem utilizar ferramentas externas como Postman ou Insomnia.

---

## Estrutura do Repositório

```text
Polieus-IA/
├── consulta_excel/
│   ├── 01_Consulta_Excel_Cobertura_por_Servico_e_Trimestre.xlsx
│   ├── 02_Consulta_Excel_Perfis_por_Distrito_e_Mes.xlsx
│   └── 03_Consulta_Excel_Solicitacoes_com_Duracao_em_Dias.xlsx
│
├── dados_polieus/
│   ├── 01_cobertura_por_servico_e_trimestre.csv
│   ├── 02_perfis_por_distrito_e_mes.csv
│   └── 03_solicitacoes_com_duracao_em_dias.csv
│
├── modelos_polieus/
│   ├── modelo_duracao_administrativa.joblib
│   ├── modelo_perfis_territoriais.joblib
│   ├── ficha_duracao_administrativa.json
│   └── ficha_perfis_territoriais.json
│
├── static/
│   └── polieus.png
│
├── templates/
│   └── demonstracao.html
│
├── 00_LEIA_PRIMEIRO_Guia_do_Polieus.txt
├── 01_Preparar_Dados_SP156.ipynb
├── 02_Agrupar_Perfis_Distrito_Mes.ipynb
├── 03_Estimar_Dias_ate_Finalizacao.ipynb
├── api_polieus.py
├── testar_api_polieus.py
├── Resultados_dos_testes_da_API.txt
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Como Executar o Projeto

### Pré-requisitos

- Python 3.12;
- Git;
- Terminal ou editor de código;
- Bibliotecas listadas em `requirements.txt`.

### 1. Clonar o Repositório

```bash
git clone https://github.com/POLITECH-Global-Solution/Polieus-IA.git
cd Polieus-IA
```

### 2. Criar o Ambiente Virtual

No Windows, utilizando o Prompt de Comando:

```cmd
py -3.12 -m venv .venv
```

### 3. Instalar as Dependências

```cmd
.venv\Scripts\python -m pip install -r requirements.txt
```

### 4. Executar os Testes da API

```cmd
.venv\Scripts\python testar_api_polieus.py
```

O script utiliza o cliente de testes do Flask para verificar respostas válidas, entradas inválidas e resultados dos modelos exportados.

### 5. Iniciar a API Flask

```cmd
.venv\Scripts\python api_polieus.py
```

A aplicação será iniciada localmente na porta `5000`.

Abra no navegador:

**http://localhost:5000/demonstracao**

### 6. Executar os Notebooks

Os notebooks podem ser executados no Jupyter ou no Google Colab, seguindo esta sequência:

| Notebook | Finalidade |
|---|---|
| `01_Preparar_Dados_SP156.ipynb` | Preparar e validar os dados originais |
| `02_Agrupar_Perfis_Distrito_Mes.ipynb` | Treinar e avaliar o agrupamento territorial |
| `03_Estimar_Dias_ate_Finalizacao.ipynb` | Treinar e avaliar a regressão da duração administrativa |

Os notebooks 02 e 03 também podem utilizar diretamente os dados preparados disponíveis no repositório.

Para reproduzir integralmente o notebook 01, é necessário obter os dois arquivos CSV originais do SP156.

Instruções detalhadas estão disponíveis no arquivo:

**[`00_LEIA_PRIMEIRO_Guia_do_Polieus.txt`](./00_LEIA_PRIMEIRO_Guia_do_Polieus.txt)**

---

## Testes e Validação

O projeto inclui:

- Notebooks com treinamento e avaliação;
- Modelos serializados e fichas técnicas em JSON;
- Testes automatizados da API Flask;
- Testes de requisições válidas e inválidas;
- Verificação de respostas de regressão e agrupamento;
- Registro dos resultados obtidos pela equipe.

**[Consultar resultados dos testes da API](./Resultados_dos_testes_da_API.txt)**

### Limitações Conhecidas

- O agrupamento identifica similaridades estatísticas, mas não determina automaticamente a prioridade de atendimento.
- A regressão apresenta desempenho limitado e não substitui estimativas operacionais oficiais.
- O estudo está restrito aos serviços e períodos selecionados do município de São Paulo.
- A finalização administrativa de um chamado não comprova necessariamente a conclusão física de uma intervenção urbana.
- Os modelos e a API são componentes demonstrativos e não representam, por si só, uma integração concluída com o front-end ou com o banco de dados Java do Polieus.

---

## Relação com o Ecossistema Polieus

O módulo de IA integra o conjunto de projetos acadêmicos desenvolvidos pela equipe Politech para a Global Solution 2026/2.

| Recurso | Link |
|---|---|
| Plataforma Web | [polieus.vercel.app](https://polieus.vercel.app) |
| Front-end React | [POLITECH-Global-Solution/Polieus](https://github.com/POLITECH-Global-Solution/Polieus) |
| Banco de Dados Oracle | [POLITECH-Global-Solution/data-base-polieus](https://github.com/POLITECH-Global-Solution/data-base-polieus) |
| Inteligência Artificial | [POLITECH-Global-Solution/Polieus-IA](https://github.com/POLITECH-Global-Solution/Polieus-IA) |

A API Flask deste repositório pode servir de base para futuras integrações, mas sua comunicação com os demais módulos deve ser implementada e validada separadamente.

---

## Impacto Social

O Polieus busca contribuir para os seguintes Objetivos de Desenvolvimento Sustentável:

- **ODS 10 — Redução das Desigualdades:** dar visibilidade a problemas que afetam pessoas com deficiência ou mobilidade reduzida;
- **ODS 11 — Cidades e Comunidades Sustentáveis:** apoiar a compreensão de demandas de infraestrutura urbana;
- **ODS 16 — Paz, Justiça e Instituições Eficazes:** incentivar transparência, participação cidadã e decisões apoiadas por informações.

A inteligência artificial é utilizada como ferramenta de apoio à análise, preservando a importância da supervisão humana nas decisões públicas.

---

## 👥 Integrantes & Autores

Projeto desenvolvido pela **Equipe Politech**, turma **1TDSPH**, para a Global Solution 2026/2 da FIAP.

- <img src="https://raw.githubusercontent.com/POLITECH-Global-Solution/Polieus/main/src/img/fotoHenrique.jpeg" width="120px" alt="Foto de Henrique Bonachela"><br>
  **Henrique Bonachela de Carvalho Carabante** — RM **573620** (Inteligência Artificial) — Turma: **1TDSPH**  
  [LinkedIn](https://www.linkedin.com/in/henrique-bonachela-de-carvalho-carabante-260b86338/) | [GitHub](https://github.com/henriquebonachela)

- <img src="https://raw.githubusercontent.com/POLITECH-Global-Solution/Polieus/main/src/img/fotoIsa.png" width="120px" alt="Foto de Isabelle Ferreira"><br>
  **Isabelle Ferreira Neri Feitoza** — RM **573507** (Engenharia de Dados) — Turma: **1TDSPH**  
  [LinkedIn](https://www.linkedin.com/in/isabelle-ferreira-8844593ab) | [GitHub](https://github.com/isabelleferreiraa)

- <img src="https://raw.githubusercontent.com/POLITECH-Global-Solution/Polieus/main/src/img/fotoMilena.png" width="120px" alt="Foto de Milena Conegin"><br>
  **Milena Silva Conegin** — RM **568923** (Back-end Java) — Turma: **1TDSPH**  
  [LinkedIn](https://www.linkedin.com/in/milena-conegin-996b22269) | [GitHub](https://github.com/MilenaConegin)

- <img src="https://raw.githubusercontent.com/POLITECH-Global-Solution/Polieus/main/src/img/fotoMarina.jpg" width="120px" alt="Foto de Marina Fernandes"><br>
  **Marina Fernandes Gomes Mesquita** — RM **571265** (Front-end) — Turma: **1TDSPH**  
  [LinkedIn](https://www.linkedin.com/in/marifernandesgm-58460a40a) | [GitHub](https://github.com/marifernandesgm)

- <img src="https://raw.githubusercontent.com/POLITECH-Global-Solution/Polieus/main/src/img/fotoMurilo.jpeg" width="120px" alt="Foto de Murilo Almeida"><br>
  **Murilo Almeida Rodrigues de Souza** — RM **573977** (Back-end Python) — Turma: **1TDSPH**  
  [LinkedIn](https://www.linkedin.com/in/murilo-a-souza/) | [GitHub](https://github.com/murilo-a-souza)

---

## 📞 Contato

Para dúvidas, sugestões ou contribuições, utilize a seção de Issues deste repositório.

- [Abrir uma Issue](https://github.com/POLITECH-Global-Solution/Polieus-IA/issues)
- [Organização Politech](https://github.com/POLITECH-Global-Solution)

---

<p align="center">
  <strong>POLIEUS — Equipe Politech</strong><br>
  FIAP | Global Solution 2026/2 | CitizenTech | Turma 1TDSPH<br>
  <em>Tecnologia que conecta pessoas, cidades e decisões.</em>
</p>
