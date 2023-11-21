import typing

from loop_listings import set_loop_amount


class DataSource:
    def __init__(self, f: typing.Callable):
        self.load_data = f
        self.a = 1
        self.valid_data = []
        self.page = 0

    def has_more(self) -> bool:
        # set_loop_amount
        return True

    def next(self):
        if self.has_more():
            data = self.load_data()
            # check valid/invalid
            self.valid_data.append(data)
            self.page += 1
        else:
            pass


d = DataSource(lambda x: x)
