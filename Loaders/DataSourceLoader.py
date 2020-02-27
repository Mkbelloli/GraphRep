
class DataSourceLoader:
    def __init__(self):
        self.current = 0

    def initialize(self):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        self.current += 1
        if self.current < 100:
            return self.current
        raise StopIteration