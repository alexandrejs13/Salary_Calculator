# 00_Layout_Global.md (COMPLETO – BLOCOS)

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 1 — identidade visual global
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Esta seção define a identidade visual completa do app...

(Conteúdo detalhado aqui conforme especificações.)

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 2 — tipografia
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Detalhamento completo da tipografia conforme instruções...


────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 3 — cores
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

A paleta de cores global do aplicativo segue uma estrutura 
defensiva para garantir consistência visual e alto contraste.

- color-bg-page        = #F5F5F7   (fundo da página)
- color-card-bg        = #FFFFFF   (fundo de containers)
- color-text-main      = #222222   (texto primário)
- color-text-muted     = #666666   (descrições, tooltips)
- color-border-light   = #E0E0E0   (linhas internas suaves)
- color-accent-primary = #0F4F59   (cor principal, igual à imagem enviada)
- color-accent-text    = #FFFFFF   (texto branco para destaque)

Regras gerais:
- Botões usam a cor color-accent-primary.
- Linhas finais das tabelas usam fundo color-accent-primary e 
  texto branco em negrito.
- Créditos (proventos) sempre em azul.
- Débitos (descontos) sempre em vermelho com sinal negativo.


────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 4 — barra lateral (sidebar)
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

A barra lateral é um elemento fixo do layout global. 

Regras:

1. Sempre aparece do lado esquerdo.
2. Não pode ser redimensionada pelo usuário.
3. Quando recolhida, o container da página permanece centralizado.
4. Deve conter, no mínimo:
   - seletor de idioma
   - navegação entre páginas
   - logo (caso exista)
5. Texto da sidebar segue a tipografia global.
6. Espaçamento interno consistente (padding >= 16px).
7. Quando recolhida:
   - mostra ícones ou abreviações,
   - NÃO desloca o container para a esquerda.

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 5 — título da página + bandeira do país
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

O título da página segue sempre o padrão:

Simulador de Remuneração – Região Américas                                     [BANDEIRA]

Regras:
1. O título fica SEMPRE alinhado à esquerda.
2. A bandeira do país selecionado fica SEMPRE alinhada à direita, na mesma linha.
3. A bandeira é carregada da pasta: assets/img/bandeiras/
4. Caso nenhum país esteja selecionado ainda, usar o ícone da região ou não exibir nada.
5. A altura do título e a altura da bandeira devem ser visualmente harmonizadas.
6. Não pode quebrar linha — largura calculada para caber dentro das 120 colunas.
7. Espaçamento superior e inferior fixo conforme CSS Global.

Comportamento:
- Ao mudar o país no formulário da Pag 01, a bandeira é atualizada dinamicamente.


────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 6 — select de idioma (i18n)
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Idiomas obrigatórios:
- pt (Português)
- en (Inglês)
- es (Espanhol)

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Localização:
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
- Sempre na barra lateral, no topo.

Regras do seletor:
1. O idioma selecionado afeta toda a aplicação.
2. Todos os textos da interface vêm dos arquivos JSON:
   data/i18n/pt.json
   data/i18n/en.json
   data/i18n/es.json
3. Cada JSON contém as mesmas chaves, apenas com textos traduzidos.
4. Nomes de países, rótulos de campos, nomes das abas das tabelas, mensagens de erro
   e tooltips são carregados automaticamente conforme o idioma.
5. As páginas NÃO devem conter textos fixos — somente chaves de tradução.

Exemplo de estrutura JSON:

{
  "titulo_pagina": "Simulador de Remuneração",
  "label_salario_base": "Salário Base",
  "btn_calcular": "Calcular Remuneração"
}

Carregamento:
- O app.py carrega o JSON do idioma no início.
- As páginas acessam o dicionário traduzido via sessão ou função global.


────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 7 — containers e layout 120 colunas
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

O layout principal do simulador utiliza um container de largura fixa lógica
equivalente a aproximadamente 120 colunas em fonte monoespaçada (Menlo).

REGRAS FUNDAMENTAIS:

1. O container é sempre CENTRALIZADO na área útil.
2. Ele NÃO pode ser redimensionado pelo usuário.
3. A largura total lógica (ASCII) aproxima-se de 120 colunas para manter:
   - alinhamento dos mockups
   - bordas retas
   - consistência visual
4. Cada linha de entradas deve ser distribuída com:
   - caixas proporcionais ao conteúdo
   - espaçamento consistente entre elas
   - alinhamento vertical e horizontal perfeito
5. O container deve respeitar paddings internos:
   - mínimo 16px top/bottom
   - mínimo 20px left/right
6. As bordas aparecem APENAS nos mockups da documentação, não no app real.
7. No app real, o container deve parecer um “card” limpo, com:
   - fundo branco (color-card-bg)
   - bordas suaves (color-border-light)
   - leve sombra (opcional)
8. O título da linha (“BASE DE CÁLCULO”, etc.) é alinhado totalmente à esquerda.
9. Títulos de caixa SEM negrito.
10. Títulos de seção COM negrito.
11. Espaço vertical entre seções: 20px a 32px.

FUNÇÃO DO CONTAINER:
Conter todos os campos do formulário sem quebrar o layout, independentemente:
- do país selecionado
- do número de caixas
- das labels maiores ou menores


────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 8 — botões do app
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

