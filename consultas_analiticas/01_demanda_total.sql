-- DEMANDA TOTAL JANEIRO
SELECT
    ROUND(SUM(demanda_jan), 2) AS demanda_total_jan
FROM demanda_janeiro_2022;

--DEMANDA TOTAL FEVEREIRO
SELECT
    ROUND(SUM(demanda_fev), 2) AS demanda_total_fev
FROM demanda_fevereiro_2022;
