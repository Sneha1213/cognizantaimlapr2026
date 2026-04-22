import asyncio
import time 
async def create_clock():
    while True :
        print(time.strftime("%H:%M:%S", time.localtime()))
        await asyncio.sleep(1)
if __name__ == "__main__":
    asyncio.run(create_clock())