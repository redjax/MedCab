from __future__ import annotations

from decimal import Decimal

from wtforms import (
    BooleanField,
    DecimalField,
    Form,
    PasswordField,
    StringField,
    validators,
)

class NewProductform(Form):
    favorite: bool = BooleanField("favorite")
    strain: str | None = StringField("strain", [validators.DataRequired()])
    family: str | None = StringField("family", [validators.DataRequired()])
    form: str | None = StringField("form")
    total_cbd: Decimal | None = DecimalField("total_cbd")
    total_thc: Decimal | None = DecimalField("total_thc")
