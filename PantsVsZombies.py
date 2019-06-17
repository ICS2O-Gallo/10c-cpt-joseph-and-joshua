import math
import random
import arcade

WIDTH = 1200
HEIGHT = 800

# button stuff
BTN_X = 0
BTN_Y = 1
BTN_WIDTH = 2
BTN_HEIGHT = 3
BTN_IS_CLICKED = 4
BTN_COLOR = 5
BTN_CLICKED_COLOR = 6

# Menu: 0
# Instructions: 1
# Game: 2
current_screen = 0

tick_counter = 0
# Unselected: 0
# pant: 1
# pant2: 2
# pant3: 3

grid = [[0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]]

cost_pant = 100
cost_gold = 50
cost_leather = 25

send_fabric_error = False
fabric = 50

# 0: unselected
# 1: pant
mouse_select = 0

instruction_button = [(WIDTH - 190) / 2, HEIGHT - 560,
                      190, 50, arcade.color.GRAY, arcade.color.RED]
game_button = [(WIDTH - 190) / 2, HEIGHT - 710, 190, 50,
               arcade.color.BLACK, arcade.color.BLUE]

# grid
grid_col_1 = arcade.color.GREEN
grid_col_2 = arcade.color.DARK_GREEN

gridGenerator = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

mousePos = [0, 0]
selected = -1


class Fabric(arcade.Sprite):
    def __init__(self, start_x=None, start_y=None):
        if (start_x is not None) and (start_y is not None):
            super().__init__('.\\assets\\fabric.png', scale=3,
                             center_x=start_x, center_y=start_y)
        else:
            super().__init__('.\\assets\\fabric.png', scale=3,
                             center_x=random.randrange(WIDTH), center_y=HEIGHT)

    def update(self):
        self.center_y -= 5
        if self.top < 0:
            self.kill()


class Zombie(arcade.Sprite):
    def __init__(self, row, speed=5, health=10):
        center_x = 1050
        center_y = [50, 150, 250, 350, 450, 550, 650][row]
        super().__init__('.\\assets\\red_circle.png', center_x=center_x,
                         center_y=center_y)
        self.health = health
        self.speed = speed

    def walk(self):
        global current_screen
        self.set_position(self.center_x - self.speed, self.center_y)
        if self.right <= 0:
            current_screen = 3

    def eat(self):
        try:
            round_x = square_round(self.center_x)
            round_y = square_round(self.center_y)
            if grid[round_x][round_y] == 35:
                self.kill()
            grid[round_x][round_y] = 0
        except:
            pass

    def hit(self, damage=1):
        self.health -= damage
        if self.health <= 0:
            self.kill()


def level_generator(tick):
    if tick < 50:
        return []
    elif tick == 50:
        return [3]
    elif tick < 104:
        return []
    if tick % 35 == 0:
        random_number = random.random()
        for i in range(7, 1, -1):
            if random_number < ((1/2) ** (i - tick/200)):
                return random.sample(set(range(7)), i)
        return [random.choice(range(7))]
    return []


# Testing data
zombie_sprites = arcade.SpriteList()

pant_sprites = arcade.SpriteList()
fabric_sprites = arcade.SpriteList()

mouse_hidden_sprite = arcade.Sprite('.\\assets\\hidden_pixel.png')


def setup():
    arcade.open_window(WIDTH, HEIGHT, "Pants Vs. Zombies")
    arcade.set_background_color(arcade.color.WHITE)
    arcade.schedule(update, 1 / 60)
    window = arcade.get_window()
    window.on_draw = on_draw
    window.on_key_press = on_key_press
    window.on_key_release = on_key_release
    window.on_mouse_press = on_mouse_press
    window.on_mouse_release = on_mouse_release
    window.on_mouse_motion = mouse_motion

    arcade.run()


def update(delta_time):
    global fabric
    if current_screen == 2:
        for i in zombie_sprites:
            i.walk()
            i.eat()
            hit_list = arcade.check_for_collision_with_list(i, pant_sprites)
            for projectile in hit_list:
                i.hit()
                projectile.kill()
        if tick_counter % 30 == 1:
            fabric_sprites.append(Fabric())
        fabric_sprites.update()
        hit_list = arcade.check_for_collision_with_list(
            mouse_hidden_sprite, fabric_sprites)
        for _fabric in hit_list:
            _fabric.kill()
            fabric += 25
        if (len(pant_sprites)) >= 250:
            pant_sprites[0].kill()


