import csv
from datetime import datetime
import json
import logging
import os

import click
from marshmallow.exceptions import ValidationError
import pylightxl as xl

import chicagorecoverypy.utils as utils
from chicagorecoverypy.workbook import ActivityWorkbook


logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


@click.command()
@click.argument("workbooks", nargs=-1)
@click.argument("destination", nargs=1)
@click.option(
    "--recreate",
    is_flag=True,
    default=False,
    help="Overwrite existing flattened workbooks",
)
def flatten_workbooks(workbooks, destination, recreate):
    try:
        error_f = open(f"data_errors_{datetime.now().isoformat()}.csv", "w+")

        error_writer = csv.DictWriter(
            error_f,
            fieldnames=[
                "priority_area",
                "program",
                "sub_program",
                "dataset",
                "record",
                "error",
            ],
        )

        error_writer.writeheader()

        summary_f = open(f"import_summary_{datetime.now().isoformat()}.csv", "w+")

        summary_writer = csv.DictWriter(
            summary_f,
            fieldnames=[
                "priority_area",
                "program",
                "sub_program",
                "dataset",
                "imported without errors",
                "records without errors",
                "records with errors",
            ],
        )

        summary_writer.writeheader()

        for workbook in workbooks:
            wb = ActivityWorkbook(xl.readxl(workbook))

            program_metadata = utils.parse_workbook_filename(workbook)

            try:
                next(wb.records)
            except (UserWarning, AttributeError) as e:
                logger.warning(
                    f"🙅‍♀️ Could not load {workbook} due to the following error. Skipping..."
                )
                logger.warning(str(e))
                error_writer.writerow(
                    {
                        **program_metadata,
                        "record": None,
                        "error": str(e),
                    }
                )
                summary_writer.writerow(
                    {
                        **program_metadata,
                        "imported without errors": False,
                        "records without errors": None,
                        "records with errors": None,
                    }
                )
                continue

            try:
                data_format = wb.cover_sheet["data type"].lower()
            except UserWarning as e:
                logger.warning(
                    f"🙅‍♀️ Could not load {workbook} due to the following error. Skipping..."
                )
                logger.warning(str(e))
                error_writer.writerow(
                    {
                        **program_metadata,
                        "record": None,
                        "error": str(e),
                    }
                )
                summary_writer.writerow(
                    {
                        **program_metadata,
                        "imported without errors": False,
                        "records without errors": None,
                        "records with errors": None,
                    }
                )
                continue

            try:
                schema_cls = utils.get_schema_from_data_type(data_format)
            except KeyError as e:
                logger.warning(
                    f"🙅‍♀️ Schema not available for {workbook} as {data_format}. Skipping..."
                )
                error_writer.writerow(
                    {
                        **program_metadata,
                        "record": None,
                        "error": str(e),
                    }
                )
                summary_writer.writerow(
                    {
                        **program_metadata,
                        "imported without errors": False,
                        "records without errors": None,
                        "records with errors": None,
                    }
                )
                continue

            schema = schema_cls()

            output_directory = os.path.join(destination, data_format)

            if not os.path.exists(output_directory):
                os.mkdir(output_directory)

            output_file = os.path.join(output_directory, program_metadata["dataset"])

            if os.path.exists(output_file) and not recreate:
                continue

            with open(output_file, "w+") as f:
                record_writer = None
                record_count = 0
                error_count = 0

                for record in wb.records:
                    if not any(record.values()):
                        continue

                    try:
                        normalized_record = schema.loads(json.dumps(record))

                    except ValidationError as e:
                        error_writer.writerow(
                            {
                                **program_metadata,
                                "record": json.dumps(record),
                                "error": str(e),
                            }
                        )
                        error_count += 1

                    else:
                        # Instantiate record writer when we find a valid record so
                        # we can use the normalized keys, rather than the raw ones.
                        if not record_writer:
                            record_writer = csv.DictWriter(
                                f,
                                fieldnames=[
                                    "priority_area",
                                    "program",
                                    "sub_program",
                                    "dataset",
                                    "department",
                                    "data_description",
                                    "data_type",
                                    *normalized_record.keys(),
                                ],
                            )

                            record_writer.writeheader()

                        normalized_record.update(
                            {
                                **program_metadata,
                                "department": wb.cover_sheet["department"],
                                "data_description": wb.cover_sheet["data description"],
                                "data_type": wb.cover_sheet["data type"],
                            }
                        )

                        record_writer.writerow(normalized_record)

                        record_count += 1

                summary_writer.writerow(
                    {
                        **program_metadata,
                        "imported without errors": error_count < 1,
                        "records without errors": record_count,
                        "records with errors": error_count,
                    }
                )

    finally:
        error_f.close()
        summary_f.close()


if __name__ == "__main__":
    flatten_workbooks()
