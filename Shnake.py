"""
Object of importance requiring abstraction:

Score

Play area - grid, stores positions and informs of interractions

nake_segment - playable, stores the array of positions

Food - Moves in the grid. Needs to know current populated positions. Needs to be consumed


"""

class snake:
    def __init__(self, length, head_direction, tail_direction, frame_advance):
        self.length = length
        self.head_direction = head_direction
        self.tail_direction = tail_direction
        self.frame_advance = frame_advance
        for _ in range(length):


    

class grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[H for _ in range(height)] for _ in range(width)]

    def advance_frame(self):
        
