CREATE TABLE ipl_matches (
    mid INT,
    date DATE,
    venue VARCHAR(100),
    bat_team VARCHAR(100),
    bowl_team VARCHAR(100),
    batsman VARCHAR(100),
    bowler VARCHAR(100),
    runs INT,
    wickets INT,
    overs DECIMAL(4,1),
    runs_last_5 INT,
    wickets_last_5 INT,
    striker INT,
    non_striker INT,
    total INT
);
select * from ipl_matches;
-- copy
-- ipl_matches(mid,date,venue,bat_team,bowl_team,batsman,bowler,runs,wickets,overs,runs_last_5,wickets_last_5,striker,non_striker,total)
-- FROM '‪C:\ipl_data.csv'
-- DELIMITER ','
-- CSV HEADER;

SELECT batsman, SUM(runs) as total_runs
FROM ipl_matches
GROUP BY batsman
ORDER BY total_runs DESC
LIMIT 10;


SELECT bowler, SUM(wickets) as total_wickets
FROM ipl_matches
GROUP BY bowler
ORDER BY total_wickets DESC
LIMIT 10;


SELECT SUBSTR(date, -4) as season, SUM(runs) as total_runs_per_season
FROM ipl_matches
GROUP BY season
ORDER BY season;

SELECT venue, SUM(runs) as total_runs
FROM ipl_matches
GROUP BY venue
ORDER BY total_runs DESC
LIMIT 5;

--HAR SEASON KE TOP 3 PLAYER
SELECT season, batsman, total_runs, rank
FROM (
    SELECT 
        EXTRACT(YEAR FROM date) as season,
        batsman,
        SUM(runs) as total_runs,
        ROW_NUMBER() OVER (PARTITION BY EXTRACT(YEAR FROM date) ORDER BY SUM(runs) DESC) as rank
    FROM ipl_matches
    GROUP BY EXTRACT(YEAR FROM date), batsman
) ranked
WHERE rank <= 3
ORDER BY season, rank;

-- PER SEASON TOTAL RUNS
SELECT 
    EXTRACT(YEAR FROM date) as season,
    SUM(runs) as total_runs_per_season
FROM ipl_matches
GROUP BY EXTRACT(YEAR FROM date)
ORDER BY season;

-- PER SEASON TOP 5 BOLWER
SELECT season, bowler, total_wickets, rank
FROM (
    SELECT 
        EXTRACT(YEAR FROM date) as season,
        bowler,
        SUM(wickets) as total_wickets,
        ROW_NUMBER() OVER (PARTITION BY EXTRACT(YEAR FROM date) ORDER BY SUM(wickets) DESC) as rank
    FROM ipl_matches
    GROUP BY EXTRACT(YEAR FROM date), bowler
) ranked
WHERE rank <= 5
ORDER BY season, rank;