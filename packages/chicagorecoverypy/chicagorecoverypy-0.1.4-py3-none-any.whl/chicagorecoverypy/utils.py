import csv
from itertools import groupby
import logging
import os
from statistics import mean
import sys

import pandas as pd
import geopandas

import chicagorecoverypy.schemas as crp_schemas


logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def get_schema_from_data_type(data_type):
    return {
        "record-level place-based investment data": crp_schemas.RecordLevelPlaceSchema,
        "aggregated place-based investment data": crp_schemas.AggregatePlaceSchema,
        "aggregated people-based investment data": crp_schemas.AggregatePersonSchema,
    }[data_type]


def parse_workbook_filename(file):
    file_parts = file.split("/")

    return {
        "priority_area": file_parts[3],
        "program": file_parts[4],
        "sub_program": "".join(file_parts[5:-1]),
        "dataset": file_parts[-1],
    }


def parse_flat_filename(file):
    file_parts = file.split("/")

    return {
        "data_type": file_parts[-2],
        "dataset": file_parts[-1],
    }


def get_date_range(record):
    # TODO: The date range for record-level place is kind of fucked up, TBQH
    if {"announcement_date", "opening_date"} < record.keys():
        return (
            record.get("announcement_date", "No announcement date")
            or "No announcement date",
            record.get("opening_date", "No opening date") or "No opening date",
        )
    return (
        record.get("start_date", "No start date") or "No start date",
        record.get("end_date", "No end date") or "No end date",
    )


def float_or_zero(string):
    try:
        return float(string)
    except ValueError:
        return 0


def extract_custom_fields(file):
    schema_cls = get_schema_from_data_type(parse_flat_filename(file)["data_type"])
    schema = schema_cls()

    with open(file, "r") as f:
        data = list(csv.DictReader(f))

        try:
            expected_fields = [
                "priority_area",
                "program",
                "sub_program",
                "dataset",
                "department",
                "data_description",
                "data_type",
            ] + list(schema.fields.keys())

            custom_fields = [k for k in data[0] if k not in expected_fields]

            metadata = {
                "priority_area": data[0]["priority_area"],
                "program": data[0]["program"],
                "sub_program": data[0]["sub_program"],
                "dataset": data[0]["dataset"],
            }
        except IndexError:
            logger.info(f"🙀 {file} contains no records. Skipping...")
            sys.exit(0)

        custom_data = [
            {k: v for k, v in record.items() if (k in custom_fields) or ("date" in k)}
            for record in data
            if any(record.values())
        ]

        for field in custom_fields:
            if field in ("start_date", "end_date", "announcement_date", "opening_date"):
                continue

            segmented_values = groupby(
                sorted(custom_data, key=lambda x: get_date_range(x)),
                lambda x: get_date_range(x),
            )

            for (start_date, end_date), value_list in segmented_values:
                non_zero_values = list(
                    filter(
                        lambda x: x not in (None, ""),
                        map(lambda x: x[field], value_list),
                    )
                )

                if any(non_zero_values):
                    try:
                        numeric_values = [float(value) for value in non_zero_values]
                    except ValueError:
                        yield {
                            "start_date": start_date if start_date else None,
                            "end_date": end_date if end_date else None,
                            "field_name": field,
                            "field_type": type(non_zero_values[0]).__name__,
                            "aggregate_type": None,
                            "aggregate_value": None,
                            **metadata,
                        }
                    else:
                        if r"% of" in field:
                            yield {
                                "start_date": start_date if start_date else None,
                                "end_date": end_date if end_date else None,
                                "field_name": field,
                                "field_type": "percentage",
                                "aggregate_type": "mean",
                                "aggregate_value": mean(numeric_values),
                                **metadata,
                            }
                        else:
                            yield {
                                "start_date": start_date if start_date else None,
                                "end_date": end_date if end_date else None,
                                "field_name": field,
                                "field_type": "number",
                                "aggregate_type": "sum",
                                "aggregate_value": sum(numeric_values),
                                **metadata,
                            }


