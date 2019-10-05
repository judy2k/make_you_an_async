import mysyncio


@mysyncio.coroutine
def return_after(delay, value):
    yield from mysyncio.sleep(delay)
    return value


@mysyncio.coroutine
def main():
    task = loop.create_task(return_after(1, '... world'))

    print('hello ...')
    print((yield from task))
    task._loop.stop()


loop = mysyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()