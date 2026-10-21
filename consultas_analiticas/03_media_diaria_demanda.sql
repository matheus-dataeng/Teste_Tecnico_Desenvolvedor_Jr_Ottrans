SELECT 
    ROUND(
        SUM(demanda_jan) / COUNT(DISTINCT data_movimento_jan), 2
    ) AS media_demanda_diaria_jan
FROM demanda_janeiro_2022;

SELECT 
    ROUND(
        SUM(demanda_fev) / COUNT(DISTINCT data_movimento_fev), 2
    ) AS media_demanda_diaria_fev
FROM demanda_fevereiro_2022;

