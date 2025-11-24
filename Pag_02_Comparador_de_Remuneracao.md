────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Página 02 — comparador de remuneração
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

NOME DO ARQUIVO (CÓDIGO STREAMLIT)
/pages/02_Comparador_de_Remuneracao.py

NOME DO ARQUIVO (DOCUMENTAÇÃO)
/docs/Pag_02_Comparador_de_Remuneracao.md

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Objetivo da página
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

A Página 02 permite COMPARAR DOIS CENÁRIOS COMPLETOS DE REMUNERAÇÃO
(Cenário A e Cenário B) para UM MESMO PAÍS, utilizando:

- o mesmo motor de cálculo da Página 01 (Simulador de Remuneração)
- as mesmas regras fiscais, previdenciárias e de benefícios
- os mesmos renderizadores de tabelas padrão (3 colunas)
- um RENDERIZADOR ADICIONAL de tabela comparativa (5 colunas)

A página responde às perguntas:

- "Se eu mudar o salário base, quanto muda o líquido?"
- "Se eu alterar o bônus, quanto muda a remuneração anual?"
- "Qual a diferença em % entre dois pacotes de remuneração?"

O foco é comparação A x B para apoiar decisões de:

- contração
- promoção
- ajuste salarial
- propostas alternativas para candidatos ou colaboradores


────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 1 — elementos herdados do layout global
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

A Página 02 herda TODAS as configurações de layout definidas no
arquivo 00_Layout_Global.md, incluindo:

1. CONTAINER PRINCIPAL (CARD LÓGICO DE 120 COLUNAS)
   - largura lógica aproximada de 120 colunas em fonte monoespaçada
   - sempre CENTRALIZADO na área útil
   - não redimensionável pelo usuário
   - padding interno mínimo:
       - 16px top/bottom
       - 20px left/right
   - bordas visíveis APENAS na documentação (mockups ASCII)
   - no app real: card limpo, fundo branco (color-card-bg),
     borda suave (color-border-light), sombra leve opcional

2. TIPOGRAFIA E TÍTULOS
   - Labels de campos SEM negrito
   - Títulos de SEÇÃO COM negrito
   - títulos das linhas sempre alinhados totalmente à esquerda
   - fonte monoespaçada (Menlo / Consolas / monospace) na documentação

3. ESPAÇAMENTO VERTICAL
   - entre SEÇÕES: 20px a 32px
   - entre linhas de formulários: consistente com Página 01
   - entre o formulário e as tabelas: ~24px

4. TABELAS PADRÃO (RENDERER GLOBAL — 3 COLUNAS)
   - colunas:
       - Descrição (alinhado à esquerda)
       - % (alinhado ao centro, nunca negativo)
       - Valor (alinhado à direita)
   - cores:
       - créditos (proventos): azul (#0000FF)
       - débitos (descontos): vermelho (#FF0000) com sinal negativo
       - linha final:
           - fundo = color-accent-primary (#0F4F59)
           - texto branco
           - negrito
   - título da tabela sempre ACIMA, alinhado à esquerda
   - sem título dentro do grid
   - bordas internas com color-border-light
   - padding de 8–12px
   - responsividade preservando ordem das colunas

5. SIDEBAR E NAVEGAÇÃO
   - menu lateral herdado do layout global
   - seleção de idiomas (sem detalhar aqui)
   - item selecionado: Página 02 — Comparador de Remuneração

6. CORES E ESTÉTICA GERAL
   - mesma paleta de cores global utilizada na Página 01
   - componentes reutilizam as mesmas classes de CSS:
       - .app-container
       - .section-title
       - .field-row
       - .result-table
       - .tabs-header, etc.


────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 2 — visão geral da estrutura da página
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

BLOCOS PRINCIPAIS
A Página 02 é composta pelos seguintes blocos, nesta ordem:

1) Cabeçalho da Página (título + país selecionado)
2) Container de seleção de país
3) Container de comparação (Cenário A x Cenário B)
4) Bloco de resultados individuais (A e B)
5) Bloco de tabela comparativa consolidada (5 colunas)
6) Bloco de observações/notas (opcional)

