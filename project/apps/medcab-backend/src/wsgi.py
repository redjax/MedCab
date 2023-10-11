from medcab_backend.main import app
from medcab_backend.constants import env_str

if __name__ == "__main__":
    print(f"{env_str} Starting WSGI app")
    app.run()