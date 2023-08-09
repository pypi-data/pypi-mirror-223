import csv
import logging
import sys

import click

from chicagorecoverypy.schemas import AggregatePersonSchema
import chicagorecoverypy.utils as utils


logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


@click.command()
@click.option("--file", help="Absolute path of Excel file to process")
def aggregate_custom_fields(file):
    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=[
            "priority_area",
            "program",
            "sub_program",
            "dataset",
            "start_date",
            "end_date",
            "field_name",
            "field_type",
            "aggregate_type",
            "aggregate_value",
        ],
    )

    writer.writeheader()

    for aggregate_record in utils.extract_custom_fields(file):
        writer.writerow(aggregate_record)


@click.command()
@click.option("--file", help="Absolute path of Excel file to process")
def extract_demographics(file):
    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=[
            "priority_area",
            "program",
            "sub_program",
            "dataset",
            "data_description",
            "start_date",
            "end_date",
            "geography",
            "total_served",
        ],
        extrasaction="ignore",
    )

    writer.writeheader()

    for record in utils.extract_demographic_fields(file):
        writer.writerow(record)


@click.command()
@click.option("--file", help="Absolute path of Excel file to process")
def aggregate_demographics(file):
    schema = AggregatePersonSchema()

    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=[
            "priority_area",
            "program",
            "sub_program",
            "dataset",
            "data_description",
            "start_date",
            "end_date",
            *sorted(
                [
                    field
                    for field in schema.fields
                    if any(
                        field.startswith(f"{prefix}_")
                        for prefix in ("age", "gender", "re")
                    )
                    or field == "total_served"
                ]
            ),
        ],
    )

    writer.writeheader()

    for aggregate_record in utils.aggregate_demographic_fields(file):
        writer.writerow(aggregate_record)


@click.command()
@click.option("--file", help="Absolute path of Excel file to process")
def extract_program_sites(file):
    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=[
            "priority_area",
            "program",
            "sub_program",
            "dataset",
            "announcement_date",
            "opening_date",
            "project_name",
            "data_description",
            "lat",
            "lon",
        ],
        extrasaction="ignore",
    )

    writer.writeheader()

    with open(file, "r") as f:
        records = csv.DictReader(f)

        for record in records:
            writer.writerow(record)


@click.command()
@click.option("--file", help="Absolute path of Excel file to process")
def aggregate_program_sites(file):
    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=[
            "priority_area",
            "program",
            "sub_program",
            "dataset",
            "start_date",
            "end_date",
            "geography",
            "data_description",
            "n_applications_received",
            "n_projects_announced",
            "n_projects_completed",
        ],
    )

    writer.writeheader()

    for aggregate_record in utils.aggregate_place_fields(file):
        writer.writerow(aggregate_record)
