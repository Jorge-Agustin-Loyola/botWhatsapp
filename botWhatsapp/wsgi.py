from ..app import app
import asyncio

application = app

if __name__== "__main__":
    asyncio.run(application.run())