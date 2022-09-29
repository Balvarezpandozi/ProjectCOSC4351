class Table:
    totalNum = 0
    def __init__(self, capacity):
        self.capacity = capacity
        Table.totalNum += 1