A lógica de cálculo é a mesma da Página 01, mas aplicada DUAS VEZES:
uma para o Cenário A, outra para o Cenário B.


────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 3 — cabeçalho da página
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

TÍTULO VISÍVEL
Simulador de Remuneração — Comparador de Cenários

SUBTÍTULO
Compare dois cenários completos de remuneração para o mesmo país
e visualize as diferenças mensais e anuais.

MOCKUP ASCII DO CABEÇALHO

+================================================================================================+
| Simulador de Remuneração — Comparador de Cenários                                              |
| País selecionado: [BRASIL ▼]                                                                   |
+================================================================================================+


────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 4 — formulário de seleção de país
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

REGRA FUNDAMENTAL
- O COMPARADOR NÃO PERMITE países diferentes entre Cenário A e B.
- O país é selecionado UMA ÚNICA VEZ.
- TODOS os cálculos dos dois cenários usam as regras desse país.

CAMPOS
- País (obrigatório, dropdown/picklist)
  - mesmas opções da Página 01:
    - Brasil
    - Chile
    - Argentina
    - Colômbia
    - México
    - Estados Unidos
    - Canadá
    - (outros, se incluídos no projeto)

MOCKUP ASCII (DENTRO DO CONTAINER PRINCIPAL)

+------------------------------------------------------------------------------------------------+
| País                                                                                           |
| [ BRASIL ▼ ]                                                                                   |
+------------------------------------------------------------------------------------------------+


────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 5 — formulário de comparação (cenário a x cenário b)
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

VISÃO GERAL
O container principal de comparação é dividido em DUAS colunas:
- lado esquerdo: CENÁRIO A
- lado direito: CENÁRIO B

Cada lado utiliza os MESMOS CAMPOS, com valores independentes.

REGRA DE NOMENCLATURA VISUAL
- Títulos das seções:
    - "Cenário A"
    - "Cenário B"
  (em negrito)
- Labels dos campos (sem negrito):
    - "Salário base"
    - "Bônus alvo anual" (ou equivalente do país)
    - "Número de dependentes" (onde aplicável)
    - Campos adicionais podem ser adicionados DEPOIS
      mantendo a simetria A e B.

CAMPOS MÍNIMOS POR CENÁRIO
Cada cenário (A e B) deve ter, no mínimo:

1) Salário base
   - numérico, obrigatório
   - currency do país
   - validação: > 0

2) Bônus alvo anual (ou valor de variável anual)
   - numérico, opcional
   - se vazio, assume 0

3) Número de dependentes (quando aplicável ao país)
   - inteiro, >= 0
   - se não aplicável ao país, o campo pode ser desabilitado
     ou oculto, mas a estrutura do container deve ser mantida.

OUTROS CAMPOS
Campos adicionais específicos de país (por exemplo:
tipo de contrato, UF/Estado, plano de saúde etc.) NÃO são
duplicados aqui individualmente na documentação, pois já
foram detalhados na Página 01.

REGRA IMPORTANTE:
- A Página 02 reutiliza TODOS os campos de entrada da Página 01
  para o país selecionado, porém:
  - com duas instâncias de valores: A e B
  - a mesma estrutura de picklists e validações

MOCKUP ASCII RESUMIDO DO FORMULÁRIO DE COMPARAÇÃO

+================================================================================================+
| Cenário A                                     | Cenário B                                      |
|-----------------------------------------------+------------------------------------------------|
| Salário base                                  | Salário base                                   |
| [__________R$__________]                      | [__________R$__________]                       |
|                                               |                                                |
| Bônus alvo anual                              | Bônus alvo anual                               |
| [__________R$__________]                      | [__________R$__________]                       |
|                                               |                                                |
| Número de dependentes                         | Número de dependentes                          |
| [____]                                        | [____]                                         |
|                                               |                                                |
| (Outros campos específicos do país,           | (Mesmos campos, duplicados para o Cenário B)   |
|  exatamente como na Página 01)                |                                                |
+================================================================================================+

BOTÃO DE CÁLCULO
- Um único botão no rodapé do container, centralizado:

