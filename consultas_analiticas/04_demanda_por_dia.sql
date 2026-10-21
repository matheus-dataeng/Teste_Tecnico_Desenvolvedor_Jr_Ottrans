--DEMANDA POR DIA EM JANEIRO

SELECT
    data_movimento_jan,
    SUM(demanda_jan) AS demanda_total_jan
FROM demanda_janeiro_2022
GROUP BY data_movimento_jan
ORDER BY data_movimento_jan ASC;

--DEMANDA POR DIA EM FEVEREIRO

SELECT
    data_movimento_fev,
    SUM(demanda_fev) AS demanda_total_fev
FROM demanda_fevereiro_2022
GROUP BY data_movimento_fev
ORDER BY data_movimento_fev ASC;

