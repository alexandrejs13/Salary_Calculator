
# Pag_01_Simulador_de_Remuneracao.md (COMPLETO – BLOCOS)

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 1 — introdução da página
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Esta página documenta o funcionamento completo da primeira tela do
Simulador de Remuneração. Inclui formulários para 7 países, regras de
cálculo e o layout das tabelas de resultados.

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 2 — estrutura geral da página
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Elementos principais:
- Título + bandeira (emoji nativo)
- Container central de 120 colunas
- Formulário dinâmico conforme país (seletor de país fica dentro da seção “Localização e tipo de contrato de trabalho”)
- Botão "Calcular Remuneração" (com divisor antes do botão)
- 3 abas de resultados:
  - Remuneração Mensal
  - Remuneração Anual
  - Composição da Remuneração
  - Linha de benefícios informativos logo abaixo das abas Mensal/Anual (FGTS/AFP/Jubilación/Cesantías/AFORE/RRSP etc., conforme país)

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 3 — estrutura completa do formulário
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

O formulário da Página 01 segue um padrão rígido para garantir alinhamento,
consistência visual e funcionamento dinâmico para os 7 países.

REGRAS GERAIS DO FORMULÁRIO:

1. O formulário fica dentro de um CONTAINER de 120 colunas (layout global).
2. Cada linha tem um TÍTULO DE SEÇÃO alinhado à esquerda (ex.: LOCALIZAÇÃO).
3. Abaixo do título da linha, as caixas de entrada são exibidas lado a lado.
4. As caixas se distribuem automaticamente em largura proporcional, ocupando toda a linha (2, 3, 4 ou 5 colunas conforme o país).
5. Labels de caixas SEM negrito.
6. Títulos de linha COM negrito.
7. Espaçamento vertical entre linhas: entre 12px e 24px (mais compacto).
8. O botão "Calcular Remuneração" fica FORA do container, alinhado à esquerda, precedido por um divisor.
9. Campo “Salário Anual” (somente leitura) calculado automaticamente = salário base × frequência anual.

SEÇÕES DO FORMULÁRIO:
- Localização e Tipo de Contrato de Trabalho
- Base de Cálculo
- Descontos e Fatores de Dedução
- Previdência Privada
- Bônus Anual

Cada país pode ter:
- mais ou menos campos
- campos editáveis ou não
- tooltips específicos
- picklists exclusivos

O layout e spacing, porém, permanecem CONSISTENTES para todos.

ATUALIZAÇÕES RECENTES POR PAÍS:
- Campo “Salário Anual” aparece em Base de Cálculo (automático em todos os países).
- Chile: Saúde/Plano e AFP ficam na mesma linha de “Descontos e fatores de dedução”.
- Argentina: campos de Jubilación e Obra Social não são editáveis (descontos automáticos).
- Colômbia: Cidade fica na primeira linha ao lado do País; Fundo de Solidariedade é automático e não tem campo manual.
- México: Estado fica na primeira linha ao lado do País; Cuota Obrera é automática (sem campo); Riesgo de Trabajo removido.
- EUA: Estado na primeira linha ao lado do País; Filing Status e Retenção adicional na linha de descontos.
- Canadá: Província e ajustes provinciais na primeira linha ao lado do País; subtítulo de tributação removido.
- Benefícios informativos (FGTS/AFP/Jubilación/Cesantías/AFORE/RRSP etc.) aparecem logo abaixo das tabelas Mensal e Anual, não na composição.


────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 4 — formulários dos 7 países
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

A seguir, cada país tem seu formulário desenhado em ASCII,
ocupando sempre o container de 120 colunas, com bordas retas
e distribuição proporcional das caixas.

FORMULÁRIO 1 — BRASIL

