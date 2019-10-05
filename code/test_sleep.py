from asyncio import coroutine, sleep, run

@coroutine
def hello_world():
    print("Hello ...")
    yield from sleep(1) 
    print("... World")

run(hello_world())