from tortoise import Tortoise


async def tortoise_init(db_url: str, generate_schemas: bool = False):
    await Tortoise.init(
        db_url=db_url,
        modules={"models": ["app.core.auth.models", "app.core.users.models"]},
    )

    if generate_schemas:
        await Tortoise.generate_schemas()


async def tortoise_close():
    await Tortoise.close_connections()