+--------------------------------------------------------------------------------------------------------+
| LOCALIZAÇÃO E TIPO DE CONTRATO DE TRABALHO                                                             |
|                                                                                                        |
| País                     | Tipo de Contrato                                                            |
| [__________]             | [______________________________]                                            |
+--------------------------------------------------------------------------------------------------------+
| BASE DE CÁLCULO                                                                                        |
|                                                                                                        |
| Salário Base             | Frequência Anual (fixo)        | Outros Adicionais                          |
| [__________]             | [13,33] (não editável)         | [______________________________]           |
+--------------------------------------------------------------------------------------------------------+
| DESCONTOS E FATORES DE DEDUÇÃO                                                                         |
|                                                                                                        |
| Outros Descontos         | Pensão Alimentícia             | Nº de Dependentes IRRF                     |
| [__________]             | [__________]                   | [__________]                               |
+--------------------------------------------------------------------------------------------------------+
| PREVIDÊNCIA PRIVADA                                                                                    |
|                                                                                                        |
| Tipo de Previdência      | Contribuição Empregador        | Contribuição Empregado                     |
| [__________]             | [__________]                   | [__________]                               |
+--------------------------------------------------------------------------------------------------------+
| BÔNUS ANUAL                                                                                            |
|                                                                                                        |
| % do Bônus Anual         | Valor Calculado (fixo)         | Incidências do Bônus                       |
| [__________]             | [__________] (não editável)    | [Picklist ▼]                               |
+--------------------------------------------------------------------------------------------------------+

PICKLISTS DO BRASIL:
- Tipo de Previdência:
  • PGBL
  • VGBL
  • FGBL
- Incidências do Bônus:
  • Não sofre incidência
  • Incidência apenas IRRF
  • Incidência total: FGTS, 13º, férias, IRRF, INSS
- Tipo de Contrato:
  • CLT
  • Estatutário
  • Autônomo


FORMULÁRIO 2 — CHILE

+--------------------------------------------------------------------------------------------------------+
| LOCALIZAÇÃO E TIPO DE CONTRATO DE TRABALHO                                                             |
|                                                                                                        |
| País                     | Cidade                                                                      |
| [__________]             | [______________________________]                                            |
+--------------------------------------------------------------------------------------------------------+
| BASE DE CÁLCULO                                                                                        |
|                                                                                                        |
| Sueldo Base              | Frecuencia Anual (fixo)        | Otros Adicionales                          |
| [__________]             | [12 + Aguinaldo] (no editable)| [______________________________]            |
+--------------------------------------------------------------------------------------------------------+
| DESCUENTOS                                                                                             |
|                                                                                                        |
| Salud (7% ó Isapre)      | AFP (%)                        | Otros Descuentos                           |
| [Picklist ▼]             | [__________]                   | [__________]                               |
+--------------------------------------------------------------------------------------------------------+
| BONO ANUAL                                                                                             |
| % del Bono               | Valor Calculado (fijo)         | Incidencias del Bono                       |
| [__________]             | [__________] (no editable)     | [Picklist ▼]                               |
+--------------------------------------------------------------------------------------------------------+

PICKLISTS CHILE:
- Salud:
  • FONASA (7%)
  • ISAPRE (plano privado)
- Incidencias del Bono:
  • Afecto solo a impuestos
  • Afecto a AFP + Salud
  • Exento
- Frecuencia Anual: 12 + aguinaldo (aguinaldo ≈ 1 sueldo)


FORMULÁRIO 3 — ARGENTINA

+--------------------------------------------------------------------------------------------------------+
| LOCALIZACIÓN Y TIPO DE CONTRATO                                                                        |
|                                                                                                        |
| País                     | Ciudad                                                                      |
| [__________]             | [______________________________]                                            |
+--------------------------------------------------------------------------------------------------------+
| BASE DE CÁLCULO                                                                                        |
|                                                                                                        |
| Salario Base             | Frecuencia (fijo)               | Otros Adicionales                         |
| [__________]             | [13] (no editable)             | [______________________________]           |
+--------------------------------------------------------------------------------------------------------+
| DESCUENTOS                                                                                             |
|                                                                                                        |
| Jubilación (%)           | Obra Social (%)                 | Otros Descuentos                          |
| [__________]             | [__________]                   | [__________]                               |
+--------------------------------------------------------------------------------------------------------+
| IMPUESTO A LAS GANANCIAS                                                                               |
|                                                                                                        |
| Deducción Especial       | Deducción por Dependientes                                                  |
| [__________]             | [__________]                                                                |
+--------------------------------------------------------------------------------------------------------+

... (continua com Colômbia, México, EUA e Canadá)

FORMULÁRIO 4 — COLÔMBIA
(Formulário completo será inserido aqui conforme especificações)

