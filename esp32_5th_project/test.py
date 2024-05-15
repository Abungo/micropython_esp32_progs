import uasyncio
import dh
async def my_async_function():
    dh.run()
    print("Async function called")

async def main():
    while True:
        await my_async_function()
        await uasyncio.sleep(10)

# Start the event loop
uasyncio.run(main())