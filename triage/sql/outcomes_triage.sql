CREATE SCHEMA if not exists triage;

DROP TABLE IF EXISTS triage.outcomes;

-- This table represents the date in which the officer 
-- made an action that was found as adverse (final ruling code 1,4,5)
CREATE TABLE triage.outcomes AS (
    SELECT
    entity_id                      AS entity_id,
    event_datetime                  AS outcome_date,
    CASE
    WHEN final_ruling_code in (1,4,5)
    THEN true
    ELSE false
    END                             AS outcome
    FROM staging.incidents);

DROP TABLE IF EXISTS triage.outcomes_daily;
DROP TABLE IF EXISTS triage.daily_outcomes;

-- This is an intermediate table for creating the dense table
CREATE TABLE triage.daily_outcomes AS (
       WITH officers as (
       SELECT distinct(entity_id) as entity_id
       FROM staging.events_hub)
       SELECT entity_id, outcome_date from officers 
       CROSS JOIN 
       generate_series('2000-01-01'::date,
       '2017-07-25'::date,
       '1 day'::interval)
       outcome_date);

CREATE TABLE triage.outcomes_daily AS (
       with sub as (
       SELECT entity_id, outcome_date, COALESCE(outcome, 'f') as outcome,
       row_number() over w as rn 
       from triage.daily_outcomes o 
       LEFT JOIN triage.outcomes 
       USING (entity_id, outcome_date)
       window w as (partition by entity_id, outcome_date order by outcome desc)
       )

 SELECT entity_id, outcome_date, outcome
       from sub where rn=1
    );  

-- This is the dense table: each officer, per each day in the modeling
-- time window.
CREATE TABLE triage.outcomes_active_officers AS
       SELECT f.entity_id, f.outcome_date, f.outcome
       FROM triage.outcomes_daily AS f,
       LATERAL
       (
                SELECT 1
                FROM staging.events_hub AS e
                WHERE f.entity_id = e.entity_id
                AND e.event_datetime + INTERVAL '1 year' > f.outcome_date
                AND e.event_datetime <= f.outcome_date
        LIMIT 1
) sub ;


DROP TABLE IF EXISTS triage.states;

-- Finally the states table, it just specifies 
-- which officers are active in a period of time
CREATE TABLE triage.states AS (
       SELECT
       entity_id,
       'active'::text AS state,
       min(outcome_date) AS start_time,
       max(outcome_date) AS end_time
       FROM
       triage.outcomes_active_officers
       GROUP BY entity_id
);
