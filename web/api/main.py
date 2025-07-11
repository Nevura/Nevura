from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import system, auth, modules, vm, users, mail, alerts, themes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(system.router, prefix="/api/system")
app.include_router(auth.router, prefix="/api/auth")
app.include_router(modules.router, prefix="/api/modules")
app.include_router(vm.router, prefix="/api/vm")
app.include_router(users.router, prefix="/api/users")
app.include_router(mail.router, prefix="/api/mail")
app.include_router(alerts.router, prefix="/api/alerts")
app.include_router(themes.router, prefix="/api/themes")