# MedCab

An app I'm working on to keep track of the medicine I'm taking.

## Requirements

- Docker/Compose
- Python [`pdm`](pdm.fming.dev/) dependency manager
  - (Optional) [`poetry`](python-poetry.org/).
    - If using `poetry` instead of `pdm`, you will need to convert the `pyproject.toml` file to `poetry`'s format

## Usage

### Run local with Docker environment

- `cd` to `project/`
- Copy `.env.example` -> `.env`
  - Set `MEDCAB_API_DOCKERFILE` to "Dockerfile.dev"
  - Set `MEDCAB_API_LOG_LEVEL` to "DEBUG"
  - Set `MEDCAB_API_APP_ENV` to "dev"
  - **REQUIRED**: Set a value for `NGINX_BACKEND_SERVER`
    - Default is `127.0.0.1` and is only accessible from the local machine
    - To use on a LAN:
      - With a DNS hostname:
        - Set backend FQDN (i.e. `medcab.devbox.local`)
      - With an IP address:
        - Set backend IP (i.e. `192.168.1.xxx`)
- Run `docker compose build`
- If the build succeeds, run `docker compose up -d`
  - Check container status with:
    - API: `docker compose logs -f api`
    - Proxy: `docker compose logs -f proxy`

#### Reload NGINX proxy config without restarting container

When using the `proxy` container, if you make any changes to the configuration while the container is live, you can trigger a config reload without restarting the container by running `project/reload_nginx.sh`, or with the command:

```
docker compose exec proxy nginx -s reload
```

## Notes

## Links
