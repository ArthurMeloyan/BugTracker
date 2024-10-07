SELECT s.name, s.length
FROM streets s
JOIN houses h ON s.id = h.street_id
GROUP BY s.id, s.name, s.length
HAVING SUM(h.tenants) < 500
ORDER BY s.length DESC
LIMIT 3;
