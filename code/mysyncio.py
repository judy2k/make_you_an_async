#!/usr/bin/env python3

import collections
import time


_PENDING = 'PENDING'
_FINISHED = 'FINISHED'


def coroutine(func):
    return func


@coroutine
def sleep(seconds):
    then = time.time() + seconds
    while time.time() < then:
        yield


class Future:
    def __init__(self, loop):
        self._loop = loop
        self._state = _PENDING
        # self._callbacks = []

    def done(self):
        return self._state != _PENDING

    def set_result(self, result):
        self.result = result
        self._state = _FINISHED
        # self._schedule_callbacks()

    # def add_done_callback(self, fn):
    #     self._callbacks.append(fn)

    # def _schedule_callbacks(self):
    #     for callback in self._callbacks:
    #         self._loop.call_soon(lambda: callback(self))

    def __iter__(self):
        while not self.done():
            yield
        return self.result


class Task(Future):
    """A coroutine wrapped in a Future."""

    def __init__(self, coro, *, loop=None):
        super().__init__(loop=loop)
        self._coro = coro
        self._loop.call_soon(self._step)

    def _step(self):
        coro = self._coro
        
        try:
            result = next(coro)
        except StopIteration as exc:
            self.set_result(exc.value)
        else:
            self._loop.call_soon(self._step)


class MyEventLoop:
    def __init__(self):
        self._ready = collections.deque()
        self._stopping = False

    def stop(self):
        self._stopping = True

    def create_future(self):
        return Future(self)

    def create_task(self, coro):
        return Task(coro, loop=self)

    def call_soon(self, callback):
        self._ready.append(callback)

    def run_forever(self):
        while True:
            self._run_once()
            if self._stopping:
                break

    def _run_once(self):
        while self._ready:
            callback = self._ready.popleft()
            callback()
            time.sleep(0.1)


def hello_world_and_stop(loop):
    print("Hello, World!")
    loop.call_soon(lambda: loop.stop())


default_loop = MyEventLoop()

def get_event_loop():
    return default_loop
