from red_utils.ext.sqlalchemy_utils import saSQLiteConnection, get_engine

from medcab_backend.utils.ui_utils.menus import (
    family_dropdown_options,
    form_dropdown_options,
)
from medcab_backend.domain.ui import DropdownMenuOptions

db_conn: saSQLiteConnection = saSQLiteConnection(database=".db/medcab.db")

engine = get_engine(connection=db_conn)

## Initialize entries for dropdown menus
dropdown_family: DropdownMenuOptions = family_dropdown_options()
dropdown_form: DropdownMenuOptions = form_dropdown_options()