[   Calcular cenários A e B   ]


────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 6 — fluxo de cálculo
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

1. Usuário seleciona o país.
2. Preenche os campos do Cenário A.
3. Preenche os campos do Cenário B.
4. Clica em "Calcular cenários A e B".
5. O código executa:

   a) chamando o motor de cálculo (mesmo da Página 01) para o Cenário A:
      - engines/calculator.py
      - usando parâmetros do país + parâmetros A

   b) chamando o mesmo motor para o Cenário B:
      - engines/calculator.py
      - usando parâmetros do país + parâmetros B

6. Cada chamada retorna:
   - dados de remuneração mensal
   - dados de remuneração anual
   - composição da remuneração
   - estrutura pronta para montar as tabelas de 3 colunas

7. Os resultados são enviados aos renderizadores:
   - engines/tables_renderer.py
     -> para as TABELAS INDIVIDUAIS de A e B
   - engines/tables_renderer_comparador.py
     -> para a TABELA COMPARATIVA consolidada de 5 colunas


────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 7 — tabelas individuais (cenário a e cenário b)
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

BLOCOS DE RESULTADO INDIVIDUAL
Após o cálculo, as tabelas individuais de cada cenário
são exibidas EM DUAS COLUNAS (A à esquerda, B à direita).

Para cada cenário são exibidas 3 tabelas padrão:

1) Remuneração Mensal
2) Remuneração Anual
3) Composição da Remuneração

ESTRUTURA VISUAL (EXEMPLO ASCII RESUMIDO)

+=========================================+=========================================+
| Remuneração Mensal — Cenário A          | Remuneração Mensal — Cenário B          |
+-----------------------------------------+-----------------------------------------+
| Descrição                |  % |  Valor  | Descrição                |  % |  Valor  |
|--------------------------+----+---------|--------------------------+----+---------|
| Salário base             | .. |  .....  | Salário base             | .. |  .....  |
| Bônus mensalizado        | .. |  .....  | Bônus mensalizado        | .. |  .....  |
| (-) Imposto de renda     | .. | -.....  | (-) Imposto de renda     | .. | -.....  |
| (-) Contribuição previd. | .. | -.....  | (-) Contribuição previd. | .. | -.....  |
| ...                      | .. |  .....  | ...                      | .. |  .....  |
|--------------------------+----+---------|--------------------------+----+---------|
| REMUNERAÇÃO MENSAL LÍQUIDA              | REMUNERAÇÃO MENSAL LÍQUIDA              |
| (linha final em destaque)               | (linha final em destaque)               |
+=========================================+=========================================+

As mesmas regras se aplicam para "Remuneração Anual" e "Composição da Remuneração":

- 3 colunas
- título acima da tabela
- linha final destacada
- cores de créditos/débitos
- responsividade preservada


────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 8 — tabela comparativa consolidada (5 colunas)
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Objetivo
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
Apresentar, em UMA ÚNICA TABELA, a comparação dos principais
indicadores finais dos dois cenários, lado a lado, com:

- valor do Cenário A
- valor do Cenário B
- diferença absoluta (B - A)
- diferença percentual (B / A - 1, em %)

ESTRUTURA PADRÃO DA TABELA COMPARATIVA
A tabela comparativa possui SEMPRE 5 colunas:

1) Descrição                  (texto, alinhado à esquerda)
2) Cenário A                  (valor numérico, à direita)
3) Cenário B                  (valor numérico, à direita)
4) Diferença Absoluta (B - A) (valor numérico, à direita)
5) Diferença %     (B vs A)   (percentual, alinhado à direita)

REGRAS DE CÁLCULO

- DIFERENÇA ABSOLUTA:
  diff_abs = valor_B - valor_A

- DIFERENÇA %:
  Se valor_A != 0:
      diff_pct = (valor_B / valor_A - 1) * 100
  Se valor_A == 0:
      - exibir "—" ou tratar como caso especial
      - impedir divisão por zero

- SINAL VISUAL (COR):
  - Se diff_abs > 0:
      - pode ser exibido em azul ou cor neutra (ganho)
  - Se diff_abs < 0:
      - pode ser exibido em vermelho (perda)
  - Se diff_abs = 0:
      - texto padrão (cor neutra)

