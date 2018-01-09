# coding: utf-8

import os

import boto3
import s3fs

import click
import yaml
import sqlalchemy
import datetime

from catwalk.storage import FSModelStorageEngine, S3ModelStorageEngine
from triage.experiments import MultiCoreExperiment


import logging

logging_level = logging.DEBUG

logging.basicConfig(
    format="%(name)-30s  %(asctime)s %(levelname)10s %(process)6d  %(filename)-24s  %(lineno)4d: %(message)s",
    datefmt = "%d/%m/%Y %I:%M:%S %p",
    level=logging_level,
    handlers=[logging.StreamHandler()]
)


@click.command()
@click.option('--experiment-file', type=click.Path(),
              help="Triage's experiment configuration file")
@click.option('--output-path',
              type=click.Path(),
              help="Triage's output path (For storing matrices and trained models)")
def run_experiment(experiment_file, output_path):

    start_time = datetime.datetime.now()
    logging.info(f"Reading the file experiment file {experiment_file}")

    # Load the experiment file
    s3 = s3fs.S3FileSystem()
    with s3.open(experiment_file, 'rb') as f:
        experiment_config = yaml.load(f.read())

    host = os.environ['POSTGRES_HOST']
    user = os.environ['POSTGRES_USER']
    db = os.environ['POSTGRES_DB']
    password = os.environ['POSTGRES_PASSWORD']
    port = os.environ['POSTGRES_PORT']

    db_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"

    logging.info(f"Using the database: postgresql://{user}:XXXXX@{host}:{port}/{db}")

    try:
        n_processes = int(os.environ.get('NUMBER_OF_PROCESSES', 12))
    except ValueError:
        n_processes = 12
    try:
        n_db_processes = int(os.environ.get('NUMBER_OF_DB_PROCESSES', 6))
    except ValueError:
        n_db_processes = 6

    logging.info(f"The experiment will use {n_processes} cores in the host")

    logging.info(f"Creating experiment object")

    experiment = MultiCoreExperiment(
        n_processes=n_processes,
        n_db_processes=n_db_processes,
        config=experiment_config,
        db_engine=sqlalchemy.create_engine(db_url),
        model_storage_class=S3ModelStorageEngine,
        project_path=output_path
    )

    logging.info(f"Experiment created: all the file permissions, and db connections are OK")

    logging.debug(f"Experiment configuration: {experiment.config}")

    logging.info(f"Running the experiment")
    experiment.run()
    end_time = datetime.datetime.now()

    logging.info(f"Experiment {experiment_file} completed in {end_time - start_time} seconds")

    with s3.open(os.path.join(output_path, "_SUCCESS"), 'wb') as sf:
        sf.write(datetime.date.today().strftime('%Y-%m-%d'))
        sf.write(f"Experiment {experiment_file} completed in {end_time - start_time} seconds")

    print("Done!")


if __name__ == '__main__':
    run_experiment()
