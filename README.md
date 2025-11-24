# Simulador de Remuneração — Streamlit

Aplicação multipágina desenvolvida em Streamlit seguindo a documentação do projeto. Inclui simulador completo, comparador de cenários, custo do empregador, cálculo inverso (bruto a partir do líquido), tabelas de contribuições, comparativo de países, explicador automático, glossário e equivalência internacional.

## Estrutura
- `app.py`: Página 01 — Simulador de Remuneração.
- `pages/02_Comparador_de_Remuneracao.py`: Comparação de cenários A x B.
- `pages/03_...` a `pages/09_...`: Demais páginas descritas na documentação.
- `assets/css/layout_global.css`: Estilo global (container 120 colunas, botões, tabelas, sidebar).
- `assets/img/bandeiras/`: Bandeiras carregadas dinamicamente no título.
- `data/i18n/*.json`: Textos em pt/en/es (i18n).
- `engines/`: Motores de cálculo, formulários dinâmicos, renderizadores de tabelas e utilidades de UI.

## Rodando localmente
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy no Streamlit Cloud
1) Crie um repositório no GitHub e faça push deste diretório.  
2) No Streamlit Cloud, escolha “New app” > conecte ao repositório > branch principal > `app.py`.  
3) Variáveis ambientais não são necessárias. A versão mínima recomendada está em `requirements.txt`.

## Testes rápidos
```bash
pytest
```
- Valida consistência das traduções e fluxo básico de cálculo.

## Observações
- As fórmulas de encargos por país seguem o fluxo bruto → líquido da documentação e utilizam parâmetros simplificados/ilustrativos onde a legislação completa não foi detalhada.  
- Todos os textos visíveis vêm dos arquivos de tradução; rótulos fixos no código foram minimizados.  
- Cores, layout da sidebar, largura lógica (~120 colunas), botões e tabelas seguem o guia visual fornecido.
