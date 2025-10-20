import asyncio
import os

from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv

from app.db import engine
from app import models, schemas, crud, deps

load_dotenv()

async def init_data():
    admin_login, admin_password = os.getenv("TEST_ADMIN_LOGIN"), os.getenv("TEST_ADMIN_PASSWORD")
    worker_login, worker_password = os.getenv("TEST_WORKER_LOGIN"), os.getenv("TEST_WORKER_PASSWORD")
    async with AsyncSession(engine) as session:
        # Check if admin exists
        existing_admin = await crud.get_user_by_username(session, admin_login)
        if not existing_admin:
            hashed = deps.get_password_hash(admin_password)
            await crud.create_user(session, schemas.UserCreate(
                username=admin_login,
                password=admin_password,
                full_name=f"{admin_login} user"
            ), models.Role.admin, hashed)

        # Check if worker exists
        existing_worker = await crud.get_user_by_username(session, worker_login)
        if not existing_worker:
            hashed = deps.get_password_hash(worker_password)
            await crud.create_user(session, schemas.UserCreate(
                username=worker_login,
                password=worker_password,
                full_name=f"{worker_login} user"
            ), models.Role.worker, hashed)

    print("✅ Default users created (if missing)")


if __name__ == "__main__":
    asyncio.run(init_data())