FORMULÁRIO 5 — MÉXICO
(Formulário completo será inserido aqui conforme especificações)

FORMULÁRIO 6 — ESTADOS UNIDOS
(Formulário completo será inserido aqui conforme especificações)

FORMULÁRIO 7 — CANADÁ
(Formulário completo será inserido aqui conforme especificações)

FORMULÁRIO 4 — COLÔMBIA

+--------------------------------------------------------------------------------------------------------+
| LOCALIZAÇÃO E TIPO DE CONTRATO DE TRABALHO                                                             |
|                                                                                                        |
| País                     | Cidade                                | Tipo de Contrato                    |
| [Colômbia ▼]             | [___________________________]          | [Picklist ▼]                       |
+--------------------------------------------------------------------------------------------------------+
| BASE DE CÁLCULO                                                                                        |
|                                                                                                        |
| Salário Base             | Frequência Anual (fixo)                | Outros Adicionais (tooltip)        |
| [__________]             | [12 + Prima] (não editável)            | [___________________________]      |
+--------------------------------------------------------------------------------------------------------+
| SEGURIDADE SOCIAL – DESCONTOS                                                                          |
|                                                                                                        |
| Saúde (4%)               | Pensão (4%)                            | Fundo de Solidariedade (se aplic.) |
| [__________]             | [__________]                           | [__________]                       |
+--------------------------------------------------------------------------------------------------------+
| DESCONTOS E DEDUÇÕES TRIBUTÁRIAS                                                                       |
|                                                                                                        |
| Outros Descontos         | Dependentes para Desconto IRPF         | Benefícios Isentos                 |
| [__________]             | [__________]                           | [__________]                       |
+--------------------------------------------------------------------------------------------------------+
| BÔNUS ANUAL                                                                                            |
|                                                                                                        |
| % do Bônus Anual         | Valor Calculado (fixo)                 | Incidências do Bônus               |
| [__________]             | [__________] (não editável)            | [Picklist ▼]                       |
+--------------------------------------------------------------------------------------------------------+

PICKLISTS COLÔMBIA:
- Tipo de Contrato:
  • Indefinido
  • Termo Fijo
  • Prestação de Serviços (sem benefícios sociais)
- Frequência Anual:
  • 12 + Prima Legal (equivalente ao 13º)
- Incidências do Bônus:
  • Só imposto
  • Imposto + Seguridade Social
  • Isento
- Saúde:
  • 4% empregado
- Pensão:
  • 4% empregado
- Fundo de Solidariedade:
  • 1% a 2% (obrigatório acima de certos salários)

TOOLTIPS:
- Outros Adicionais:
  “Inclui horas extras, recargos noturnos, comissões, periculosidade.”
- Outros Descontos:
  “Inclui plano de saúde privado, seguros, empréstimos, etc.”
- Benefícios Isentos:
  “Elementos que reduzem base tributária segundo legislação colombiana.”

FORMULÁRIO 5 — MÉXICO

+--------------------------------------------------------------------------------------------------------+
| LOCALIZACIÓN Y TIPO DE CONTRATO                                                                        |
|                                                                                                        |
| País                     | Estado                                | Tipo de Contrato                    |
| [México ▼]               | [Picklist ▼]                          | [Picklist ▼]                        |
+--------------------------------------------------------------------------------------------------------+
| BASE DE CÁLCULO                                                                                        |
|                                                                                                        |
| Salario Base             | Frecuencia Anual (fijo)               | Otros Adicionales (tooltip)         |
| [__________]             | [12 + Aguinaldo] (no editable)        | [___________________________]       |
+--------------------------------------------------------------------------------------------------------+
| SEGURIDAD SOCIAL – IMSS                                                                                |
|                                                                                                        |
| Cuota Obrera (%)         | Riesgo de Trabajo (%)                 | Otros Descuentos                    |
| [__________]             | [__________]                           | [__________]                       |
+--------------------------------------------------------------------------------------------------------+
| IMPUESTO SOBRE LA RENTA (ISR)                                                                          |
|                                                                                                        |
| Subsidio para el empleo   | Dependientes (si aplica)             | Beneficios Exentos                  |
| [__________]             | [__________]                           | [__________]                       |
+--------------------------------------------------------------------------------------------------------+
| BONO ANUAL                                                                                             |
|                                                                                                        |
| % del Bono               | Valor Calculado (fijo)                | Incidencias del Bono                |
| [__________]             | [__________] (no editable)             | [Picklist ▼]                       |
+--------------------------------------------------------------------------------------------------------+

