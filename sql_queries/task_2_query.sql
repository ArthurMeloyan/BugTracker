WITH RankedDevelopers AS (
  SELECT team, developer, task_count,
         ROW_NUMBER() OVER (PARTITION BY team ORDER BY task_count) AS rn
  FROM developers
)
SELECT team, developer, task_count
FROM RankedDevelopers
WHERE rn = 1;
