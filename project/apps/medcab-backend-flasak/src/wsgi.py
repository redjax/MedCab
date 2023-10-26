from __future__ import annotations

from medcab_backend.constants import env_str
from medcab_backend.main import app

if __name__ == "__main__":
    print(f"{env_str} Starting WSGI app")
    app.run()