PICKLISTS MÉXICO:
- Estado:  
  • CDMX  
  • Estado de México  
  • Jalisco  
  • Nuevo León  
  • Puebla  
  • Otros (lista completa no código final)

- Tipo de Contrato:
  • Tiempo Indeterminado  
  • Tiempo Determinado  
  • Honorarios (sin prestaciones)

- Frecuencia Anual:
  • 12 + Aguinaldo (Aguinaldo = 15 días base legal)

- Incidencias del Bono:
  • Solo ISR  
  • ISR + IMSS  
  • Exento hasta tope legal  

TOOLTIPS:
- Otros Adicionales:
  “Incluye horas extras, comisiones, bonos recurrentes, trabajo nocturno.”
- Cuota Obrera:
  “Porcentaje descontado al trabajador según tablas del IMSS.”
- Riesgo de Trabajo:
  “Factor determinado por el patrón según clasificación del centro laboral.”
- Beneficios Exentos:
  “Prestaciones que reducen base gravable ISR (vales, despensa, etc.).”

FORMULÁRIO 6 — ESTADOS UNIDOS (USA)

+--------------------------------------------------------------------------------------------------------+
| LOCALIZAÇÃO E TIPO DE CONTRATO DE TRABALHO                                                             |
|                                                                                                        |
| País                     | Estado                                | Tipo de Contrato                    |
| [USA ▼]                  | [Picklist ▼]                          | [Picklist ▼]                        |
+--------------------------------------------------------------------------------------------------------+
| BASE DE CÁLCULO                                                                                        |
|                                                                                                        |
| Base Salary (Monthly)    | Annual Frequency (fixed)              | Other Earnings (tooltip)            |
| [__________]             | [12] (not editable)                   | [___________________________]       |
+--------------------------------------------------------------------------------------------------------+
| FEDERAL TAXES — IRS                                                                                    |
|                                                                                                        |
| Filing Status            | Dependents (IRS)                      | Additional Withholding              |
| [Picklist ▼]             | [__________]                           | [__________]                       |
+--------------------------------------------------------------------------------------------------------+
| SOCIAL SECURITY / MEDICARE (FICA)                                                                      |
|                                                                                                        |
| Social Security (6.2%)   | Medicare (1.45%)                       | Additional Medicare (0.9% >125k)   |
| [Auto]                   | [Auto]                                | [__________]                        |
+--------------------------------------------------------------------------------------------------------+
| STATE TAXES                                                                                            |
|                                                                                                        |
| State Income Tax Rate    | State Adjustments                     | Local/City Taxes (if any)           |
| [Auto or Picklist ▼]     | [__________]                           | [__________]                       |
+--------------------------------------------------------------------------------------------------------+
| BONUS ANUAL                                                                                            |
|                                                                                                        |
| Annual Bonus %           | Calculated Value (fixed)              | Bonus Taxation Rules                |
| [__________]             | [__________] (not editable)            | [Picklist ▼]                       |
+--------------------------------------------------------------------------------------------------------+

PICKLISTS — ESTADOS UNIDOS:

- Estado:
  • Florida (no state tax)
  • Texas (no state tax)
  • Nevada (no state tax)
  • Washington (no state tax)
  • Tennessee (limited tax)
  • New York
  • California
  • New Jersey
  • Illinois
  • Massachusetts
  • (lista completa no código final)

- Tipo de Contrato:
  • Full-time (W2)
  • Part-time (W2)
  • Contractor (1099, sem FICA patronal)

- Filing Status (IRS):
  • Single
  • Married Filing Jointly
  • Married Filing Separately
  • Head of Household

- Bonus Taxation:
  • Flat IRS Supplemental Rate (22%)
  • Flat IRS High Earner Rate (37% > 1M)
  • Combined Federal + State
  • Employer Custom Rule

TOOLTIPS:

- Other Earnings:
  “Include overtime, shift differentials, commissions, hazard pay.”
