# Benchmark EIS
Repository for code that will be given to Benchmark Analytics

## Infrastructure

- A dummy PostgreSQL database with simulated data in `staging` schema. It is provided inside a docker container (This is not intended for production purposes),

- [Triage v2.20](https://github.com/dssg/triage/releases/tag/v2.2.0) is also dockerized. This version could be used in production.

## Running Benchmark EIS

Everything is controled from [`benchmark.sh`](benchmark.sh) script.

The help could be call with

```
./benchmark.sh --help
```

### Creating dummy database

Building the Docker images (This will create the images `benchmark/police_db` and `benchmark/triage_experiment`)

```
./benchmark.sh build
```

Run the database

```
./benchmark.sh start
```

Check that everything is running:

```
.benchmark.sh status
```

### Connecting to the database

You can connect to the `police_db` database using the following URL

```
postgresql://benchmark_user:some_password@0.0.0.0:5434/police_db
```

(The password is set in `.env` file. If you change it you need to recreate this database with `./benchmark.sh rebuild`)

For example using `psql`:

```
psql postgresql://benchmark_user:some_password@0.0.0.0:5434/police_db
```

### Preparing the database for running the experiment

Triage requires two tables besides `staging` and both are expected in the configuration file

- A table that indicates the date, the officer, the *outcome* of that
date (i.e. if the officer had an adverse incident or not). You should
put the full qualified table name in `events` in the config file. This
table will be use for transform the *outcomes* in *labels* (the label
is controlled with `test_label_span` in the config file too)
  NOTE: *In the dummy database it is `triage.outcomes_active_officers`*
  
- A table that indicates the time window in which the entity is in a particular state. You should put the full qualified table name in `state` in the config file
  NOTE: *In the dummy database it is `triage.states`*
  NOTE: If your **real** data has a table with hiring date, end date or anything similar you can use that for populate this table.
  NOTE: The *state* in the example data is just `active` but you can
  create a more complex set of states (like *active*, *flagged*,
  *action performed* etc)
  
This tables **aren't** created in `staging` you should run the
`sql/outcomes_triage.sql` file for creating them.

If you are using `psql` you can do:

```
psql postgresql://benchmark_user:some_password@0.0.0.0:5434/police_db -a -f sql/outcomes_triage.sql
```

You should have now both tables in your database.

### Running experiments

The `benchmark/triage` docker image assumes shares with the **host** (your laptop or the AWS EC2) the directory `triage`. 

Every  *experiment config* file should be put inside the `triage/experiment_config` directory.

The output (matrices and trained `sklearn` models) of the experiment will be stored in `triage/output` directory.

   Validate experiment configuration file (recommended)
   
        $ ./benchmark.sh -t --config_file sample_experiment_config.yaml validate

   Show experiment's temporal cross-validation blocks (the image will be store in `triage/`):
   
        $ ./benchmark.sh -t --config_file sample_experiment_config.yaml show_temporal_blocks

   Run one experiment:
   
        $ ./benchmark.sh -t --config_file sample_experiment_config.yaml run

   Triage help:
   
        $ ./benchmark.sh -t --help

Obviously, you could change `sample_experiment_config.yaml` file with your own.


## Experiment config file 

A sample is in this repo [sample_experiment_config.yaml](triage/experiment_config/sample_experiment_config.yaml)

## Original source code

- [Police EIS](https://github.com/dssg/police-eis)
- [Triage](https://github.com/dssg/triage)

We will add code from other police projects in this repo.

## Create staging schemas and tables
https://github.com/dssg/police-eis/tree/master/schemas

## Get triage
Latest version will be at https://github.com/dssg/triage 
Frozen working version compatabile with provided config files is https://github.com/dssg/triage/releases/tag/v2.2.0

