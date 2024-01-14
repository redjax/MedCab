from __future__ import annotations

from .modules.demo import demo_cli

import click

@click.group()
def cli():
    pass


cli.add_command(demo_cli)