- A coluna "Descrição" não muda de cor.

LINHA FINAL
- A tabela comparativa também possui uma LINHA FINAL EM DESTAQUE,
  similar ao padrão global:
  - fundo color-accent-primary (#0F4F59)
  - texto branco
  - negrito
- Exemplo de linha final:
  - "Diferença total na remuneração anual"
  - agregando todas as diferenças consideradas relevantes.

EXEMPLO ASCII RESUMIDO DA TABELA COMPARATIVA (5 COLUNAS)

+==============================================================================================+
| Comparativo de Remuneração — Cenário A x Cenário B                                           |
+----------------------------------------------------------------------------------------------+
| Descrição                          |   Cenário A |   Cenário B | Dif. Absoluta | Dif.  %     |
|------------------------------------+-------------+-------------+---------------+-------------|
| Remuneração mensal bruta           |   10.000,00 |   11.000,00 |    1.000,00   |   10,0%     |
| Remuneração mensal líquida         |    7.200,00 |    7.600,00 |      400,00   |    5,6%     |
| Remuneração anual total            |  160.000,00 |  175.000,00 |   15.000,00   |    9,4%     |
| % bônus sobre remuneração anual    |      15,0%  |      20,0%  |        5,0 p.p|   33,3%     |
| ...                                |         ... |         ... |          ...  |     ...     |
|------------------------------------+-------------+-------------+---------------+-------------|
| DIFERENÇA TOTAL REMUNERAÇÃO ANUAL  |  160.000,00 |  175.000,00 |   15.000,00   |    9,4%     |
| (linha final em destaque)          |             |             |               |             |
+==============================================================================================+

OBSERVAÇÃO:
- A linha final pode repetir os valores totais ou apresentar apenas a diferença.
- A decisão exata é tomada no código de renderer, mas a documentação garante
  que visualmente a linha final é destacada e não editável pelo usuário.


────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 9 — regras de negócio específicas
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

1. MESMO PAÍS PARA A E B
   - O comparador não permite escolher países diferentes para A e B.
   - Se o usuário tentar alterar o país após preencher os campos,
     o app deve:
       - exibir aviso (opcional) e
       - recalcular ambos os cenários com as novas regras ou
       - limpar os campos, dependendo da implementação escolhida.

2. CAMPOS OBRIGATÓRIOS
   - País
   - Salário base A
   - Salário base B
   - Eventuais campos obrigatórios da Página 01 também
     são obrigatórios em A e B (ex: tipo de contrato em países específicos).

3. VALIDAÇÕES BÁSICAS
   - Salário base > 0
   - Bônus >= 0
   - Dependentes >= 0
   - Não permitir caracteres inválidos (letras em campos numéricos etc.)

4. CONSISTÊNCIA ENTRE A E B
   - As mesmas regras fiscais, previdenciárias e de benefícios se aplicam
     automaticamente aos dois cenários, pois ambos usam o mesmo país.

5. MOEDA E FORMATAÇÃO
   - As colunas de valores usam o formato de moeda do país selecionado.
   - A tabela comparativa utiliza a MESMA moeda nas colunas A e B.
   - Diferença % sempre em percentual, com casas decimais definidas
     no layout global (por exemplo, 1 casa para % relativas, 2 casas para % de impostos).

6. PERFIL DE USO
   - Gestores de remuneração, HRBP, recrutadores, etc.
   - Cenários típicos:
     - Proposta atual vs. proposta futura
     - Pacote interno vs. oferta externa
     - Cenário com e sem bônus / com e sem benefícios específicos


────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 10 — arquitetura técnica
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

ARQUIVOS PRINCIPAIS

1) /pages/02_Comparador_de_Remuneracao.py
   - Define o layout da Página 02.
   - Contém:
      - seleção de país
      - formulário Cenário A
      - formulário Cenário B
      - botão de cálculo
      - chamadas ao motor de cálculo
      - chamadas aos renderizadores de tabelas
      - montagem da tabela comparativa (via renderer específico)

