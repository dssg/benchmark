DROP TABLE IF EXISTS staging.officer_addresses;
CREATE  TABLE staging.officer_addresses (
	entity_id          		int references staging.officers_hub(entity_id) on delete cascade,  	--officer id
	address_id        			int,                																--unique id for the address
	address_raw         		varchar,            															 	--raw address string
	miles_to_assignment			numeric,																								--distance to assigned post from home address
	last_modified						timestamp																						--date row last modified
);
