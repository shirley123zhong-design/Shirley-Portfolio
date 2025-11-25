SELECT TOP 10 * FROM sets;
SELECT TOP 10 * FROM themes;

/* Counts how many LEGO sets were released for each theme 
in a specific year.*/
SELECT 
    s.year,
    t.name AS theme,
    COUNT(*) AS num_sets
FROM dbo.sets s
JOIN dbo.themes t 
    ON s.theme_id = t.id
GROUP BY 
    s.year,
    t.name
ORDER BY 
    s.year,
    t.name;

/*Calculate Year-on-Year Theme Growth (SQL Trend Analysis)
Is a theme growing or declining?
Which themes have rising popularity?
Which themes peaked then dropped?
How fast is each theme expanding?*/
WITH theme_year AS (
    SELECT 
        s.year,
        t.name AS theme,
        COUNT(*) AS num_sets
    FROM sets s
    JOIN themes t 
        ON s.theme_id = t.id
    GROUP BY s.year, t.name
),
with_lag AS (
    SELECT
        year,
        theme,
        num_sets,
        LAG(num_sets) OVER (PARTITION BY theme ORDER BY year) AS prev_num_sets
    FROM theme_year
)
SELECT
    year,
    theme,
    num_sets,
    prev_num_sets,
    (num_sets - prev_num_sets) AS abs_change,
    CASE 
        WHEN prev_num_sets IS NULL OR prev_num_sets = 0 THEN NULL
        ELSE ROUND(100.0 * (num_sets - prev_num_sets) / prev_num_sets, 2)
    END AS pct_change
FROM with_lag
ORDER BY theme, year;
/* top grownth theme*/
WITH theme_year AS (
    SELECT 
        s.year,
        t.name AS theme,
        COUNT(*) AS num_sets
    FROM sets s
    JOIN themes t 
        ON s.theme_id = t.id
    GROUP BY s.year, t.name
),
with_lag AS (
    SELECT
        year,
        theme,
        num_sets,
        LAG(num_sets) OVER (PARTITION BY theme ORDER BY year) AS prev_num_sets
    FROM theme_year
),
growth AS (
    SELECT
        year,
        theme,
        num_sets,
        prev_num_sets,
        (num_sets - prev_num_sets) AS abs_change,
        CASE 
            WHEN prev_num_sets IS NULL OR prev_num_sets = 0 THEN NULL
            ELSE ROUND(100.0 * (num_sets - prev_num_sets) / prev_num_sets, 2)
        END AS pct_change
    FROM with_lag
)
SELECT TOP 10
    theme,
    year,
    num_sets,
    prev_num_sets,
    abs_change,
    pct_change
FROM growth
WHERE pct_change IS NOT NULL
ORDER BY pct_change DESC;

/* Top Themes by Total Sets Released*/
SELECT 
    t.name AS theme,
    COUNT(*) AS total_sets
FROM sets s
JOIN themes t 
    ON s.theme_id = t.id
GROUP BY t.name
ORDER BY total_sets DESC;

/*What % of LEGO’s total yearly product portfolio 
was contributed by each theme?*/
WITH theme_year AS (
    SELECT 
        s.year,
        t.name AS theme,
        COUNT(*) AS num_sets
    FROM sets s
    JOIN themes t 
        ON s.theme_id = t.id
    GROUP BY s.year, t.name
),
year_total AS (
    SELECT 
        year,
        SUM(num_sets) AS total_sets_year
    FROM theme_year
    GROUP BY year
)
SELECT 
    ty.year,
    ty.theme,
    ty.num_sets,
    yt.total_sets_year,
    ROUND(100.0 * ty.num_sets / yt.total_sets_year, 2) AS pct_of_portfolio
FROM theme_year ty
JOIN year_total yt
    ON ty.year = yt.year
ORDER BY 
    ty.year ASC,            
    pct_of_portfolio ASC;  

/*How often does lego release a new theme and when is the new theme released year*/
/*How many new themes did LEGO introduce each year?*/
WITH theme_year AS (
    SELECT 
        s.year,
        t.name AS theme
    FROM dbo.sets s
    JOIN dbo.themes t 
        ON s.theme_id = t.id
    GROUP BY s.year, t.name
),
first_year AS (
    SELECT 
        theme,
        MIN(year) AS first_year
    FROM theme_year
    GROUP BY theme
)
SELECT 
    first_year AS year,
    COUNT(*) AS new_themes_launched
FROM first_year
GROUP BY first_year
ORDER BY year;



/* create a table combing every info we have calculated before
so we will be able to use it later in python or powerBI*/
-- If you already created this view before, drop it first:
-- Drop the view first if it already exists
IF OBJECT_ID('dbo.vw_theme_year_stats', 'V') IS NOT NULL
    DROP VIEW dbo.vw_theme_year_stats;
GO

CREATE VIEW dbo.vw_theme_year_stats
AS
-- Base: sets per theme per year
WITH theme_year AS (
    SELECT 
        s.year,
        t.name AS theme,
        COUNT(*) AS num_sets
    FROM dbo.sets s
    JOIN dbo.themes t 
        ON s.theme_id = t.id
    GROUP BY s.year, t.name
),

-- Year-on-year comparison
with_lag AS (
    SELECT
        year,
        theme,
        num_sets,
        LAG(num_sets) OVER (PARTITION BY theme ORDER BY year) AS prev_num_sets
    FROM theme_year
),

-- Total sets per year (all themes combined)
year_total AS (
    SELECT 
        year,
        SUM(num_sets) AS total_sets_year
    FROM theme_year
    GROUP BY year
),

-- First year each theme appears (launch year)
first_year AS (
    SELECT 
        theme,
        MIN(year) AS first_year
    FROM theme_year
    GROUP BY theme
),

-- How many new themes were launched each year
new_theme_count AS (
    SELECT 
        first_year AS year,
        COUNT(*) AS new_themes_launched
    FROM first_year
    GROUP BY first_year
)

SELECT
    wl.year,
    wl.theme,
    wl.num_sets,
    wl.prev_num_sets,
    (wl.num_sets - wl.prev_num_sets) AS abs_change,
    CASE 
        WHEN wl.prev_num_sets IS NULL OR wl.prev_num_sets = 0 THEN NULL
        ELSE ROUND(100.0 * (wl.num_sets - wl.prev_num_sets) / wl.prev_num_sets, 2)
    END AS pct_change,
    yt.total_sets_year,
    ROUND(100.0 * wl.num_sets / yt.total_sets_year, 2) AS pct_of_portfolio,
    CASE 
        WHEN wl.year = fy.first_year THEN 1 
        ELSE 0 
    END AS is_new_theme_year,           
    nt.new_themes_launched              -- how many themes launched in that year (same for all rows that year)
FROM with_lag wl
JOIN year_total yt
    ON wl.year = yt.year
LEFT JOIN first_year fy
    ON wl.theme = fy.theme
LEFT JOIN new_theme_count nt
    ON wl.year = nt.year;
GO

/* test*/
SELECT TOP 100 *
FROM dbo.vw_theme_year_stats
ORDER BY year, pct_of_portfolio DESC;