- Dependents (IRS):
  “For Child Tax Credit or other deductions.”
- State Tax Rate:
  “Some states use flat tax; others use progressive tables.”

FORMULÁRIO 7 — CANADÁ

+--------------------------------------------------------------------------------------------------------+
| LOCALIZAÇÃO E TIPO DE CONTRATO DE TRABALHO                                                             |
|                                                                                                        |
| País                     | Província                              | Tipo de Contrato                   |
| [Canadá ▼]               | [Picklist ▼]                           | [Picklist ▼]                       |
+--------------------------------------------------------------------------------------------------------+
| BASE DE CÁLCULO                                                                                        |
|                                                                                                        |
| Base Salary (Monthly)    | Annual Frequency (fixed)               | Other Earnings (tooltip)           |
| [__________]             | [12] (not editable)                    | [___________________________]      |
+--------------------------------------------------------------------------------------------------------+
| FEDERAL TAXES – CANADA REVENUE AGENCY (CRA)                                                            |
|                                                                                                        |
| Federal Tax Credits      | Dependents CRA                         | Additional Withholding             |
| [__________]             | [__________]                           | [__________]                       |
+--------------------------------------------------------------------------------------------------------+
| PROVINCIAL TAXES                                                                                       |
|                                                                                                        |
| Provincial Tax Rate      | Provincial Credits                     | Additional Provincial Adj.         |
| [Auto / Picklist ▼]      | [__________]                           | [__________]                       |
+--------------------------------------------------------------------------------------------------------+
| CANADIAN PENSION PLAN (CPP/QPP) + EMPLOYMENT INSURANCE (EI)                                            |
|                                                                                                        |
| CPP/QPP (%)              | EI (%)                                 | Additional EI (if any)             |
| [Auto]                   | [Auto]                                 | [__________]                       |
+--------------------------------------------------------------------------------------------------------+
| BONUS ANUAL                                                                                            |
|                                                                                                        |
| Annual Bonus %           | Calculated Value (fixed)               | Bonus Taxation Rules               |
| [__________]             | [__________] (not editable)             | [Picklist ▼]                      |
+--------------------------------------------------------------------------------------------------------+

PICKLISTS — CANADÁ:

- Província:
  • Ontario  
  • British Columbia  
  • Alberta  
  • Québec (usa QPP, não CPP)  
  • Manitoba  
  • Saskatchewan  
  • Nova Scotia  
  • New Brunswick  
  • Prince Edward Island  
  • Newfoundland & Labrador  
  • Northwest Territories  
  • Yukon  
  • Nunavut  

- Tipo de Contrato:
  • Full-time Employment  
  • Part-time Employment  
  • Contractor (T4A / sem EI padrão)  

- Incidências do Bônus:
  • Apenas Federal  
  • Federal + Provincial  
  • Federal + Provincial + CPP/EI  
  • Exento (apenas em casos específicos)  

TOOLTIPS:

- Other Earnings:
  “Include overtime, commissions, premiums, retroactive pay.”  
- Federal Tax Credits:
  “Basic Personal Amount e demais créditos permitidos pela CRA.”  
- Provincial Tax Rate:
  “Cada província tem tabela própria, progressiva.”  
- CPP/QPP:
  “Contribuição obrigatória conforme faixa salarial anual.”  
- EI:
  “Seguro de emprego com teto anual fixado pela CRA.”

INFORMAÇÕES ADICIONAIS — VALORES DO EMPREGADO RECEBIDOS EM CASO DE DESLIGAMENTO

Os valores abaixo NÃO fazem parte da remuneração mensal líquida,
mas pertencem ao empregado e ficam acumulados para recebimento
em situações específicas, como desligamento, aposentadoria ou resgate.
Devem ser exibidos logo abaixo das Tabelas de Remuneração Mensal e Anual.

Esses itens variam conforme a legislação de cada país:

• BRASIL
  - **FGTS acumulado**: depósitos mensais equivalentes a 8% do salário
    (valor pertence ao empregado para saque em demissão, aposentadoria,
     compra de imóvel, doenças graves, etc.)
  - **Previdência Privada (se contratada)**: contribuições do empregado
    e do empregador acumuladas no plano.

