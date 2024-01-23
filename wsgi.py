import asyncio
from app import app
import modelo

if __name__== "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(app.run())