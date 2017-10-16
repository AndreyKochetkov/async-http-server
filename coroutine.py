class Future:
    def __init__(self):
        self.result = None
        self._callbacks = []

    def append_done_callback(self, func):
        self._callbacks.append(func)

    def set_result(self, result):
        self.result = result
        for func in self._callbacks:
            func(result)


class Task:
    def __init__(self, coroutine, fileno):
        self.coroutine = coroutine
        self.coroutine.send(None)
        self.fileno = fileno
        fut = Future()
        fut.set_result(fileno)
        self.step(fut)

    def step(self, fut):
        try:
            next_fut = self.coroutine.send(fut.result)
        except (StopIteration, ValueError):
            return
        next_fut.append_done_callback(self.step)
