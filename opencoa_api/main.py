from fastapi import FastAPI
from opencoa_api.config import Config
from opencoa_api.routes import coa
from opencoa_api.routes.vendors import cisco
import uvicorn

config = Config(RADIUS_DICTIONARY_PATH="./attributes")
app = FastAPI()

# Include vendor specific API endpoints
app.include_router(coa.router)
app.include_router(cisco.router)
