import click

from chicagorecoverypy.processors.core import flatten_workbooks
from chicagorecoverypy.processors.reporting import (
    aggregate_custom_fields,
    aggregate_demographics,
    aggregate_program_sites,
    extract_demographics,
    extract_program_sites,
)


@click.group
def cli():
    pass


cli.add_command(flatten_workbooks)
cli.add_command(aggregate_custom_fields)
cli.add_command(extract_demographics)
cli.add_command(aggregate_demographics)
cli.add_command(extract_program_sites)
cli.add_command(aggregate_program_sites)

if __name__ == "__main__":
    cli()
