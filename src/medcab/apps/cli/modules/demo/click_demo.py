from __future__ import annotations

from .methods import add_new_dispensary, add_new_product, add_new_purchase

import click
from domain.dispensary import Dispensary
from domain.product import Product
from domain.purchase import Purchase

from entrypoints.startup import entrypoint_app_startup

@click.group(name="demo", help="Demo functions using pre-built data.")
def demo_cli():
    pass


@demo_cli.command(help="Run the app startup entrypoint to set app up for execution.")
def app_startup():
    entrypoint_app_startup()


@demo_cli.command(help="Answer prompts to add a new demo Product")
def add_product():
    product: Product = add_new_product()
    click.echo(f"New Product: {product}")


@demo_cli.command(help="Answer prompts to add a new demo Dispensary")
def add_dispensary():
    dispensary: Dispensary = add_new_dispensary()
    click.echo(f"New dispensary: {dispensary}")

@demo_cli.command(help="Answer prompts to add a new demo Purchase")
def add_purchase():
    purchase: Purchase = add_new_purchase()
    click.echo(f"New Purchase: {purchase}")