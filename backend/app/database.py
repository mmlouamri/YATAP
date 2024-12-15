from tortoise import Tortoise

from app.config import config

TORTOISE_ORM = {
    "connections": {
        "default": config.DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": [
                "app.core.auth.models",
                "app.core.users.models",
                "app.features.todos.models",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}

print(TORTOISE_ORM.get("apps").get("models").get("models"))

async def tortoise_init():
    await Tortoise.init(
        db_url=TORTOISE_ORM.get("connections").get("default"),
        modules={"models": TORTOISE_ORM.get("apps").get("models").get("models")},
    )


async def tortoise_close():
    await Tortoise.close_connections()
