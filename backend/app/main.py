from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.database import tortoise_close, tortoise_init
from app.router import api_router
from app.config import config


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    await tortoise_init(config.DATABASE_URL, generate_schemas=True)
    yield
    await tortoise_close()


app = FastAPI(
    title=config.PROJECT_TITLE,
    openapi_url=f"/{config.API_PREFIX}/{config.API_VERSION}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)

app.include_router(api_router, prefix=f"/{config.API_PREFIX}/{config.API_VERSION}")
