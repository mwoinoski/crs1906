#!/usr/bin/python3.7
# asyncio_example1.py
# Example: py asyncio_example1.py

import asyncio
import time


class SampleSensorAsyncio:
    async def count(self):
        print("One ", end="")
        await asyncio.sleep(1)
        print("Two ", end="")

async def main():
    sensor = SampleSensorAsyncio()
    await asyncio.gather(sensor.count(), sensor.count(), sensor.count())

if __name__ == "__main__":
    s = time.perf_counter()

    asyncio.run(main())

    print()
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