2) /engines/calculator.py
   - Mesmo motor de cálculo utilizado na Página 01.
   - Recebe:
      - país
      - dicionário de parâmetros (salário, bônus, dependentes etc.)
   - Retorna:
      - estrutura de dados para as 3 tabelas padrão.

3) /engines/tables_renderer.py
   - Renderer global para as tabelas:
      - Remuneração Mensal
      - Remuneração Anual
      - Composição da Remuneração
   - Usado para Cenário A e Cenário B.

4) /engines/tables_renderer_comparador.py
   - Renderer específico para a TABELA COMPARATIVA de 5 colunas.
   - Responsável por:
      - receber os resultados consolidados de A e B
      - calcular diferença absoluta e percentual
      - aplicar cores condicionais
      - destacar a linha final.

5) /components/global_container.py
   - Componente opcional que monta o container de 120 colunas
     com paddings corretos, bordas (na documentação) e comportamento
     responsivo.

6) /assets/css/layout_global.css
   - Define as classes globais de estilo:
      - container
      - headings
      - field rows
      - result-table
      - etc.

7) /data/parametros_*.*
   - Arquivos de parâmetros específicos por país (json, py ou equivalente).
   - Já documentados na Página 01.


────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 11 — mockup ascii completo da página
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Abaixo, um mockup ASCII simplificado, apenas para mostrar
a ESTRUTURA GERAL em 120 colunas lógicas:

+================================================================================================+
| Simulador de Remuneração — Comparador de Cenários                                              |
| País: [ BRASIL ▼ ]                                                                             |
+================================================================================================+
|                                                                                                |
|  Cenário A                                     |  Cenário B                                    |
|  ---------------------------------------------+----------------------------------------------- |
|  Salário base                                  |  Salário base                                 |
|  [__________________________]                  |  [__________________________]                 |
|                                               |                                                |
|  Bônus alvo anual                              |  Bônus alvo anual                             |
|  [__________________________]                  |  [__________________________]                 |
|                                               |                                                |
|  Número de dependentes                         |  Número de dependentes                        |
|  [____]                                        |  [____]                                       |
|                                               |                                                |
|  (Demais campos herdados da Página 01,        |  (Mesmos campos, replicados para B)            |
|   conforme país selecionado)                  |                                                |
|                                                                                                |
|                               [  Calcular cenários A e B  ]                                    |
+================================================================================================+

(área de resultados)

+================================================================================================+
| Remuneração Mensal — Cenário A              | Remuneração Mensal — Cenário B                   |
| (tabela padrão de 3 colunas)                | (tabela padrão de 3 colunas)                     |
+================================================================================================+

+================================================================================================+
| Remuneração Anual — Cenário A               | Remuneração Anual — Cenário B                    |
| (tabela padrão de 3 colunas)                | (tabela padrão de 3 colunas)                     |
+================================================================================================+

+================================================================================================+
| Composição da Remuneração — Cenário A       | Composição da Remuneração — Cenário B            |
| (tabela padrão de 3 colunas)                | (tabela padrão de 3 colunas)                     |
+================================================================================================+

+================================================================================================+
| Comparativo de Remuneração — Cenário A x Cenário B                                             |
| (tabela de 5 colunas: Descrição | A | B | Dif. Abs. | Dif. %)                                  |
+================================================================================================+


────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 12 — resumo executivo
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

- A Página 02 é uma extensão direta da Página 01.
- Toda a base de regras, parâmetros e cálculos é reaproveitada.
- A única grande diferença é:
    - DUAS entradas completas de dados (Cenário A e B)
    - UM renderizador adicional para a TABELA COMPARATIVA (5 colunas).
- O layout segue rigorosamente:
    - container de 120 colunas
    - paddings padronizados
    - tipografia definida
    - cores e bordas globais.

Essa documentação é suficiente para:

- Desenvolver o código completo da Página 02
- Implementar o renderer específico de comparação
- Validar o comportamento visual no layout global
- Manter consistência com todo o simulador (todas as páginas).

FIM DO DOCUMENTO — PÁGINA 02 (COMPARADOR DE REMUNERAÇÃO)