def extract_demographic_fields(file):
    with open(file, "r") as f:
        data = list(csv.DictReader(f))

        try:
            demographic_fields = [
                k
                for k in data[0]
                if k in ("geography", "date", "total_served")
                or any(k.startswith(f"{prefix}_") for prefix in ("age", "gender", "re"))
            ]

            metadata = {
                "priority_area": data[0]["priority_area"],
                "program": data[0]["program"],
                "sub_program": data[0]["sub_program"],
                "dataset": data[0]["dataset"],
                "data_description": data[0]["data_description"],
            }

        except IndexError:
            logger.info(f"🙀 {file} contains no records. Skipping...")
            sys.exit(0)

        demographic_data = [
            {
                k: v
                for k, v in record.items()
                if (k in demographic_fields) or ("date" in k)
            }
            for record in data
            if any(record.values())
        ]

        # Data can be subdivided by service center. Aggregate up to geography.
        segmented_values = groupby(
            sorted(
                demographic_data,
                key=lambda x: (
                    x.get("geography") or "No geography",
                    get_date_range(x),
                ),
            ),
            lambda x: (
                x.get("geography") or "No geography",
                get_date_range(x),
            ),
        )

        for (geography, (start_date, end_date)), value_list in segmented_values:
            _value_list = list(value_list)
            geography_record = {
                k: sum({float_or_zero(record[k]) for record in _value_list})
                for k in demographic_fields
                if k not in ("geography", "date")
            }

            geography_record.update(
                {
                    "geography": geography,
                    "start_date": start_date if start_date else None,
                    "end_date": end_date if end_date else None,
                    **metadata,
                }
            )
            yield geography_record


def aggregate_demographic_fields(file):
    segmented_values = groupby(
        sorted(
            extract_demographic_fields(file),
            key=lambda x: get_date_range(x),
        ),
        lambda x: get_date_range(x),
    )

    for (start_date, end_date), value_list in segmented_values:
        # Convert to list so we can grab keys from the first record
        _value_list = list(value_list)

        date_metadata = {k: _value_list[0][k] for k in ("start_date", "end_date")}

        dataset_metadata = {
            "priority_area": _value_list[0]["priority_area"],
            "program": _value_list[0]["program"],
            "sub_program": _value_list[0]["sub_program"],
            "dataset": _value_list[0]["dataset"],
            "data_description": _value_list[0]["data_description"],
        }

        aggregate_data = {}

        aggregate_data = {
            k: sum(float_or_zero(record[k]) for record in _value_list)
            for k in _value_list[0]
            if k not in ("geography", "date", "date_range", "start_date", "end_date")
        }

        aggregate_data.update(**date_metadata)
        aggregate_data.update(**dataset_metadata)

        yield aggregate_data


def aggregate_place_fields(file):
    with open(file, "r") as f:
        place_data = csv.DictReader(f)
        df = pd.DataFrame(place_data)

    try:
        assert len(df.index) > 0
    except AssertionError:
        logger.info(f"🙀 {file} contains no records. Skipping...")
        sys.exit(0)

    (dataset_metadata,) = df[:1][
        [
            "priority_area",
            "program",
            "sub_program",
            "dataset",
            "data_description",
        ]
    ].to_dict(orient="records")

    if all(k in df.keys() for k in ("lat", "lon")):
        logger.info(f"Loading {file} points")
        records_with_points = df[(df.lat != "") & (df.lon != "")]

        sites = geopandas.GeoDataFrame(
            records_with_points,
            geometry=geopandas.points_from_xy(
                records_with_points.lon, records_with_points.lat
            ),
            crs="EPSG:4326",
        )

        community_areas = geopandas.read_file(
            os.path.join("data", "raw", "community_areas.geojson")
        )

        sites_with_community_area = geopandas.sjoin(
            sites, community_areas, how="inner", predicate="within"
        )

        grouped_sites = sites_with_community_area.groupby(
            ["community", "announcement_date", "opening_date"]
        ).count()["project_name"]

        # Not sure if this will work
        for (
            geography,
            start_date,
            end_date,
        ), n_projects in grouped_sites.to_dict().items():
            yield {
                "geography": geography,
                "start_date": start_date,
                "end_date": end_date,
                "n_projects_announced": n_projects,
                **dataset_metadata,
            }

    else:
        try:
            grouped_sites = df[
                [
                    "geography",
                    "start_date",
                    "end_date",
                    "number_of_projects_announced",
                    "number_of_applications_received",
                    "number_of_projects_completed",
                ]
            ]
        except KeyError:
            logger.warning(f"🙅‍♀️ {file} is malformed. Skipping...")
            sys.exit(0)

        for record in grouped_sites.to_dict(orient="records"):
            yield {
                "geography": record["geography"],
                "start_date": record["start_date"],
                "end_date": record["end_date"],
                "n_projects_announced": record["number_of_projects_announced"],
                "n_applications_received": record["number_of_applications_received"],
                "n_projects_completed": record["number_of_projects_completed"],
                **dataset_metadata,
            }
