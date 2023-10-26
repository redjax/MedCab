from __future__ import annotations

from medcab_backend.domain.product.validators import valid_families, valid_forms
from medcab_backend.domain.ui.menu import DropdownMenuOptions

def family_dropdown_options() -> DropdownMenuOptions:
    """Return valid families list for populating frontend dropdown menus."""
    options: DropdownMenuOptions = DropdownMenuOptions(options=valid_families)

    return options


def form_dropdown_options() -> DropdownMenuOptions:
    """Return valid forms list for populating frontend dropdown menus."""
    options: DropdownMenuOptions = DropdownMenuOptions(options=valid_forms)

    return options
