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
    "ENEMY_SNAKE": 3,
    "BARRIER": 4,
    "DEAD_SNAKE": 5,
}

obstacle_1 = (
    (0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3), (0, 3), (0, 2)
)
obstacle_2 = (
    (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (3, 4), (2, 4), (1, 4), (0, 4), (0, 3), (0, 1)
)
obstacle_3 = (
    (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (0, 1), (0, 2), (0, 3), (0, 4), (-1, 0), (-2, 0), (-3, 0), (-4, 0), (0, -1), (0, -2), (0, -3), (0, -4), 
)
obstacle_4 = (
    (0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2), 
)
obstacle_5 = (
    (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), 
)
obstacle_6 = (
    (0, 0), (1, 0), (2, 0), (1, 1), (1, -1)
)
obstacle_7 = (
    (0, 0), (1, 1), (2, 2), (3, 3)
)
obstacle_8 = (
    (0, 0), (1, 1), (2, 2), (1, -1), (2, -2), (-1, 1), (-2, 2), (-1, -1), (-2, -2), 
)


obstacle_list = (
    obstacle_1, 
    obstacle_2,
    obstacle_3,
    obstacle_4,
    obstacle_5,
    obstacle_6,
    obstacle_7,
    obstacle_8,
)

regular_food_amount = 1300
dead_snake_food_amount = 100

wallpaper = False

# struct space_data
# grid_object, int
    


def set_player_direction():

    global x_move
    global y_move

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            global done
            done = True  # Flag that we are done so we exit this loop


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                y_move = 1
                x_move = 0
            if event.key == pygame.K_UP:
                y_move = -1
                x_move = 0
            if event.key == pygame.K_LEFT:
                y_move = 0
                x_move = -1
            if event.key == pygame.K_RIGHT:
                y_move = 0
                x_move = 1

    return (x_move, y_move)

def get_player_direction():
    global x_move
    global y_move
    
    return (x_move, y_move)

def reset_player_direction():
    global x_move
    global y_move
    y_move = 0
    x_move = 0

class Snake:
    def __init__(self, length, scale = 1):
        self.init_length = length
        self.scale = scale
        self.reset()
        
    def reset(self):
        self.length = self.init_length
        self.direction = random.choice(((1, 0), (-1, 0), (0, 1), (0, -1)))
        self.head = None
        self.goal_pos = None
        self.hunt = False
        self.hunt_timeout = 0
        self.hunt_timeout_limit = 100
        self.scale = 1

    def grow(self, amount):
        self.length += amount
        return self.length


class Grid:
    def __init__(self, width, height, speed, snake_list):
        self.width = width
        self.height = height
        self.speed = speed
        self.snake_list = snake_list
        self.reset()

    def add_snake(self, snake):
        if isinstance(snake, Snake):
            self.snake_list.append(snake) 

    def cleanup_snake(self, snake):
        if isinstance(snake, Snake):
            x, y = snake.head
            neighbour = (-1, 1)
            # decrement body
            for _ in range(int(snake.length/100 + 1)):
                val = snake.length - (_ + 1) * 100
                self.grid[x][y] = (grid_object["NONE"], -1)
                # self.grid[x][y] = (grid_object["FOOD"], 100)

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

    def reset_snake(self, snake):
        if isinstance(snake, Snake):
            self.cleanup_snake(snake)

            snake.reset()
            
            free = self.list_free_coordinates()
            snake.head = random.choice(free)

            offset_x = random.choice(range(-15, 16))
            offset_y = random.choice(range(-15, 16))

            snake.goal_pos = (snake.head[0] + offset_x, snake.head[1] + offset_y)

        
    def in_bounds(self, x, y):
        if x < 0 or x >= self.width:
            return False

        if y < 0 or y >= self.height:
            return False

        return True
        
    def game_over(self):
        self.running = False
        self.reset()
        reset_player_direction()
        self.start()

    def reset(self):
        self.grid = [[(grid_object['NONE'], -1) for _ in range(height)] for _ in range(width)]
        self.running = False

        for _ in range(self.width):
            self.grid[_][0] = (grid_object["BARRIER"], 0)
            self.grid[_][self.height - 1] = (grid_object["BARRIER"], 0)
            

        for _ in range(self.height):
            self.grid[0][_] = (grid_object["BARRIER"], 0)
            self.grid[self.width - 1][_] = (grid_object["BARRIER"], 0)
            

        #place obstacles:
        for _ in range(16):
            scale = random.choice(range(1, 5))
            direction = random.choice(((1, 0), (-1, 0), (0, 1), (0, -1)))
            randx = random.choice(range(self.width))
            randy = random.choice(range(self.height))

            self.create_obstacle((randx, randy), direction, random.choice(obstacle_list), scale)

        #populate the rest
        snake_list_length = len(self.snake_list)

        free = []
        for look_x in range(self.width):
            for look_y in range (self.height):
                if self.grid[look_x][look_y][0] == grid_object["NONE"]:
                    free.append((look_x, look_y))

        rand_coord = random.choices(free, k=snake_list_length + 1)
    
        offset_x = random.choices(range(-15, 16), k=snake_list_length + 1)
        offset_y = random.choices(range(-15, 16), k=snake_list_length + 1)


        for idx, snake in enumerate(self.snake_list):
                snake.head = (rand_coord[idx][0], rand_coord[idx][1])
                snake.length = snake.init_length
                snake.goal_pos = (rand_coord[idx][0] + offset_x[idx], rand_coord[idx][1] + offset_y[idx])

        # self.snake_head = (50, 100)
        # self.grid[50][100] = (grid_object['SNAKE'], 5)
        x2, y2 = free[idx]

        self.grid[x2][y2] = (grid_object['FOOD'], regular_food_amount)
        self.food = (x2, y2)
        self.food_on_timer = 0
        self.food_off_timer = 10
        self.frame = 0

    def start(self):
        direction = (1, 0)
        self.render()
        pygame.display.update()
        
        
        # while(direction == (0, 0)):
        #     set_player_direction()
        #     temp = get_player_direction()
        #     if temp == (0, 0):
        #         pass
        #     elif self.in_bounds(self.snake_head[0] + temp[0], self.snake_head[1] + temp[1]):
        #         direction = temp
        grid.running = True
        # self.update_snake(direction[0], direction[1], self.snake_list[0]) 
        
    def list_free_coordinates(self):
        coords = []
        for x in range(width):
            for y in range(height):
                if self.grid[x][y][0] == grid_object["NONE"]:
                    coords.append((x, y))
        return coords

    

    def respawn_food(self):
        free = self.list_free_coordinates()
        if len(free):
            chosenOne = random.choice(free)
            self.grid[chosenOne[0]][chosenOne[1]] = (grid_object['FOOD'], regular_food_amount)
            self.food = (chosenOne[0], chosenOne[1])

    def move_food(self):
        if self.food_off_timer == 0:
            self.food_on_timer -= 1
            if self.food_on_timer <= 0:
                self.food_off_timer = int(100 * random.random())
                self.food_on_timer = int(20 * random.random())

            free = []
            search = [-1, 0, 1]
            for column in search:
                for row in search:
                    if self.in_bounds(self.food[0] + column, self.food[1] + row):
                        if self.grid[self.food[0] + column][self.food[1] + row][0] == grid_object["NONE"]:
                            free.append((self.food[0] + column, self.food[1] + row))
            if len(free):
                chosenOne = random.choice(free)
                self.grid[self.food[0]][self.food[1]] = (grid_object['NONE'], 0)
                self.food = (chosenOne[0], chosenOne[1])
                self.grid[chosenOne[0]][chosenOne[1]] = (grid_object['FOOD'], regular_food_amount)
        else:
            self.food_off_timer -= 1
        

    def check_collision(self, x_direction, y_direction, snake):
        # for snake in self.snake_list:
        x = snake.head[0] + x_direction
        y = snake.head[1] + y_direction
        if not self.in_bounds(x, y):
            # self.game_over()
            self.reset_snake(snake)
            return False
        
        if self.grid[x][y][0] == grid_object["SNAKE"] and self.grid[snake.head[0]][snake.head[1]][0] == grid_object["SNAKE"] and not snake.direction == (0, 0):
            self.game_over()
            print("AHSUHFKJASBFDSHFKJSDF")
            return False
                                                                                                                

        if not self.running:
            return False


        if self.grid[x][y][0] == grid_object["BARRIER"] or self.grid[x][y][0] == grid_object["ENEMY_SNAKE"]:
            # self.game_over()
            self.reset_snake(snake)
            return False
        
        if self.grid[x][y][0] == grid_object["SNAKE"] and not self.grid[snake.head[0]][snake.head[1]][0] == grid_object["SNAKE"]:
            # snake.grow(3.0)

            if self.snake_list[0].head == (x, y):
                # self.game_over()
                self.reset_snake(self.snake_list[0])
                return False
            
            snake.grow(dead_snake_food_amount)
            # SOME METHOD OF TURNING THE REST OF THE SNAKE INTO FOOD

            val = self.grid[x][y][1]
            print("FOOD VAL: ", val)
            head_val = val
            prev_head_coords = (x, y)
            # print("length 1", self.snake_list[0].length / 100, val)
            # self.snake_list[0].length -= (int(val / 100)) * 100
            # print("length 2", self.snake_list[0].length / 100)

            # while not prev_head_coords == self.snake_list[0].head and not head_val < 100:
            #     # Trying to get to the head
            #     head_coords, head_val = self.get_next_snake_segment(prev_head_coords[0], prev_head_coords[1], True)
            #     if not head_coords == self.snake_list[0].head or not head_val < 100:
            #         self.grid[prev_head_coords[0]][prev_head_coords[1]] = (grid_object["SNAKE"], head_val - int(val / 100) * 100) 
            #         prev_head_coords = head_coords
            # for _ in range(int(self.snake_list[0].length / 100)):
            #     head_x, head_y = self.snake_list[0].head

                # coords, head_val = self.get_next_snake_segment(prev_head_coords[0], prev_head_coords[1], True)
                # print(head_val)


                # # print(head_val, head_val - int(val / 100) * 100)
                # print("now head: ", head_val - int(val / 100) * 100)
                # if coords == self.snake_list[0].head or head_val == self.snake_list[0].length or head_val == -1:
                #     print("REACHED HEAD")
                #     break
                # self.grid[prev_head_coords[0]][prev_head_coords[1]] = (grid_object["SNAKE"], head_val - int(val / 100) * 100 + 100) 
                # prev_head_coords = coords

                
            for _ in range(int(self.grid[x][y][1] / 100)):
                print("TURN TO FOOD", x, y)
                coords, val = self.get_next_snake_segment(x, y, False)
                self.grid[x][y] = (grid_object["DEAD_SNAKE"], dead_snake_food_amount)
                if val == -1:
                    break
                
                
                x, y = coords

            head_x, head_y = self.snake_list[0].head
            print(head_x, head_y, head_val)
            snake_stored_coords = []
            for _ in range(int(self.snake_list[0].length / 100)):
                coords, val = self.get_next_snake_segment(head_x, head_y, False)
                
                print(coords, val, val - int(head_val / 100) * 100)
                if val - int(head_val / 100) * 100 == -1:
                    # self.grid[head_x][head_y] = (grid_object["NONE"], 0)
                    break
                snake_stored_coords.append(coords)
                # self.grid[head_x][head_y] = (grid_object['SNAKE'], val + 100 - int(head_val / 100) * 100)
                
                head_x, head_y = coords[0], coords[1]
                
                
            for coord in snake_stored_coords:
                val = self.grid[coord[0]][coord[1]][1]
                if val < 100:
                    # self.grid[coord[0]][coord[1]] = (grid_object["NONE"], 0)
                    pass
                self.grid[coord[0]][coord[1]] = (grid_object['SNAKE'], val - int(head_val / 100) * 100)
                print(val, val + 100 - int(head_val / 100) * 100)

            self.snake_list[0].length -= (int(head_val / 100)) * 100

            # self.respawn_food()
            # self.reset_snake(snake)
            return True

        if self.grid[x][y][0] == grid_object["DEAD_SNAKE"]:
            snake.grow(self.grid[x][y][1])
            return True

        if self.grid[x][y][0] == grid_object["FOOD"]:
            # snake.grow(3.0)
            snake.grow(self.grid[x][y][1])
            self.respawn_food()
            return True
        return True

    def update_snake(self, x_direction, y_direction, snake, is_player):
        # update head
        x = snake.head[0]
        y = snake.head[1]

        if not self.in_bounds(x + x_direction, y + y_direction):
            return

        size = snake.length

        if is_player:
            self.grid[snake.head[0] + x_direction][snake.head[1] + y_direction] = (grid_object["SNAKE"], size)
        else:
            self.grid[snake.head[0] + x_direction][snake.head[1] + y_direction] = (grid_object["ENEMY_SNAKE"], size)
        snake.head = (snake.head[0] + x_direction, snake.head[1] + y_direction)

        neighbour = (-1, 1)
        # decrement body
        for _ in range(int(size/100)):
            val = size - (_ + 1) * 100
            if val >= 0 and val < 100:
                self.grid[x][y] = (grid_object["NONE"], -1)
                break
            else:
                if is_player:
                    self.grid[x][y] = (grid_object["SNAKE"], val)
                else:
                    self.grid[x][y] = (grid_object["ENEMY_SNAKE"], val)

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

    def get_next_snake_segment(self, x, y, ascending):
        next = 100 if ascending else -100

        value = self.grid[x][y][1]
        if not value > 0:
            return (-1, -1), -1

        val = value + next

        next_x = x
        next_y = y

        neighbour = (-1, 1)

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
            return (-1, -1), -1
        else:
            return ((next_x, next_y), val)


    def advance_frame(self):
        self.frame += 1
        set_player_direction()
        # print(self.food)
        
        # print("FRAME ",random.randint(0, 100))
        if self.running:
            self.move_food()
            if self.frame == self.speed:
                player = True
                print("FRAME")
                for snake in self.snake_list:
                    if player and not wallpaper:
                        snake.direction = get_player_direction()
                    else:
                        self.find_goal_position(snake)
                        snake.direction = pathfind(snake.goal_pos, snake.head, snake.direction, 15)
                    player_direction = snake.direction
                    # print(player_direction)s
                    x = snake.head[0]
                    y = snake.head[1]
                    size = snake.length
                    # print(size)

                    neighbour = (-1, 1)
                        
                    for del_x in neighbour:
                        if self.in_bounds(x + del_x, y):
                            if self.grid[x + del_x][y][1] == size - 100:
                                x = x + del_x
                                break

                    for del_y in neighbour:
                        if self.in_bounds(x, y + del_y):
                            if self.grid[x][y + del_y][1] == size - 100:
                                y = y + del_y
                                break

                    snake_body_direction = (x - snake.head[0], y - snake.head[1])

                    if snake_body_direction == player_direction or player_direction[0] == player_direction[1]:
                        x_dir = snake_body_direction[0] * -1
                        y_dir = snake_body_direction[1] * -1
                    else:
                        x_dir = player_direction[0]
                        y_dir = player_direction[1]
                        
                    if not self.check_collision(x_dir, y_dir, snake):
                        x_dir, y_dir = 0, 0
                        # snake.length -= 100

                    self.update_snake(x_dir, y_dir, snake, player)


                    # if self.check_collision(x_dir, y_dir, snake):
                    #     self.update_snake(x_dir, y_dir, snake)
                    if player:
                        player = False
                self.frame = 0
                    
        
        self.render()
        
    def render(self):
        if not wallpaper:
            player_offset = (self.snake_list[0].head[0] + self.width / 2, self.snake_list[0].head[1] + self.height / 2 )
        else:
            player_offset = (self.width, self.height)

        for column in range(self.width):
            for row in range(self.height):
                if self.grid[column][row][0] == grid_object["SNAKE"]:
                    # pygame.draw.rect(screen, (254, 0, 0), [column*pixel_width, row*pixel_width, pixel_width, pixel_width])
                    if int(self.grid[column][row][1]/100) % 2 == 0:
                        const = 255 / (int(self.grid[column][row][1])/100)
                    else:
                        const = 100
                    if const < 0:
                        const = 50
                    pygame.draw.rect(screen, (60, 200 - const, 60), [((column - player_offset[0])+self.width)*pixel_width, ((row - player_offset[1])+self.height) *pixel_width, pixel_width, pixel_width])

                elif self.grid[column][row][0] == grid_object["ENEMY_SNAKE"]:
                    # pygame.draw.rect(screen, (254, 0, 0), [column*pixel_width, row*pixel_width, pixel_width, pixel_width])
                    if int(self.grid[column][row][1]/100) % 2 == 0:
                        const = 255 / (int(self.grid[column][row][1])/100)
                    else:
                        const = 125
                    pygame.draw.rect(screen, (255 - const, 30, 30), [((column - player_offset[0])+self.width)*pixel_width, ((row - player_offset[1])+self.height) *pixel_width, pixel_width, pixel_width])

                elif self.grid[column][row][0] == grid_object["FOOD"]:
                    pygame.draw.rect(screen, (0, 254, 0), [((column - player_offset[0])+self.width)*pixel_width, ((row - player_offset[1])+self.height) *pixel_width, pixel_width, pixel_width])

                elif self.grid[column][row][0] == grid_object["BARRIER"]:
                    pygame.draw.rect(screen, (254, 154, 50), [((column - player_offset[0])+self.width)*pixel_width, ((row - player_offset[1])+self.height) *pixel_width, pixel_width, pixel_width])
                elif self.grid[column][row][0] == grid_object["DEAD_SNAKE"]:
                    pygame.draw.rect(screen, (100, 100, 200), [((column - player_offset[0])+self.width)*pixel_width, ((row - player_offset[1])+self.height) *pixel_width, pixel_width, pixel_width])
                # else:
                #     pygame.draw.rect(screen, (0, 0, 0), [column*pixel_width, row*pixel_width, pixel_width, pixel_width])
        player = True
        for snake in self.snake_list:
            if player:
                pygame.draw.rect(screen, (254, 100, 125), [((snake.head[0] - player_offset[0])+self.width)*pixel_width, ((snake.head[1] - player_offset[1])+self.height)*pixel_width, pixel_width, pixel_width])
                player = False
            else:

                pygame.draw.rect(screen, (254, 100, 0), [((snake.head[0] - player_offset[0])+self.width)*pixel_width, ((snake.head[1] - player_offset[1])+self.height)*pixel_width, pixel_width, pixel_width])

    def is_close_to_food(self, snake):
        if self.in_bounds(snake.goal_pos[0], snake.goal_pos[1]) and self.grid[snake.goal_pos[0]][snake.goal_pos[1]][0] == grid_object["FOOD"]:
            return snake.goal_pos 
        for front_search in range(1, 20):
            for side_seach in range (-15, 16):
                if not snake.direction[0] == 0:
                    search_x = snake.head[0] + snake.direction[0] * front_search
                    search_y = snake.head[1] + side_seach
                else:
                    search_x = snake.head[0] + side_seach
                    search_y = snake.head[1] + snake.direction[1] * front_search

                if self.in_bounds(search_x, search_y) and self.grid[search_x][search_y][0] == grid_object["FOOD"]:
                    snake.hunt = True
                    return (search_x, search_y)
                
                if self.in_bounds(search_x, search_y) and self.grid[search_x][search_y][0] == grid_object["DEAD_SNAKE"]:
                    snake.hunt = True
                    return (search_x, search_y)

                if self.in_bounds(search_x, search_y) and self.grid[search_x][search_y][0] == grid_object["SNAKE"]:
                    if (snake.length > self.snake_list[0].length):
                        snake.hunt = True
                        return (search_x, search_y)
        return snake.goal_pos


    def find_goal_position(self, snake):
        snake.hunt_timeout += 1
        
        snake.goal_pos = self.is_close_to_food(snake)

        if snake.hunt:
            if snake.head == snake.goal_pos or not self.in_bounds(snake.goal_pos[0], snake.goal_pos[1]) or snake.hunt_timeout >= snake.hunt_timeout_limit * 2:
                snake.hunt = False
                snake.hunt_timeout = 0
                offset_x = random.choice(range(-30, 31))
                offset_y = random.choice(range(-30, 31))
                snake.goal_pos = (snake.head[0] + offset_x, snake.head[1] + offset_y)

        else:
            if snake.head == snake.goal_pos or not self.in_bounds(snake.goal_pos[0], snake.goal_pos[1]) or snake.hunt_timeout >= snake.hunt_timeout_limit:
                offset_x = random.choice(range(-30, 31))
                offset_y = random.choice(range(-30, 31))
                snake.hunt_timeout = 0

                snake.goal_pos = (snake.head[0] + offset_x, snake.head[1] + offset_y)

    def create_obstacle(self, spawn_point, direction, coords_list, scale = 1):
        for coords in coords_list:
            for scale_x in range(scale):
                for scale_y in range(scale):
                    scaled_coords_x = coords[0] * scale + scale_x
                    scaled_coords_y = coords[1] * scale + scale_y

                    if direction == (1, 0):
                        x, y = spawn_point[0] + scaled_coords_x ,spawn_point[1] + scaled_coords_y
                    elif direction == (0, 1):
                        y, x = spawn_point[0] + scaled_coords_x ,spawn_point[1] + scaled_coords_y
                    elif direction == (-1, 0):
                        x, y = spawn_point[0] - scaled_coords_x ,spawn_point[1] + scaled_coords_y
                    elif direction == (0, -1):
                        y, x = spawn_point[0] - scaled_coords_x ,spawn_point[1] - scaled_coords_y
                    else:
                        return
                    if self.in_bounds(x, y):
                        self.grid[x][y] = (grid_object["BARRIER"], 0)



    # def find_closest_direction(self, goal_pos, current_pos, direction):
    #     smallest_distance = 99

    #     for entry in self.get_possible_directions(direction):
    #         start_point = current_pos
    #         start_point = current_pos + entry
    #         dist = abs(start_point[0] - goal_pos[0]) + abs(start_point[1] - goal_pos[1])
    #         if dist < smallest_distance:
    #             smallest_distance = abs(start_point[0] - goal_pos[0]) + abs(start_point[1] - goal_pos[1])
    #             direction = entry

    #     return direction
    

def get_possible_directions(direction):
        # current = get_player_direction()

        pool = (
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0)
        )
        possible = []
        reverse = (-direction[0], -direction[1])
        for entry in pool:
            if not entry == reverse:
                possible.append(entry) 
        return possible

def rank_closest_direction(goal_pos, current_pos, direction):
    distances = []
    directions = get_possible_directions(direction)
    for entry in directions:
        start_point = (current_pos[0] + entry[0], current_pos[1] + entry[1])
        dist = pow((start_point[0] - goal_pos[0]), 2) + pow((start_point[1] - goal_pos[1]), 2)
        distances.append(dist)

    # print(current_pos)
    # print(direction)

    # print(directions, distances)

    

    sorted_x, sorted_y = zip(*sorted(zip(distances, directions)))

    # print(sorted_y)

    # assume sorted_y is ranked from closest to furthest
    return sorted_y


def pathfind(goal_pos, current_pos, current_direction, depth):
    # print(depth, current_pos, current_direction, goal_pos)

    if depth == 0:
        return current_direction
    if current_pos == goal_pos:
        return current_direction
    
    pool = rank_closest_direction(goal_pos, current_pos, current_direction)
    # print(pool)

    for search_direction in pool:
        new_pos = (current_pos[0] + search_direction[0], current_pos[1] + search_direction[1])
        if not grid.in_bounds(new_pos[0], new_pos[1]):
            continue
            #attempting to go out of bounds, choose another way
        if grid.grid[new_pos[0]][new_pos[1]][0] == grid_object['BARRIER'] or grid.grid[new_pos[0]][new_pos[1]][0] == grid_object['ENEMY_SNAKE']: # It would be cool here to have a check for the snake block value, and comparing it to the depth to see if, in time, the snake block will not be in the way.
            continue 
            # Bumping into a wall or enemy, choose another way
        search = pathfind(goal_pos, new_pos, search_direction, depth - 1) 
        if search == (-1, -1):
            continue
            # Search returned a dead end, go another way
        else:
            return search_direction
            # Search returned a valid path, continue with current direction
        
    return (-1, -1)
    # All paths exhausted, dead end

pixel_width = 8
width = 200
height = 100
x_move = 0
y_move = 0

pygame.init()
clock = pygame.time.Clock()
done = False

screen = pygame.display.set_mode(((width * pixel_width), (height * pixel_width)))
   
# Digit positions 1 and 2 are the initial length (ie 10), and the last two positions are the snake ID
player_snake = Snake(4099)
snake1 = Snake(1001)
snake2 = Snake(1002)
snake3 = Snake(1003)
snake4 = Snake(1004)
snake11 = Snake(1005)
snake21 = Snake(1006)
snake31 = Snake(1007)
snake41 = Snake(1008)
snake12 = Snake(1009)
snake22 = Snake(1010)
snake32 = Snake(1011)
snake42 = Snake(1012)


# grid = Grid(width, height, 6, (snake1, snake2))
# grid = Grid(width, height, 2, (player_snake, snake2, snake1, snake3, snake4, snake21, snake11, snake31, snake41, snake22, snake12, snake32, snake42))
grid = Grid(width, height, 2, (player_snake, snake2, snake1, snake3, snake4, snake21, snake11, snake31))



# grid.create_obstacle((5, 5), (1, 0), obstacle_1, 1)
# grid.create_obstacle((25, 25), (-1, 0), obstacle_1, 2)

# grid.create_obstacle((15, 15), (0, 1), obstacle_1, 3)

# grid.create_obstacle((51, 51), (0, -1), obstacle_1, 4)

grid.start()
# grid.grid[7][0] = (grid_object['BARRIER'], -1)
# grid.grid[5][1] = (grid_object['BARRIER'], -1)
# grid.grid[5][-1] = (grid_object['BARRIER'], -1)
# grid.grid[6][1] = (grid_object['BARRIER'], -1)
# grid.grid[6][-1] = (grid_object['BARRIER'], -1)


# print(pathfind((10, 0), (3, 1), (1, 0), 15))

while not done:


    # set_player_direction()
    
    if grid.running:
        clock.tick(60)
        screen.fill("black")
        grid.advance_frame()
        pygame.display.update()

    # for event in pygame.event.get():  # User did something
    #     if event.type == pygame.QUIT:  # If user clicked close
    #         done = True  # Flag that we are done so we exit this loop
    #         running = False

    # if not grid.running and (x_move, y_move) != get_player_direction():
            
