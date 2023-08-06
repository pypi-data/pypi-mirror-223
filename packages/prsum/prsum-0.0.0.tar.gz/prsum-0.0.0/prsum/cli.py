import click


@click.command()
@click.argument("names", nargs=-1)
def main(names):
    click.echo(repr(names))


if __name__ == "__main__":
    main()
