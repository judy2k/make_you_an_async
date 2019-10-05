import aiohttp
import asyncio
import random 

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.head(url) as response:
            print(f"Fetching: {url}")
            resp = await response.text()
            await asyncio.sleep(random.random())
            print(f"Received: {url}")

@asyncio.coroutine
def main():
    yield from asyncio.gather(*[fetch(url) for url in [
        'http://python.org',
        'http://www.yahoo.com',
        'http://www.google.com',
        'http://www.nexmo.com',
    ]])
            

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())