• CHILE
  - **Saldo AFP individual**: contribuição do empregado + SIS patronal.
  - **Fundo de Saúde (ISAPRE/FONASA)** quando houver valores acumulados
    em excedentes (dependendo do plano).

• ARGENTINA
  - **Fondo de Jubilación** acumulado no sistema previsional.
  - **Aportes voluntários** a previdência privada (quando existir).

• COLÔMBIA
  - **Fundo de Pensión**: saldos acumulados do sistema contributivo.
  - **Cesantías (Fundo de Cesantías)**: valor anual depositado pelo empregador
    e que pertence ao empregado para resgate em demissão, educação ou moradia.

• MÉXICO
  - **AFORE**: conta individual de aposentadoria (obrigatória), com
    aportes do empregado + empregador + governo.
  - **Infonavit**: saldo acumulado na conta vinculada (em alguns casos).

• ESTADOS UNIDOS
  - **401(k), 403(b), IRA**: contribuições do empregado e matching do empregador
    (quando existir), pertencentes ao empregado.
  - **HSA (Health Savings Account)**: valores acumulados e resgatáveis.

• CANADÁ
  - **RRSP / Group RRSP**: aportes do empregado e contribuições do empregador.
  - **Pension Plans** (employer-sponsored): valores acumulados no plano.

**Observação:**
Esses valores NÃO entram no cálculo da remuneração líquida mensal,
mas devem aparecer de forma informativa, pois representam benefícios
financeiros que pertencem ao empregado e podem ser resgatados futuramente.


────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 5 — fluxo completo do cálculo (bruto → líquido)
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

O fluxo de cálculo da Página 01 segue uma cadeia fixa e padronizada
para TODOS os países, com adaptações por legislação local.
A ordem nunca muda; apenas as fórmulas variam por país.

A seguir está o fluxo oficial que o código Python DEVE implementar.

5.1 ETAPA 1 — CAPTURA DOS VALORES DO FORMULÁRIO

O app coleta:
- salário base mensal
- frequência anual do país (fixa ou variável)
- adicionais
- descontos obrigatórios
- previdência social
- previdência privada
- dependentes
- pensão (quando aplicável)
- informações fiscais do país
- percentual de bônus anual

Todos os valores são convertidos para FLOAT e armazenados em um dicionário:

calculo = {
    "salario_base": ...,
    "frequencia": ...,
    "adicionais": ...,
    "descontos": ...,
    "dependentes": ...,
    "pensao": ...,
    "bonus_percentual": ...,
}

5.2 ETAPA 2 — SALÁRIO MENSAL BRUTO

SALÁRIO MENSAL BRUTO = salário base + adicionais

5.3 ETAPA 3 — SALÁRIO ANUAL BRUTO

SALÁRIO ANUAL BRUTO = salário base × frequência anual

5.4 ETAPA 4 — CÁLCULO DO BÔNUS ANUAL

VALOR DO BÔNUS = (percentual_bonus / 100) × salário anual bruto

5.5 ETAPA 5 — PREVIDÊNCIA / SEGURIDADE SOCIAL DO EMPREGADO

Depende de cada país:
- Brasil → INSS progressivo
- Chile → AFP + Salud
- Argentina → Jubilación + Obra Social
- Colômbia → Salud + Pensión
- México → IMSS
- EUA → FICA
- Canadá → CPP/QPP + EI

5.6 ETAPA 6 — CÁLCULO DO IMPOSTO DE RENDA

Cada país usa sua própria tabela fiscal.

5.7 ETAPA 7 — DESCONTOS ADICIONAIS

Inclui:
- pensão alimentícia
- vales
- seguros
- empréstimos
- benefícios opcionais

5.8 ETAPA 8 — SALÁRIO LÍQUIDO MENSAL

salario_liquido_mensal =
    salario_mensal_bruto
  - previdencia_empregado
  - imposto_renda
  - descontos_adicionais

5.9 ETAPA 9 — SALÁRIO LÍQUIDO ANUAL

SALÁRIO LÍQUIDO ANUAL = salário líquido mensal × frequência anual

5.10 ETAPA 10 — COMPOSIÇÃO DA REMUNERAÇÃO ANUAL

