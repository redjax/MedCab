from __future__ import annotations

from pathlib import Path

from core.dependencies import APP_SETTINGS
from apps.cli.methods.add_objects.methods import add_new_dispensary, add_new_product, add_new_purchase

from domain.dispensary import Dispensary
from domain.product import Product
from domain.purchase import Purchase, PurchaseNote

from entrypoints.startup import entrypoint_app_startup

import click
from red_utils.std.hash_utils import get_hash_from_str


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
    
    
    if click.confirm("Save purchase to file?"):
        _json = (purchase.model_dump_json())
        click.echo(f"Purchase json ({type(_json)}): {_json}")
        
        purchasehash = get_hash_from_str(purchase.product.strain)
        output = Path(f"{APP_SETTINGS.data_dir}/demo/purchases/{purchasehash}")
        if not output.exists():
            output.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output, "w") as f:
                f.write(_json)
