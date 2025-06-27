import random
import machine
import neopixel

num = 2 * 8 * 32
np = neopixel.NeoPixel(machine.Pin(38), num)

# dict could be enum in c++
grid_object = {
    "NONE" : 0,
    "FOOD" : 1,
    "SNAKE" : 2,
}

# struct space_data
# grid_object, int
    

def set_player_direction():

    global x_move
    global y_move

#     for event in pygame.event.get():  # User did something
#         if event.type == pygame.QUIT:  # If user clicked close
#             global done
#             done = True  # Flag that we are done so we exit this loop
# 
# 
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_DOWN:
#                 y_move = 1
#                 x_move = 0
#             if event.key == pygame.K_UP:
#                 y_move = -1
#                 x_move = 0
#             if event.key == pygame.K_LEFT:
#                 y_move = 0
#                 x_move = -1
#             if event.key == pygame.K_RIGHT:
#                 y_move = 0
#                 x_move = 1

    return (x_move, y_move)

def get_player_direction():
    return 1, 0
#     return x_move, y_move

class Grid:
    def __init__(self, width, height, speed):
        self.width = width
        self.height = height
        self.grid = [[(grid_object['NONE'], -1) for _ in range(height)] for _ in range(width)]
        self.running = False

        x1, x2 = [random.choice(range(self.width)) for _ in range(2)]
        y1, y2 = [random.choice(range(self.height)) for _ in range(2)]

        self.snake_head = (x1, y1)
        self.grid[x1][y1] = (grid_object['SNAKE'], 10)

        # self.snake_head = (50, 100)
        # self.grid[50][100] = (grid_object['SNAKE'], 5)

        self.grid[x2][y2] = (grid_object['FOOD'], -1)
        self.food = (x2, y2)
        self.food_on_timer = 0
        self.food_off_timer = 10

        self.frame = 0
        self.speed = speed

        
    def in_bounds(self, x, y):
        if x < 0 or x >= self.width:
            return False

        if y < 0 or y >= self.height:
            return False

        return True
        
    def game_over(self):
        self.running = False

    def start(self):
        direction = (0, 0)
        self.render()
        np.write()
        
        while(direction == (0, 0)):
            set_player_direction()
            temp = get_player_direction()
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
            self.food = (chosenOne[0], chosenOne[1])

    def move_food(self):
        # print(self.food_on_timer, self.food_off_timer)
        if self.food_off_timer == 0:
            self.food_on_timer -= 1
            if self.food_on_timer <= 0:
                self.food_off_timer = int(200 * random.random())
                self.food_on_timer = int(20 * random.random())

            free = []
            search = [-1, 0, 1]
            for column in search:
                for row in search:
                    if self.in_bounds(self.food[0] + column, self.food[1] + row):
                        if not self.grid[self.food[0] + column][self.food[1] + row][1] > 0:
                            free.append((self.food[0] + column, self.food[1] + row))
            if len(free):
                chosenOne = random.choice(free)
                self.grid[self.food[0]][self.food[1]] = (grid_object['NONE'], -1)
                self.food = (chosenOne[0], chosenOne[1])
                self.grid[chosenOne[0]][chosenOne[1]] = (grid_object['FOOD'], -1)
        else:
            self.food_off_timer -= 1

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
            val = self.grid[x][y][1] - 1
            if val == 0:
                self.grid[x][y] = (grid_object["NONE"], -1)
            else:
                self.grid[x][y] = (grid_object["SNAKE"], val)

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

            if next_x == x and next_y == y:
                break
            else:
                x = next_x
                y = next_y

    def advance_frame(self):
        self.frame += 1
        player_direction = get_player_direction()
        print(self.food)
        
        if self.running:
            self.move_food()
            if self.frame == self.speed:
                

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
                self.frame = 0

        self.render()
        
    def coord_to_np_index(self, x, y):
        if y < 8:
            if x % 2 == 0: #even
                num = 8 * x + y
            else:
                num = 8 * x + (7 - y)
        else:
            if not x % 2 == 0: #even
                num = 256 + 8 * (31 - x) + (7 - (y % 8))
            else:
                num = 256 + 8 * (31 - x) + (y % 8)
                
        return num
        
    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                num = self.coord_to_np_index(x, y)
                

                if self.grid[x][y][0] == grid_object['FOOD']:
                        np[num] = (0, 254, 0)
                elif self.grid[x][y][0] == grid_object['SNAKE']:
                    np[num] = (254, 0, 0)
                else:
                    np[num] = (0, 0, 0)
        np[self.coord_to_np_index(self.snake_head[0], self.snake_head[1])] = (254, 100, 0)
    


