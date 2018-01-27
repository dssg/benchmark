DROP TABLE IF EXISTS staging.acs_shapefiles;
CREATE TABLE staging.acs_shapefiles (
  acs_area_id              INT, --Census (ACS) Block Group Id
  acs_area_level_code      VARCHAR, --ACS Block Group
  acs_area_valid_from_date INT, --Year of ACS Data
  parent_acs_area_id       VARCHAR, --Census (ACS) Id for chosen ACS area level, such as census tract id
  acs_area_name            VARCHAR, --?
  acs_area_description     VARCHAR, --?
  acs_area_geometry        FLOAT, --?
  acs_projection_type      VARCHAR             --?
);
