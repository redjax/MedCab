from pathlib import Path

from core.dependencies import APP_SETTINGS, ENSURE_DIRS

from loguru import logger as log

def ensure_dirs_exist(dirs: list[Path] = None):
    assert dirs is not None, ValueError("dirs cannot be None")
    assert isinstance(dirs, list), TypeError(f"dirs must be of type list, not ({type(dirs)})")
    
    for d in dirs:
        if not d.exists():
            try:
                d.mkdir(parents=True, exist_ok=True)
            except Exception as exc:
                msg = Exception(f"Unhandled exception creating dir '{d}'. Details: {exc}")
                log.error(msg)
                
                pass
            
def entrypoint_app_startup(ensure_dirs: list[Path] = ENSURE_DIRS):
    log.info(f"Entrypoint: app_startup")
    ensure_dirs_exist(dirs=ensure_dirs)