pixel_width = 20
width = 32
height = 16
x_move = 0
y_move = 0

# pygame.init()
# clock = pygame.time.Clock()
done = False

# screen = pygame.display.set_mode(((width * pixel_width), (height * pixel_width)))
   
grid = Grid(width, height, 2)
grid.start()

while not done:
    set_player_direction()
    
    if grid.running:
        # clock.tick(60)
        # screen.fill("black")
        grid.advance_frame()
        # pygame.display.update()

        np.write()
        # for event in pygame.event.get():  # User did something
        #     if event.type == pygame.QUIT:  # If user clicked close
        #         done = True  # Flag that we are done so we exit this loop
        #         running = False
            


"""
def display(grid):
    for y in range(grid.height):
        # pygame.draw.line(screen, (40, 40, 40), [0, ypixelWidth], [grid.widthpixelWidth, ypixelWidth], 5)
        for x in range(grid.width):
            # if y == 0:
            #     pygame.draw.line(screen, (40, 40, 40), [xpixelWidth, 0], [xpixelWidth, grid.heightpixelWidth], 5)
            num = 0
            material = grid.get(x, y)
            if y < 8:
                if x % 2 == 0: #even
                    num = 8 * x + y
                else:
                    num = 8 * x + (7 - y)

                if material.element.name == "air":
                    np[num] = (0, 0, 0)
                else:
                    np[num] = (material.element.colour.r, material.element.colour.g, material.element.colour.b)
            else:
                if not x % 2 == 0: #even
                    num = 256 + 8 * (31 - x) + (7 - (y % 8))
                else:
                    num = 256 + 8 * (31 - x) + (y % 8)
                if material.element.name == "air":
                    np[num] = (0, 0, 0)
                else:
                    np[num] = (material.element.colour.r, material.element.colour.g, material.element.colour.b)
import machine, neopixel, time
import random
import math
import gc
num = 2 * 8 * 32
np = neopixel.NeoPixel(machine.Pin(38), num)
from machine import Pin, ADC
import timedef render(self):
        f

led = Pin("LED", Pin.OUT)

purple = 21 #left
green = 27 # right
yellow = 20 # top
blue = 26 # bottom

regulator_mode_pin = machine.Pin(23, machine.Pin.OUT)

left = Pin(purple, Pin.OUT)
right = Pin(green, Pin.OUT)
top = ADC(Pin(blue))
bot = Pin(yellow, Pin.IN)
def getXTouch():
    xHIGH = Pin(purple, Pin.OUT)
    xLOW = Pin(green, Pin.OUT)
    Pin(yellow, Pin.IN)

    xHIGH.value(1)
    xLOW.value(0)

    time.sleep(0.020)  # Debounce delay
    adc_value = ADC(Pin(blue)).read_u16()
    return adc_value

def getYTouch():
    yHIGH = Pin(yellow, Pin.OUT)
    yLOW = Pin(blue, Pin.OUT)
    Pin(purple, Pin.IN)

    yHIGH.value(1)
    yLOW.value(0)

    time.sleep(0.020)  # Debounce delay
    adc_value = ADC(Pin(green)).read_u16()
    return adc_value

print("starting...")

print("enter loop...")
regulator_mode_pin.value(1)
while True:
    led.off()
    x = getXTouch()
    #time.sleep(0.1)
    led.on()
    y = getYTouch()
    #time.sleep(0.1)
    print("X:", x, "Y:", y)

"""

