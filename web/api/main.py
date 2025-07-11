from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socket

from .version import APP_NAME, APP_VERSION

app = FastAPI(title=f"{APP_NAME} Backend API")

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

from routes import (
    accounts, auth, modules, vm, nodes, storage, shares, mail, alerts, themes,
    diagnostics, tasks, plugins, settings, iso
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
def root_api():
    return {
        "status": "running",
        "host": hostname,
        "ip": local_ip,
        "name": APP_NAME,
        "version": APP_VERSION
    }
app.include_router(accounts.router, prefix="/api/accounts")
app.include_router(auth.router, prefix="/api/auth")
app.include_router(modules.router, prefix="/api/modules")
app.include_router(vm.router, prefix="/api/vm")
app.include_router(nodes.router, prefix="/api/nodes")
app.include_router(storage.router, prefix="/api/storage")
app.include_router(shares.router, prefix="/api/shares")
app.include_router(mail.router, prefix="/api/mail")
app.include_router(alerts.router, prefix="/api/alerts")
app.include_router(themes.router, prefix="/api/themes")
app.include_router(diagnostics.router, prefix="/api/diagnostics")
app.include_router(tasks.router, prefix="/api/tasks")
app.include_router(plugins.router, prefix="/api/plugins")
app.include_router(settings.router, prefix="/api/settings")
app.include_router(iso.router, prefix="/api/iso")