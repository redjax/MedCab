from wtforms import (
    Form,
    BooleanField,
    StringField,
    PasswordField,
    DecimalField,
    validators,
)

from decimal import Decimal


class NewProductform(Form):
    strain: str | None = StringField("strain", [validators.DataRequired()])
    family: str | None = StringField("family", [validators.DataRequired()])
    form: str | None = StringField("form")
    total_cbd: Decimal | None = DecimalField("total_cbd")
    total_thc: Decimal | None = DecimalField("total_thc")
