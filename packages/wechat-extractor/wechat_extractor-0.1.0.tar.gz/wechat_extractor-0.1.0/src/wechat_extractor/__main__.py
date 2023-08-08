import click

from wechat_extractor import __version__
from wechat_extractor.commands import command_group


def print_version(ctx: click.Context, _, value: str):
    if not value or ctx.resilient_parsing:
        return

    click.echo(__version__)
    ctx.exit()


@click.group(commands=command_group)
@click.option('--version', help='Show version information.', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
def cli():
    """A command-line tool that can extract data from WeChat backup files."""


if __name__ == '__main__':
    cli()
