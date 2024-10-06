import random


class Ship:
    def __init__(self, size):
        self.row = random.randrange(0, 9)
        self.column = random.randrange(0, 9)
        self.size = size
        self.orientation = random.choice(['horizontal', 'vertical'])
        self.indexes = self.compute_indexes()

    def compute_indexes(self):
        start_index = self.row*10 + self.column
        if self.orientation == 'horizontal':
            list_of_indexes = [start_index + index for index in range(self.size)]
            return list_of_indexes
        elif self.orientation == 'vertical':
            list_of_indexes = [start_index + index*10 for index in range(self.size)]
            return list_of_indexes
