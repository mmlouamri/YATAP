from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "passwordresetsdb" (
    "email" VARCHAR(255) NOT NULL  PRIMARY KEY,
    "token" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "userdb" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP,
    "name" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "email_verified_at" TIMESTAMP,
    "password_hash" VARCHAR(255) NOT NULL,
    "profile_photo_path" VARCHAR(2045),
    "last_login" TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "idx_userdb_email_e5e37e" ON "userdb" ("email");
CREATE TABLE IF NOT EXISTS "tododb" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP,
    "title" VARCHAR(255) NOT NULL,
    "description" TEXT NOT NULL,
    "is_done" INT NOT NULL  DEFAULT 0,
    "owner_id" CHAR(36) NOT NULL REFERENCES "userdb" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
