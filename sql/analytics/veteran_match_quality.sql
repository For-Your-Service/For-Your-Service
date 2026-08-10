-- Veteran Match Quality Analytics
-- Analyze match quality and success metrics

-- Top matches by veteran
SELECT 
    veteran_id,
    veteran_name,
    COUNT(*) as total_matches,
    AVG(match_score) as avg_match_score,
    MAX(match_score) as best_match_score,
    MIN(match_score) as lowest_match_score
FROM veteran_intake.gold_matches
WHERE match_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY veteran_id, veteran_name
ORDER BY avg_match_score DESC
LIMIT 100;

-- Match score distribution
SELECT 
    FLOOR(match_score * 10) / 10 as score_bucket,
    COUNT(*) as match_count,
    COUNT(DISTINCT veteran_id) as unique_veterans
FROM veteran_intake.gold_matches
WHERE match_date >= CURRENT_DATE - INTERVAL 7 DAYS
GROUP BY score_bucket
ORDER BY score_bucket DESC;

-- Daily match volume trend
SELECT 
    match_date,
    COUNT(DISTINCT veteran_id) as veterans_matched,
    COUNT(*) as total_matches,
    AVG(match_score) as avg_score
FROM veteran_intake.gold_matches
WHERE match_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY match_date
ORDER BY match_date DESC;
