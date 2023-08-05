import click


@click.group()
def cli():
    pass


@cli.command()
def commit():
    click.echo('commit')
