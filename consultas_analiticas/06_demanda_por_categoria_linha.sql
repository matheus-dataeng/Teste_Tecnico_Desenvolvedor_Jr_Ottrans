-- DEMANDA TOTAL DE ESTUDANTES EM JANEIRO DE 2022
SELECT 
    SUM(demanda_jan) AS demanda_total_jan,
    nome_passageiro_jan,
    tipo_passageiro_jan
FROM demanda_janeiro_2022
GROUP BY nome_passageiro_jan,tipo_passageiro_jan
HAVING tipo_passageiro_jan = 3;

-- DEMANDA TOTAL DE ESTUDANTES EM FEVEREIRO DE 2022

SELECT 
    SUM(demanda_fev) AS demanda_total_fev,
    nome_passageiro_fev,
    tipo_passageiro_fev
FROM demanda_fevereiro_2022
GROUP BY nome_passageiro_fev,tipo_passageiro_fev
HAVING tipo_passageiro_fev = 3;
