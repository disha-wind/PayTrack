import asyncio

from database.model import User, Admin, Account
from database.unit import Database

async def main():
    db = Database()
    await db.init()
    user_1 = User(
        id=1,
        email='admin@gmail.com',
        password_hash='$2b$12$MjRsxhcKKmGXiTBsITez8uExAHT.Ooeaeo2m0HbuAEFQC/Mt1HaP2',
        full_name="Admin Test"
    )

    user_2 = User(
        id=2,
        email='user@gmail.com',
        password_hash='$2b$12$sl8ACbQQ/ZGLHip3F9LMMeNhAT8ehbiqeZ5mUl0QJUQtioleawQEC',
        full_name="User Test"
    )

    admin = Admin(
        user_id=user_1.id
    )

    account = Account(
        id=1,
        user_id=user_2.id
    )
    try:
        await db.add(user_1)
        await db.add(user_2)
        await db.add(admin)
        await db.add(account)
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(main())