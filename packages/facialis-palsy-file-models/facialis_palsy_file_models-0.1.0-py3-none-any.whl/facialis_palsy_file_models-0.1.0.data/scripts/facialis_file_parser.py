import json

import click
import logging

from facialis_palsy_file_models.jauto_eface_file_type import EfaceSunnybrookFile

_logger = logging.getLogger("facialis_file_parser")


@click.command()
@click.argument("filename", type=click.Path(exists=True),
              nargs=1, required=True,)
def parse_file(filename):
    """Parse a given file

    FILENAME: The file to parse

    It trys to parse the file and prints the result to stdout.
    If the file is not parsable, it prints an error message to stderr.

    :param filename:
    :return:
    """
    try:
        with open(filename, "r") as file:
            input_file = file.read()
            jauto_eface_file = EfaceSunnybrookFile.parse_raw(input_file)

            _logger.info(f"File {filename} successfully parsed")
    except Exception as e:
        _logger.error(f"Error while parsing file {filename}: \n"
                      f"{e}")
    pass


@click.command()
@click.argument("filename", type=click.Path(exists=True),
              nargs=1, required=True,)
def eface_v1(filename):
    """
    Migrate eface v1 to this eface format.
    :param filename:
    :return:
    """
    _logger.error("Not implemented yet")
    pass


@click.command()
@click.argument("grading_system", type=click.Choice(["sunnybrook", "housebrackmann", "eface", "jauto_eface"]),
                nargs=1, required=True,)
def json_schema(grading_system):
    """
    Create a json shema from the given grading system.
    :param grading_system:
    :return:
    """
    if grading_system == "sunnybrook":
        from facialis_palsy_file_models.sunnybrook_type import Sunnybrook
        print(json.dumps(Sunnybrook.model_json_schema(), indent=2))
    elif grading_system == "housebrackmann":
        from facialis_palsy_file_models.housebrackmann_type import HouseBrackmann
        print(json.dumps(HouseBrackmann.model_json_schema(), indent=2))
    elif grading_system == "eface":
        from facialis_palsy_file_models.eface_type import Eface
        print(json.dumps(Eface.model_json_schema(), indent=2))
    elif grading_system == "jauto_eface":
        from facialis_palsy_file_models.jauto_eface_file_type import EfaceSunnybrookFile
        print(json.dumps(EfaceSunnybrookFile.model_json_schema(), indent=2))
    else:
        _logger.error(f"Grading system {grading_system} not implemented yet")


@click.group()
def cli():
    """Facialis File Parser

    as an example program for implementing the Facial Palsy File Models
    """
    pass


@click.group()
def migrate():
    """Migrate a file to a new format"""
    pass


# Migrate Group Command
migrate.add_command(eface_v1)

# Main Group Command
cli.add_command(parse_file)
cli.add_command(migrate)
cli.add_command(json_schema)


if __name__ == "__main__":
    cli()
