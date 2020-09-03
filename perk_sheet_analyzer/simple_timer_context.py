import time


class SimpleTimerContext:
    def __init__(self, message: str):
        self.message = message

    def __enter__(self):
        print(self.message)
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.end = time.perf_counter()
        self.interval = self.end - self.start
        print("Elapsed: %s" % (self.end - self.start))
