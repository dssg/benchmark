DROP TABLE IF EXISTS staging.officer_marital; 
CREATE  TABLE staging.officer_marital (
	entity_id                                                            int references staging.officers_hub(entity_id) on delete cascade,                --officer id
	marital_status_code                                                   int,                --officer marital status (never married, married, divorced, separated, widowed)
	last_modified                                                         timestamp           --date at which marital/child status changed
);
