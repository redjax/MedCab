from __future__ import annotations

import json
from pathlib import Path

from core.dependencies import APP_SETTINGS

example_schemas_dir: Path = Path(f"{APP_SETTINGS.data_dir}/example_schemas")
example_product_schemas_dir: Path = Path(f"{example_schemas_dir}/products")
example_product_simplified_schemas_dir: Path = Path(
    f"{example_product_schemas_dir}/simplified_for_testing"
)


def load_example_products():
    raise NotImplementedError("Loading example products not supported")


def load_example_products_simplified(
    schema_dir: Path = example_product_simplified_schemas_dir,
):
    assert schema_dir is not None, ValueError("schema_dir cannot be None")
    if not isinstance(schema_dir, Path):
        if isinstance(schema_dir, str):
            schema_dir: Path = Path(schema_dir)
        else:
            raise TypeError(
                f"Invalid type for schema_dir: ({type(schema_dir)}). Must be of type Path"
            )
    assert schema_dir.exists(), FileNotFoundError(
        f"Could not find schema dir: {schema_dir}"
    )

    products: list[dict] = []
    for p in schema_dir.glob("**/*.json"):
        if p.is_file():
            with open(p, "r") as f:
                contents = f.read()
                data = json.loads(contents)
                products.append(data)

    return products
