from __future__ import annotations

import secrets

def create_secret() -> str:
    _secret = secrets.token_hex()

    return _secret


if __name__ == "__main__":
    secret = create_secret()
    print(
        f"""
    -----------------
    | !! WARNING !! |
    -----------------
    This is your Flask app's secret. Store it in the 'app_secret_key' environment
    variable, either by updating 'src/config/.secrets.toml', or by setting the env
    variable DYNACONF_APP_SECRET_KEY=<your secret>.
    {'-' * 78}
    
    ------------------
    | APP SECRET KEY |
    ------------------
    {secret}
    """
    )