%_salario = salario_anual_bruto / total_remuneracao  
%_bonus   = valor_bonus_anual / total_remuneracao  

FIM DA SEÇÃO 5 — FLUXO COMPLETO DO CÁLCULO

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 6 — tabelas de saída (mensal, anual, composição)
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

As três tabelas seguem o layout padrão definido no 00_Layout_Global.md.
Cada tabela contém 3 colunas: Descrição | % | Valor.

6.1 TABELA — REMUNERAÇÃO MENSAL

Título: REMUNERAÇÃO MENSAL

+--------------------------------------------------------------+
| Descrição                         |   %   |       Valor       |
+--------------------------------------------------------------+
| Salário Base                      |  xx   |   R$ XXXX,XX      |
| Outros Adicionais (créditos)      |  xx   |   R$ XXXX,XX      |
| Imposto de Renda (débitos)        |  xx   |  -R$ XXXX,XX      |
| Previdência Social (débitos)      |  xx   |  -R$ XXXX,XX      |
| Outros Descontos (débitos)        |  xx   |  -R$ XXXX,XX      |
+--------------------------------------------------------------+
| REMUNERAÇÃO MENSAL LÍQUIDA        |  xx   |   R$ XXXX,XX      |
+--------------------------------------------------------------+

Informações adicionais (fora da tabela):
• FGTS (Brasil): R$ XXXX,XX  
• Previdência privada: R$ XXXX,XX  
• Contribuições patronais (quando aplicável)

6.2 TABELA — REMUNERAÇÃO ANUAL

Título: REMUNERAÇÃO ANUAL

+--------------------------------------------------------------+
| Descrição                         |   %   |       Valor       |
+--------------------------------------------------------------+
| Salário Anual Bruto               |  xx   |   R$ XXXX,XX      |
| Impostos Anuais                   |  xx   |  -R$ XXXX,XX      |
| Contribuições Previdenciárias     |  xx   |  -R$ XXXX,XX      |
+--------------------------------------------------------------+
| REMUNERAÇÃO ANUAL LÍQUIDA         |  xx   |   R$ XXXX,XX      |
+--------------------------------------------------------------+

6.3 TABELA — COMPOSIÇÃO DA REMUNERAÇÃO

Título: COMPOSIÇÃO DA REMUNERAÇÃO ANUAL

+--------------------------------------------------------------+
| Descrição                         |   %   |       Valor       |
+--------------------------------------------------------------+
| Salário Anual                     |  xx   |   R$ XXXX,XX      |
| Bônus Anual                       |  xx   |   R$ XXXX,XX      |
+--------------------------------------------------------------+
| TOTAL REMUNERAÇÃO ANUAL           | 100%  |   R$ XXXX,XX      |
+--------------------------------------------------------------+


────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 7 — glossário técnico
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

• Salário base — Remuneração mensal fixa antes de adicionais.  
• Frequência anual — Multiplicador que define o salário anual.  
• Adicionais — Ganhos extras como horas extras, comissões etc.  
• Descontos obrigatórios — Tributos e previdência social.  
• Remuneração líquida — Valor após todos descontos.  
• FGTS (Brasil) — Depósito do empregador (informativo).  
• FICA (EUA) — Social Security + Medicare.  
• CPP/QPP (Canadá) — Contribuição previdenciária.  
• EI (Canadá) — Seguro-desemprego.  
• ISR (México) — Imposto sobre la Renta.  
• AFP (Chile) — Previdência privada obrigatória.  
• Ganancias (Argentina) — Imposto de renda argentino.  
• Retención en la fuente (Colômbia) — IR retido na fonte.  


────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Seção 8 — dependências do layout global
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

A Página 01 herda:

1. **Tipografia** — Todas as labels e textos usam os padrões definidos.  
2. **Containers** — O formulário está dentro de um container de 120 colunas.  
3. **Botão Principal** — “Calcular Remuneração” estilizado pelo CSS global.  
4. **Tabelas** — Todas renderizam segundo as classes .result-table.  
5. **Título + Bandeira** — Exibição dinâmica conforme o país selecionado.  
6. **Sidebar** — Idiomas e navegação.  
7. **Cores** — Azul para créditos, vermelho para débitos, linha final verde-escura.

FIM DAS SEÇÕES 6, 7 E 8
