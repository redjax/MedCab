from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from typing import Union

from core.validators.product import VALID_FAMILIES, VALID_FORMS
from domain.dispensary import Dispensary
from domain.product import Product
from domain.purchase import Purchase

import click
import inquirer
import pendulum

def add_new_product() -> Product:
    list_select_questions = [
        inquirer.List("family", message="Product Family", choices=VALID_FAMILIES),
        inquirer.List("form", message="Product Form", choices=VALID_FORMS),
    ]
    strain = click.prompt("Product strain name", type=str)
    # family = click.prompt("Product Family", type=click.Choice(VALID_FAMILIES))
    # form = click.prompt("Product Form", type=click.Choice(VALID_FORMS))
    family_form_answers = inquirer.prompt(list_select_questions)
    family = family_form_answers["family"]
    form = family_form_answers["form"]
    total_thc = click.prompt("Total THC in Product", type=Decimal)
    total_cbd = click.prompt("Total CBD in Product", type=Decimal)
    weight = click.prompt("Product weight", type=Decimal)

    try:
        product: Product = Product(
            family=family,
            form=form,
            strain=strain,
            total_cbd=total_cbd,
            total_thc=total_thc,
            weight=weight,
        )
        click.echo(f"Success: Create new Product | {product}")

        if click.confirm("Add Product to favorites?"):
            product.favorite = True

        return product
    except Exception as exc:
        msg = Exception(f"Unhandled exception creating new Product. Details: {exc}")
        click.echo(msg)

        raise msg


def add_new_dispensary() -> Dispensary:
    name = click.prompt("Dispensary name")
    city = click.prompt("Dispensary City")
    state = click.prompt("Dispensary 2-letter State code, i.e. 'NY'", type=str)

    try:
        dispensary: Dispensary = Dispensary(name=name, city=city, state=state)
        click.echo(f"Success: Create new Dispensary | {dispensary}")

        if click.confirm("Add Dispensary to favorites?"):
            dispensary.favorite = True

        return dispensary

    except Exception as exc:
        msg = Exception(f"Unhandled exception creating new Dispensary. Details: {exc}")
        click.echo(msg)

        raise msg

def add_new_purchase() -> Purchase:
    # Purchase(date=..., dispensary=..., product=..., price=...)
    date = click.prompt(f"Purchase date (ex: {pendulum.now().date()})", type=str, default=f"{pendulum.now().date()}")
    
    try:
        date_convert: pendulum.Date = pendulum.from_format(date, "YYYY-MM-DD").date()
        date = date_convert
    except Exception as exc:
        msg = Exception(f"Unhandled exception converting input to date: {date}. Details: {exc}")
        click.echo(msg)
        
        raise msg
    
    dispensary = add_new_dispensary()
    product = add_new_product()
    
    price = click.prompt("Purchase price", type=Decimal)
    
    try:
        purchase: Purchase = Purchase(date=date, dispensary=dispensary, product=product, price=price)
        
        return purchase
    except Exception as exc:
        msg = Exception(f"Unhandled exception creating new Purchasea. Details: {exc}")
        click.echo(msg)

        raise msg    
