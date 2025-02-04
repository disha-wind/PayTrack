import asyncio

import database

async def main():
    await database.init_db()

if __name__ == "__main__":
    asyncio.run(main())