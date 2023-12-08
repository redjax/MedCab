from core.enums import FamilyEnum, FormEnum

VALID_FORMS: list = [member.value for member in FormEnum]
VALID_FAMILIES: list = [member.value for member in FamilyEnum]


def validate_form(v: str = None) -> str:
    """Validate a product form.

    Params:
    -------
    v (str): The product form to validate

    Usage:
    ------
    When declaring a class or passing a product form value around the app, call this function
    to validate that the product form is a non-null string value that exists in VALID_FORMS.
    """
    if v is None:
        raise ValueError("Missing a product form to validate")
    if not isinstance(v, str):
        try:
            v = str(v)
        except Exception as exc:
            raise Exception(
                f"Unable to coerce product form value: {v} ({type(v)}) to type str. Details: {exc}"
            )
    if v.lower() not in VALID_FORMS:
        raise ValueError(f"Invalid product form: {v}. Must be one of: {VALID_FORMS}")

    return v.lower()


def validate_family(v: str = None) -> str:
    """Validate a product family.

    Params:
    -------
    v (str): The product family to validate

    Usage:
    ------
    When declaring a class or passing a product form value around the app, call this function
    to validate that the product family is a non-null string value that exists in VALID_FAMILIES.
    """
    if v is None:
        raise ValueError("Missing a product family to validate")
    if not isinstance(v, str):
        try:
            v = str(v)
        except Exception as exc:
            raise Exception(
                f"Unable to coerce product family value: {v} ({type(v)}) to type str. Details: {exc}"
            )
    if v.lower() not in VALID_FAMILIES:
        raise ValueError(
            f"Invalid product family: {v}. Must be one of: {VALID_FAMILIES}"
        )

    return v.lower()
