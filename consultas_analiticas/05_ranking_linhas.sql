-- TOP 10 LINHAS JANEIRO

WITH demanda_por_codigo_linhas_jan AS (
    SELECT
        SUM(demanda_jan) AS demanda_total_jan,
        codigo_linha_jan
    FROM demanda_janeiro_2022
    GROUP BY codigo_linha_jan
)

SELECT 
    demanda_total_jan,
    codigo_linha_jan
FROM demanda_por_codigo_linhas_jan
ORDER BY demanda_total_jan DESC
LIMIT 10;

-- TOP 10 LINHAS FEVEREIRO

WITH demanda_por_codigo_linhas_fev AS (
    SELECT
        SUM(demanda_fev) AS demanda_total_fev,
        codigo_linha_fev
    FROM demanda_fevereiro_2022
    GROUP BY codigo_linha_fev
)

SELECT 
    demanda_total_fev,
    codigo_linha_fev
FROM demanda_por_codigo_linhas_fev
ORDER BY demanda_total_fev DESC
LIMIT 10;

