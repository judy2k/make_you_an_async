import mysyncio

@mysyncio.coroutine
def set_after(delay, fut, value):
    yield from mysyncio.sleep(delay)
    fut.set_result(value)

@mysyncio.coroutine
def main():
    fut = loop.create_future()
    task = loop.create_task(set_after(1, fut, '... world'))

    print('hello ...')
    print((yield from fut))

loop = mysyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()