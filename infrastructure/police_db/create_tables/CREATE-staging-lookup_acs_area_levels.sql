DROP TABLE IF EXISTS staging.lookup_acs_area_levels;
CREATE TABLE staging.lookup_acs_area_levels (
  code        INT PRIMARY KEY, --
  value       VARCHAR, --
  description VARCHAR, --
  parent_code INT                 --
);
