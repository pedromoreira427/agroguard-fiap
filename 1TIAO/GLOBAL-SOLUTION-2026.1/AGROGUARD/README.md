# FIAP - Faculdade de Informática e Administração Paulista

![FIAP](https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Fiap_logo.png/200px-Fiap_logo.png)

# AgroGuard — Plataforma Inteligente de Previsão de Risco de Queimadas

### Global Solution 2026.1 — Inteligência Artificial aplicada à Economia Espacial

---

## Integrante

| Nome | RM |
|---|---|
| Pedro Gustavo França Moreira | RM568262 |

---

##  Sobre o Projeto

O **AgroGuard** é uma plataforma de previsão de risco de queimadas no Cerrado brasileiro, desenvolvida como prova de conceito (POC) para a Global Solution 2026.1 da FIAP.

O projeto conecta dados reais de satélites da NASA com algoritmos de Machine Learning para classificar o nível de risco de queimadas (baixo, médio ou alto) com base exclusivamente em variáveis climáticas — sem depender de informações em tempo real de focos já detectados.

O resultado é um produto com aplicabilidade B2B real: seguradoras rurais, bancos de financiamento agrícola e prefeituras de regiões do Cerrado podem usar o AgroGuard para antecipar riscos, acionar equipes e tomar decisões baseadas em dados.

---

##  Conexão com a Economia Espacial

O AgroGuard usa dados do sistema **NASA FIRMS** (Fire Information for Resource Management System), que coleta informações de focos de calor a partir de satélites como o Terra e o Aqua. Esses satélites orbitam a Terra continuamente e detectam radiação infravermelha emitida por incêndios na superfície terrestre.

Combinado com dados climáticos históricos da API **Open-Meteo**, o sistema transforma informações espaciais em inteligência acionável para o agronegócio brasileiro.

---

##  Arquitetura da Solução

```
[NASA FIRMS API]          [Open-Meteo API]
       ↓                         ↓
  coleta_dados.ipynb  ←→  coleta_dados.ipynb
       ↓
  focos_cerrado_2020_2024.csv
  clima_cerrado_2020_2024.csv
       ↓
  pipeline.ipynb
  (limpeza, cruzamento, feature engineering)
       ↓
  dataset_agroguard.csv
       ↓
  modelo.ipynb
  (Random Forest + GridSearchCV + XGBoost)
       ↓
  modelo_agroguard.pkl
       ↓
  dashboard.py (Streamlit)
  (Simulador | Mapa | Análise Temporal)
```

---

##  Machine Learning

| Item | Detalhe |
|---|---|
| Algoritmo principal | Random Forest Classifier |
| Algoritmos testados | Random Forest, Random Forest otimizado (GridSearchCV), XGBoost |
| Tipo de problema | Classificação multiclasse (3 classes) |
| Acurácia final | 71% |
| Features de entrada | Temperatura máxima, precipitação, vento, umidade, dias sem chuva, mês, dia do ano |
| Target | Nível de risco: 0 (Baixo), 1 (Médio), 2 (Alto) |
| Dataset | 1.827 dias (2020–2024), Cerrado brasileiro |
| Fonte dos dados | NASA FIRMS (273.308 focos) + Open-Meteo |

### Variáveis mais importantes (feature importance):
1. **Umidade máxima** — 21,84%
2. **Dia do ano** — 20,97% (sazonalidade)
3. **Temperatura máxima** — 12,83%

---

##  Dashboard

O dashboard foi desenvolvido em **Streamlit** e conta com três seções:

- ** Simulador de Risco** — o usuário informa as condições climáticas do dia e recebe a previsão de risco com probabilidades e recomendações de ação
- ** Mapa de Focos** — visualização geográfica interativa dos focos de calor detectados por satélite, filtrável por ano e mês
- ** Análise Temporal** — distribuição mensal do risco ao longo dos anos e relação entre temperatura e nível de risco

---

## 🗂️ Estrutura do Repositório

```
📂 AGROGUARD
│
├── coleta_dados.ipynb          # Etapa 1: coleta via NASA FIRMS e Open-Meteo
├── pipeline.ipynb              # Etapa 2: limpeza, cruzamento e feature engineering
├── modelo.ipynb                # Etapa 3: treinamento e avaliação do modelo ML
├── dashboard.py                # Etapa 4: dashboard interativo em Streamlit
│
├── dataset_agroguard.csv       # Dataset final para treinamento
├── modelo_agroguard.pkl        # Modelo treinado serializado
├── features.pkl                # Lista de features do modelo
│
├── assets/
│   ├── matriz_confusao.png     # Matriz de confusão do modelo
│   └── importancia_features.png # Gráfico de importância das variáveis
│
└── README.md
```

---

## ▶️ Como Executar

### Pré-requisitos
- Python 3.11+
- Conta gratuita na [NASA FIRMS API](https://firms.modaps.eosdis.nasa.gov/api/area/)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/agroguard.git
cd agroguard

# Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instale as dependências
pip install streamlit streamlit-folium folium plotly scikit-learn joblib pandas numpy xgboost openmeteo-requests requests-cache retry-requests
```

### Executando o Dashboard

```bash
streamlit run dashboard.py
```

### Executando os Notebooks

Execute os notebooks na seguinte ordem:
1. `coleta_dados.ipynb` — coleta os dados da NASA e Open-Meteo
2. `pipeline.ipynb` — processa e gera o dataset de treino
3. `modelo.ipynb` — treina o modelo e gera o `modelo_agroguard.pkl`
4. `dashboard.py` — inicia a interface interativa

---

##  Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| Python 3.11 | Linguagem principal |
| Pandas / NumPy | Manipulação e análise de dados |
| Scikit-learn | Machine Learning (Random Forest, GridSearchCV) |
| XGBoost | Algoritmo alternativo de boosting |
| Streamlit | Dashboard interativo |
| Plotly | Gráficos interativos |
| Folium | Mapa geográfico de focos |
| NASA FIRMS API | Dados de focos de calor por satélite |
| Open-Meteo API | Dados climáticos históricos |
| Google Colab | Ambiente de desenvolvimento e treinamento |
| Joblib | Serialização do modelo treinado |

---

## 📋 Licença

[![CC BY 4.0](https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1)](http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1)

Este projeto está licenciado sob [Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1).
