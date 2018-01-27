DROP TABLE IF EXISTS staging.officer_children; 
CREATE  TABLE staging.officer_children (
	entity_id                                                            int references staging.officers_hub(entity_id) on delete cascade,                --officer id
	number_of_children                                                    int,                --whether the officer has children
	last_modified                                                         timestamp           --date at which marital/child status changed
);