BOTÃO PRINCIPAL:
- Texto: “Calcular Remuneração”
- Altura: 40px
- Cantos arredondados: 6px
- Fonte: mesma do layout global, peso 600
- Cor de fundo: color-accent-primary (#0F4F59)
- Cor do texto: branca (color-accent-text)
- Deve ficar FORA do container do formulário:
  - imediatamente abaixo
  - alinhado à esquerda
  - espaçamento vertical de ~24px

INTERAÇÕES:
- Hover: escurecer levemente o fundo ou aumentar sombra.
- Active: clique sem deslocamento do layout.
- Focus: outline suave, não exagerado.

BOTÕES SECUNDÁRIOS (se existirem):
- Fundo branco
- Borda color-border-light
- Texto color-accent-primary
- Usados somente para ações auxiliares (limpar, exportar, voltar)

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 9 — tabelas (regras gerais)
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

As tabelas do simulador seguem uma padronização rigorosa em TODAS as páginas.
São 3 tabelas principais exibidas após o cálculo:

1. **Remuneração Mensal**
2. **Remuneração Anual**
3. **Composição da Remuneração**

REGRAS DE LAYOUT

1. Cada tabela tem sempre 3 colunas:
   - **Descrição** (alinhado à esquerda)
   - **%** (alinhado ao centro — nunca negativo)
   - **Valor** (alinhado à direita)

2. Cores:
   - Créditos (proventos): azul (#0000FF)
   - Débitos (descontos): vermelho (#FF0000), sempre com sinal negativo no valor
   - Títulos das tabelas: texto preto normal, fora da tabela
   - Última linha da tabela: 
       - fundo = color-accent-primary (#0F4F59)
       - texto branco
       - negrito

3. Cabeçalho das abas:
   - “Remuneração Mensal”
   - “Remuneração Anual”
   - “Composição da Remuneração”

4. A tabela NÃO tem título dentro do grid.  
   O título fica ACIMA da tabela, alinhado à esquerda.

5. LINHA FINAL:
   - Deve ser visualmente destacada.
   - Texto sempre branco.
   - Editável somente pelo código (nunca pelo usuário).
   - Ex.: “REMUNERAÇÃO MENSAL LÍQUIDA”, “REMUNERAÇÃO ANUAL LÍQUIDA”, “TOTAL REMUNERAÇÃO ANUAL”.

6. A coluna de **%**:
   - Na tabela mensal → refere-se à porcentagem que cada desconto representa do salário bruto.
   - Na tabela anual → mesma lógica, mas anualizada.
   - Na composição → % relativo da remuneração total (bonus + salário anual), somando 100%.

7. Espaçamento & Bordas:
   - Linhas separadas por `color-border-light`
   - Tabela clara, sem bordas externas grossas.
   - Padding de 8–12px por célula.

8. Responsividade:
   - Quando a largura da tela diminuir, as tabelas ENCOLHEM proporcionalmente, mas nunca quebram ordem das colunas.
   - Nomes grandes devem quebrar linha internamente se necessário, sem desalinhamento.


────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 10 — css global
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

O CSS global controla toda a aparência do app.  
Arquivo: **assets/css/layout_global.css**

10.1 — ESTRUTURA DO CSS

O arquivo deve conter:

1. **Reset global**
2. **Tipografia**
3. **Cores**
4. **Containers / cards**
5. **Botões**
6. **Tabelas**
7. **Título + bandeira**
8. **Sidebar**
9. **Responsividade mínima**

10.2 — RESET GLOBAL

body, html {
    margin: 0;
    padding: 0;
    font-family: 'Inter', sans-serif;
    background: #F5F5F7;
    color: #222222;
}

10.3 — TÍTULO + BANDEIRA

.title-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
}

.title-row h1 {
    margin: 0;
    padding: 0;
    font-size: 26px;
    font-weight: 700;
}

.title-flag {
    height: 32px;
    width: auto;
}

10.4 — CONTAINER PRINCIPAL

.form-container {
    background: #FFFFFF;
    padding: 24px;
    margin-top: 20px;
    border: 1px solid #E0E0E0;
    border-radius: 8px;
    max-width: 1200px;
    width: 100%;
    margin-left: auto;
    margin-right: auto;
}

.section-title {
    font-weight: 700;
    margin-bottom: 8px;
}

.field-label {
    font-weight: 400;
    margin-bottom: 4px;
}

.field-row {
    display: flex;
    gap: 16px;
    margin-bottom: 16px;
}

.field {
    flex: 1;
    display: flex;
    flex-direction: column;
}

10.5 — BOTÃO PRINCIPAL

.stButton>button {
    background-color: #0F4F59;
    color: white;
    border-radius: 6px;
    padding: 8px 20px;
    font-weight: 600;
    height: 40px;
    border: none;
}

.stButton>button:hover {
    background-color: #0c3f47;
}

10.6 — TABELAS

.result-table {
    width: 100%;
    border-collapse: collapse;
}

.result-table th, .result-table td {
    padding: 8px;
    border-bottom: 1px solid #E0E0E0;
}

.result-table th {
    text-align: left;
    font-weight: 600;
}

.result-table td:nth-child(2) {
    text-align: center;
}

.result-table td:nth-child(3) {
    text-align: right;
}

.result-table .final-row {
    background: #0F4F59;
    color: white;
    font-weight: 700;
}

.credit {
    color: blue;
}

.debit {
    color: red;
}

10.7 — SIDEBAR

[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #E0E0E0;
}

10.8 — RESPONSIVIDADE

@media(max-width: 900px) {
    .field-row {
        flex-direction: column;
    }
}

