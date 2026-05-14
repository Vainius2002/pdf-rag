from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes.home import router as home_router
from app.routes.upload import router as upload_router
from app.routes.health import router as health_router
from app.routes.ask import router as ask_router
from app.routes.register import router as register_router
from app.routes.login import router as login_router

app = FastAPI()
# Static has to be included. HTML templates too but in routes using Jinja2templates library
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(home_router)
app.include_router(upload_router)
app.include_router(health_router)
app.include_router(ask_router)
app.include_router(register_router)
app.include_router(login_router)