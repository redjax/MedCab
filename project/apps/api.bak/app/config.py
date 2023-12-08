from dynaconf import Dynaconf

settings_root: str = "config"

settings = Dynaconf(
    root_path=settings_root,
    environment=False,
    # envvar_prefix="DYNACONF_",
    settings_files=["settings.toml", "settings.local.toml", ".secrets.toml"],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
