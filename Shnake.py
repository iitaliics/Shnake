import random
import pygame

"""
Object of importance requiring abstraction:

Score

Play area - grid, stores positions and informs of interractions

nake_segment - playable, stores the array of positions

Food - Moves in the grid. Needs to know current populated positions. Needs to be consumed


"""

# dict could be enum in c++
grid_object = {
    "NONE" : 0,
    "FOOD" : 1,
    "SNAKE" : 2,
}

# struct space_data
# grid_object, int
    

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[(grid_object['NONE'], -1) for _ in range(height)] for _ in range(width)]
        self.running = False

        x1, x2 = random.choices(range(self.width), k=2)
        y1, y2 = random.choices(range(self.height), k=2)

        self.snake_head = (x1, y1)
        self.grid[x1][y1] = (grid_object['SNAKE'], 10)

        # self.snake_head = (50, 100)
        # self.grid[50][100] = (grid_object['SNAKE'], 5)

        self.grid[x2][y2] = (grid_object['FOOD'], -1)
        
    def in_bounds(self, x, y):
        if x < 0 or x >= self.width:
            return False

        if y < 0 or y >= self.height:
            return False

        return True
        
    def game_over(self):
        self.running = False

    def start(self):
        direction = self.get_player_direction()
        self.render()
        pygame.display.update()
        
        
        while(direction == (0, 0)):
            temp = self.get_player_direction()
            if temp == (0, 0):
                pass
            elif self.in_bounds(self.snake_head[0] + temp[0], self.snake_head[1] + temp[1]):
                direction = temp
        grid.running = True
        self.update_snake(direction[0], direction[1]) 
        


    def respawn_food(self):
        free = []
        for column in range(self.width):
            for row in range(self.height):
                if not self.grid[column][row][1] > 0:
                    free.append((column, row))
        if len(free):
            chosenOne = random.choice(free)
            self.grid[chosenOne[0]][chosenOne[1]] = (grid_object['FOOD'], -1)


    def grow(self, x, y, current_length):
        self.grid[x][y] = (grid_object['SNAKE'], current_length + 3)
        

    def check_collision(self, x_direction, y_direction):
        x = self.snake_head[0] + x_direction
        y = self.snake_head[1] + y_direction
        if not self.in_bounds(x, y):
            self.game_over()
        
        if not self.running:
            return

        if self.grid[x][y][1] > 0:
            self.game_over()
        
        if self.grid[x][y][0] == grid_object["FOOD"]:
            self.grow(self.snake_head[0], self.snake_head[1], self.grid[self.snake_head[0]][self.snake_head[1]][1])
            self.respawn_food()

    def get_player_direction(self):
        
        x_direciton = 0
        y_direciton = 0

        for event in pygame.event.get():  # User did something
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    y_direciton = 1
                    x_direciton = 0
                if event.key == pygame.K_UP:
                    y_direciton = -1
                    x_direciton = 0
                if event.key == pygame.K_LEFT:
                    y_direciton = 0
                    x_direciton = -1
                if event.key == pygame.K_RIGHT:
                    y_direciton = 0
                    x_direciton = 1

        return (x_direciton, y_direciton)

    def update_snake(self, x_direction, y_direction):
        # update head
        x = self.snake_head[0]
        y = self.snake_head[1]

        size = self.grid[x][y][1]

        self.grid[self.snake_head[0] + x_direction][self.snake_head[1] + y_direction] = (grid_object['SNAKE'], size)
        self.snake_head = (self.snake_head[0] + x_direction, self.snake_head[1] + y_direction)

        neighbour = (-1, 1)
        
        # decrement body
        for segment in range(size):
            print("Segment: ", segment)
            print("val before: ", self.grid[x][y][1])
            val = self.grid[x][y][1] - 1
            if val == 0:
                self.grid[x][y] = (grid_object["NONE"], -1)
            else:
                self.grid[x][y] = (grid_object["SNAKE"], val)

            print("val after: ", self.grid[x][y][1])
            

            next_x = x
            next_y = y

            for del_x in neighbour:
                if self.in_bounds(x + del_x, y):
                    if self.grid[x + del_x][y][1] == val:
                        next_x = x + del_x
                        break

            for del_y in neighbour:
                if self.in_bounds(x, y + del_y):
                    if self.grid[x][y + del_y][1] == val:
                        next_y = y + del_y
                        break

            print("next_val seek", val, " x: ", next_x, " y: ", next_y)

            if next_x == x and next_y == y:
                break
            else:
                x = next_x
                y = next_y
            

        

    def advance_frame(self):
        player_direction = self.get_player_direction()

        x = self.snake_head[0]
        y = self.snake_head[1]
        size = self.grid[self.snake_head[0]][self.snake_head[1]][1]

        neighbour = (-1, 1)
            
        for del_x in neighbour:
            if  self.in_bounds(x + del_x, y):
                if self.grid[x + del_x][y][1] == size - 1:
                    x = x + del_x
                    break

        for del_y in neighbour:
            if self.in_bounds(x, y + del_y):
                if self.grid[x][y + del_y][1] == size - 1:
                    y = y + del_y
                    break

        snake_body_direction = (x - self.snake_head[0], y - self.snake_head[1])

        if snake_body_direction == player_direction or player_direction[0] == player_direction[1]:
            x_dir = snake_body_direction[0] * -1
            y_dir = snake_body_direction[1] * -1
        else:
            x_dir = player_direction[0]
            y_dir = player_direction[1]
            
        self.check_collision(x_dir, y_dir)
        
        if self.running:
            self.update_snake(x_dir, y_dir)

        self.render()
        
    def render(self):
        for column in range(self.width):
            for row in range(self.height):
                if self.grid[column][row][1] > 0:
                    pygame.draw.rect(screen, (254, 0, 0), [column*pixel_width, row*pixel_width, pixel_width, pixel_width])

                elif self.grid[column][row][0] == grid_object["FOOD"]:
                    pygame.draw.rect(screen, (0, 254, 0), [column*pixel_width, row*pixel_width, pixel_width, pixel_width])

                else:
                    pygame.draw.rect(screen, (0, 0, 0), [column*pixel_width, row*pixel_width, pixel_width, pixel_width])

        pygame.draw.rect(screen, (254, 254, 0), [self.snake_head[0]*pixel_width, self.snake_head[1]*pixel_width, pixel_width, pixel_width])




pixel_width = 10
width = 100
height = 100

pygame.init()
clock = pygame.time.Clock()
done = False

screen = pygame.display.set_mode(((width * pixel_width), (height * pixel_width)))
   
grid = Grid(width, height)
grid.start()

while not done:
    
    
    while grid.running:
        clock.tick(60)
        screen.fill("black")
        grid.advance_frame()
        pygame.display.update()
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
                running = False

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
            
