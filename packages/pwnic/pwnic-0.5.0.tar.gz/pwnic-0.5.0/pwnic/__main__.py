import uvicorn

from pwnic.api import app
from pwnic.utils import ensure_certs, get_ip_addresses

keyfile, certfile = ensure_certs()
uvicorn.run(
    app,
    host=get_ip_addresses()[0],
    port=7777,
    ssl_keyfile=keyfile,
    ssl_certfile=certfile,
    log_level="trace",
)