def on_draw():
    global tick_counter
    arcade.start_render()
    # menu
    if current_screen == 0:
        arcade.set_background_color(arcade.color.GREEN)
        arcade.draw_text("Pants VS Zombies", WIDTH / 2, HEIGHT - 100,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        draw_instruction_button(instruction_button)
        draw_game_button(game_button)
        arcade.draw_text("Instructions", WIDTH / 2, HEIGHT - 550,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        arcade.draw_text("Play", WIDTH / 2, HEIGHT - 700,
                         arcade.color.BLACK, font_size=30, anchor_x="center")

    # instructions
    elif current_screen == 1:
        arcade.set_background_color(arcade.color.GRAY)
        arcade.draw_text("Instructions", WIDTH / 2, HEIGHT - 100,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        draw_instructions("instructions")
        arcade.draw_text("Esc to go to Menu", WIDTH - 1000, HEIGHT - 700,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        
    # game
    elif current_screen == 2:
        tick_counter += 1
        for i in level_generator(tick_counter):
            zombie_sprites.append(Zombie(i))
        setup_grid(grid_col_1, grid_col_2)
        for i in gridGenerator[:-1]:
            arcade.draw_rectangle_filled(
                i + 50, HEIGHT - 50, 100, 100, arcade.color.BLACK_BEAN)
            arcade.draw_rectangle_filled(
                i + 50, HEIGHT - 50, 90, 90, arcade.color.ALLOY_ORANGE)

        arcade.draw_texture_rectangle(
            150, HEIGHT - 50, 100, 100,
            arcade.load_texture('.\\assets\\diamond.png'))
        arcade.draw_texture_rectangle(
            250, HEIGHT - 50, 100, 100,
            arcade.load_texture('.\\assets\\gold.png'))
        arcade.draw_texture_rectangle(
            350, HEIGHT - 50, 100, 100,
            arcade.load_texture('.\\assets\\leather.png'))
        global mouse_select, send_fabric_error
        if mouse_select == 1:
            arcade.draw_rectangle_outline(
                150, HEIGHT - 50, 90, 90,
                color=arcade.color.RED, border_width=5)
        elif mouse_select == 2:
            arcade.draw_rectangle_outline(
                250, HEIGHT - 50, 90, 90,
                color=arcade.color.RED, border_width=5)
        elif mouse_select == 3:
            arcade.draw_rectangle_outline(
                350, HEIGHT - 50, 90, 90,
                color=arcade.color.RED, border_width=5)
        grid_counter = -1
        for row in grid:
            grid_counter += 1
            row_counter = -1
            for col in row:
                row_counter += 1
                if col == 1:
                    arcade.draw_texture_rectangle(
                        (100 * grid_counter) + 50, (100 * row_counter) + 50, 100, 100,
                        arcade.load_texture('.\\assets\\diamond.png'))
                    if tick_counter % 5 == 0:
                        pant_projectile = arcade.Sprite(
                            ".\\assets\\pant_projectile.png",
                            center_x=(100 * grid_counter) + 50,
                            center_y=(100 * row_counter) + 50)
                        pant_sprites.append(pant_projectile)
                elif col == 2:
                    arcade.draw_texture_rectangle(
                        (100 * grid_counter) + 50, (100 * row_counter) + 50, 100, 100,
                        arcade.load_texture('.\\assets\\gold.png'))
                    if random.randint(0, 45) == 1:
                        fabric_sprites.append(
                            Fabric((100 * grid_counter) + 50, (100 * row_counter) + 50))
                elif col >= 35:
                    arcade.draw_texture_rectangle(
                        (100 * grid_counter) + 50, (100 * row_counter) + 50, 100, 100,
                        arcade.load_texture('.\\assets\\leather.png'))
                    if tick_counter % 2 == 1:
                        arcade.draw_circle_filled(
                            (100 * grid_counter) + 50, (100 * row_counter) + 80, 5,
                            arcade.color.RED)
                elif col >= 3:
                    arcade.draw_texture_rectangle(
                        (100 * grid_counter) + 50, (100 * row_counter) + 50, 100, 100,
                        arcade.load_texture('.\\assets\\leather.png'))
                    grid[grid_counter][row_counter] += 1
        pant_sprites.move(30, 0)
        pant_sprites.draw()

        if send_fabric_error:
            arcade.draw_text(str(fabric), 50, HEIGHT - 60,
                             color=arcade.color.RED, font_size=30,
                             anchor_x="center")
            send_fabric_error = False
        else:
            arcade.draw_text(str(fabric), 50, HEIGHT - 60,
                             color=arcade.color.BLACK, font_size=30,
                             anchor_x="center")

        # zombies
        zombie_sprites.draw()

        # falling fabric
        fabric_sprites.draw()
    elif current_screen == 3:
        arcade.set_background_color(arcade.color.WHITE)
        arcade.draw_text("Game over!", WIDTH / 2,
                         HEIGHT - 100, arcade.color.BLACK, font_size=30,
                         anchor_x="center")


def setup_grid(color_1, color_2):
    def row(y_val):
        for x in gridGenerator:
            if y_val % 200 == 0:
                if x % 200 == 0:
                    arcade.draw_rectangle_filled(x, y_val, 200, 200, color_1)

                else:
                    arcade.draw_rectangle_filled(x, y_val, 200, 200, color_2)

            else:
                if x % 200 == 0:
                    arcade.draw_rectangle_filled(x + 100, y_val, 200, 200,
                                                 color_1)

                else:
                    arcade.draw_rectangle_filled(x + 100, y_val, 200, 200,
                                                 color_2)

    for y in gridGenerator:
        row(y)


def square_round(number):
    return int(math.floor(number / 100.0))


def board_action(x, y):
    global mouse_select, fabric, cost, grid, send_fabric_error, cost_gold, cost_leather, cost_pant
    round_x = square_round(x)
    round_y = square_round(y)
    if (mouse_select == 1) and (grid[round_x][round_y] == 0):
        if fabric - cost_pant >= 0:
            fabric -= cost_pant
            grid[round_x][round_y] = 1
        else:
            send_fabric_error = True
    elif (mouse_select == 2) and (grid[round_x][round_y] == 0):
        if fabric - cost_gold >= 0:
            fabric -= cost_gold
            grid[round_x][round_y] = 2
        else:
            send_fabric_error = True
    elif (mouse_select == 3) and (grid[round_x][round_y] == 0):
        if fabric - cost_leather >= 0:
            fabric -= cost_leather
            grid[round_x][round_y] = 3
        else:
            send_fabric_error = True

    mouse_select = 0


def on_key_press(key, modifiers):
    global current_screen

    if current_screen == 1:
        if key == arcade.key.ESCAPE:
            current_screen = 0
    elif current_screen == 2:
        if key == arcade.key.ESCAPE:
            current_screen = 0


def on_key_release(key, modifiers):
    pass


def on_mouse_press(x, y, button, modifiers):
    global mouse_select
    global selected
    global current_screen

    # menu screen
    if current_screen == 0:
        if mouse_hover(x, y, instruction_button):
            instruction_button[BTN_IS_CLICKED] = True
            current_screen = 1
        elif mouse_hover(x, y, game_button):
            game_button[BTN_IS_CLICKED] = True
            current_screen = 2

    elif current_screen == 2:
        if mouse_hover(x, y, [100, HEIGHT - 100, 100, 100]):
            if mouse_select == 1:
                mouse_select = 0
            else:
                mouse_select = 1
        elif mouse_hover(x, y, [200, HEIGHT - 100, 100, 100]):
            if mouse_select == 2:
                mouse_select = 0
            else:
                mouse_select = 2
        elif mouse_hover(x, y, [300, HEIGHT - 100, 100, 100]):
            if mouse_select == 3:
                mouse_select = 0
            else:
                mouse_select = 3
        elif mouse_hover(x, y, [0, 0, 1000, 700]):
            board_action(x, y)

        mouse_hidden_sprite.center_x = x
        mouse_hidden_sprite.center_y = y


def mouse_motion(x, y, dx, dy):
    pass


def on_mouse_release(x, y, button, modifiers):
    pass


def mouse_hover(x, y, button) -> bool:
    return x > button[BTN_X] and x < button[BTN_X] + button[BTN_WIDTH]  \
       and y > button[BTN_Y] and y < button[BTN_Y] + button[BTN_HEIGHT]


def draw_instruction_button(instruction_button):
    arcade.draw_xywh_rectangle_filled(instruction_button[BTN_X],
                                      instruction_button[BTN_Y],
                                      instruction_button[BTN_WIDTH],
                                      instruction_button[BTN_HEIGHT],
                                      instruction_button[BTN_COLOR])


def draw_game_button(game_button):
    arcade.draw_xywh_rectangle_filled(game_button[BTN_X],
                                      game_button[BTN_Y],
                                      game_button[BTN_WIDTH],
                                      game_button[BTN_HEIGHT],
                                      game_button[BTN_COLOR])


def draw_instructions(instructions):
    arcade.draw_text("1. Collect fabric to make pants.", 200,
                     600, arcade.color.BLACK, font_size=15)
    arcade.draw_text("2. Plant the pants on the yard.", 200,
                     520, arcade.color.BLACK, font_size=15)
    arcade.draw_text("3. As the zombies keep coming, plant more pants.",
                     200, 440, arcade.color.BLACK, font_size=15)
    arcade.draw_text("4. Repeat step 2 and 3.", 200, 360,
                     arcade.color.BLACK, font_size=15)
    arcade.draw_text("5. Clean it up afterwards.", 200,
                     280, arcade.color.BLACK, font_size=15)


if __name__ == '__main__':
    setup()
