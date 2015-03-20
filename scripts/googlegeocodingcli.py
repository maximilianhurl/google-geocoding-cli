import click
from scripts.manager import GeocodingManager


def validate_options(keys, file):
    if not keys:
        click.echo("Missing keys. Add with --keys ")
        return False

    if not file:
        click.echo("Missing input file. Add with --file ")
        return False

    return True


@click.command()
@click.option('--keys', help='Comma seperated list of keys XXX,XXX')
@click.option('--file', help='File with path to geocode', type=click.Path(exists=True))
def geocode(keys, file):
    if validate_options(keys, file):
        geocoding_manager = GeocodingManager(keys=keys, input_file_path=file)
        geocoding_manager.search()
        click.echo("Gecoding complete!")


@click.command()
@click.option('--keys', help='Comma seperated list of keys XXX,XXX')
@click.option('--file', help='File with path to geocode', type=click.Path(exists=True))
def reverse_geocode(keys, file):
    if validate_options(keys, file):
        geocoding_manager = GeocodingManager(
            keys=keys, input_file_path=file, query_type=GeocodingManager.REVERSE_GEOCODE_TYPE
        )
        geocoding_manager.search()
        click.echo("Reverse Gecoding complete!")
