from arcade import *

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
button1 = [200, 200, 300, 50, False, color.BLUE, color.RED]
button2 = [200, 140, 100, 30, False, color.BLUE, color.RED]

# Menu: 0
# Instructions: 1
# Game: 2
current_screen = 0

instruction_button = [(WIDTH - 190) / 2, HEIGHT - 560, 190, 50, color.GRAY, color.RED]
game_button = [(WIDTH - 190) / 2, HEIGHT - 710, 190, 50, color.BLACK, color.BLUE]

button_1 = [WIDTH - 1000, HEIGHT - 100, 100, 100, False, color.BLUE, color.RED]

# grid
grid_col_1 = color.GREEN
grid_col_2 = color.DARK_GREEN

gridGenerator = [100 * k for k in range(0, 11)]

mousePos = [0, 0]
piecePos = [50, 50]
selected = -1

# zombie moving
zombie_x_positions = [800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800]
zombie_y_positions = [130, 250, 450, 230, 13, 100, 52, 340, 259, 636, 547]

class Zombie:


    def __init__(self, row, speed='2.5', color=color.BLUE, health=10):
        self.y = [0, 100, 200, 300, 400, 500, 600, 700][row]
        self.speed = speed
        self.color = color
        self.health = health
        self.x = 800

    def walk(self):
        self.x -= self.speed
        if self.x <= 0:
            pass # TODO: Handle game over

    def hit(self, damage=1):
        self.health -= damage
        if self.health <= 0:
            pass # TODO: Handle zombie death

def setup():
    open_window(WIDTH, HEIGHT, "My Arcade Game")
    set_background_color(color.WHITE)
    schedule(update, 1 / 60)
    window = get_window()
    window.on_draw = on_draw
    window.on_key_press = on_key_press
    window.on_key_release = on_key_release
    window.on_mouse_press = on_mouse_press
    window.on_mouse_release = on_mouse_release
    window.on_mouse_motion = mouse_motion

    run()


def update(delta_time):
    setup_grid(grid_col_1, grid_col_2)
    draw_piece()

    print("Mouse: " + "(" + str(mousePos[0]) + ", " + str(
        mousePos[1]) + ")" + " | " + "Selected: " + str(
        selected) + " | " + "Piece: " + "(" + str(piecePos[0]) + ", " + str(
        piecePos[1]) + ")")
    for index in range(len(zombie_x_positions)):
        zombie_x_positions[index] -= 2.5


def on_draw():

    start_render()

    # menu
    if current_screen == 0:
        set_background_color(color.GREEN)
        draw_text("Pants VS Zombies", WIDTH / 2, HEIGHT
                         - 100, color.BLACK, font_size=30,
                         anchor_x="center")
        draw_instruction_button(instruction_button)
        draw_game_button(game_button)
        draw_text("Instructions", WIDTH / 2, HEIGHT - 550, color.BLACK, font_size=30,
                         anchor_x="center")
        draw_text("Play", WIDTH / 2, HEIGHT - 700, color.BLACK, font_size=30, anchor_x="center")

    # instructions
    elif current_screen == 1:
        set_background_color(color.GRAY)
        draw_text("Instructions", WIDTH / 2, HEIGHT - 100, color.BLACK, font_size=30,
                         anchor_x="center")
        draw_instructions("instructions")
        draw_text("Esc to go to Menu", WIDTH - 1000, HEIGHT - 700, color.BLACK, font_size=30,
                         anchor_x="center")
        # game

    elif current_screen == 2:
        # grid
        setup_grid(grid_col_1, grid_col_2)
        draw_piece()

        # zombies
        for c, d in zip(zombie_x_positions, zombie_y_positions):
            draw_circle_filled(c, d, 30, color.BLUE)


def setup_grid(color_1, color_2):
    def row(y_val):
        for x in gridGenerator:
            if y_val % 200 == 0:
                if x % 200 == 0:
                    draw_rectangle_filled(x, y_val, 200, 200, color_1)

                else:
                    draw_rectangle_filled(x, y_val, 200, 200, color_2)

            else:
                if x % 200 == 0:
                    draw_rectangle_filled(x + 100, y_val, 200, 200,
                                          color_1)

                else:
                    draw_rectangle_filled(x + 100, y_val, 200, 200,
                                          color_2)

    for y in gridGenerator:
        row(y)


def custom_round(x, base=50):
    return base * round(x / base)


def draw_piece():
    if piecePos[0] % 100 != 0:
        piecePos[0] = custom_round(piecePos[0])

    elif piecePos[1] % 100 != 0:
        piecePos[1] = custom_round(piecePos[1])

    elif (piecePos[0] % 100 == 0) or (piecePos[1] % 100 == 0):
        draw_circle_filled(piecePos[0], piecePos[1], 45, color.BLACK)


def on_key_press(key, modifiers):
    global current_screen

    if current_screen == 1:
        if key == key.ESCAPE:
            current_screen = 0
    elif current_screen == 2:
        if key == key.ESCAPE:
            current_screen = 0


def on_key_release(key, modifiers):
    pass


def on_mouse_press(x, y, button, modifiers):
    global selected, x_req, y_req

    x_req = piecePos[0] - 50 <= mousePos[0] <= piecePos[0] + 50
    y_req = piecePos[1] - 50 <= mousePos[1] <= piecePos[1] + 50

    print(f"Click at ({x}, {y})")
    global current_screen

    if mouse_hover(x, y, button1):
        button1[BTN_IS_CLICKED] = True
    if mouse_hover(x, y, button2):
        button2[BTN_IS_CLICKED] = True

    # menu screen
    if mouse_hover(x, y, instruction_button):
        instruction_button[BTN_IS_CLICKED] = True
        current_screen = 1

    elif mouse_hover(x, y, game_button):
        game_button[BTN_IS_CLICKED] = True
        current_screen = 2


def mouse_motion(x, y, dx, dy):
    mousePos[0] = x
    mousePos[1] = y

    if selected == 1 and x_req and y_req:
        piecePos[0] = mousePos[0]
        piecePos[1] = mousePos[1]


def on_mouse_release(x, y, button, modifiers):
    button1[BTN_IS_CLICKED] = False
    button2[BTN_IS_CLICKED] = False


def mouse_hover(x, y, button) -> bool:
    return x > button[BTN_X] and x < button[BTN_X] + button[BTN_WIDTH] and y > button[BTN_Y] \
        and y < button[BTN_Y] + button[BTN_HEIGHT]

def draw_button(button):
    # Select the appropriate color to draw with
    if button1[BTN_IS_CLICKED]:
        color = button1[BTN_CLICKED_COLOR]
    else:
        color = button1[BTN_COLOR]

    if button2[BTN_IS_CLICKED]:
        color = button2[BTN_CLICKED_COLOR]
    else:
        color = button2[BTN_COLOR]
        # Draw button1
    draw_xywh_rectangle_filled(button[BTN_X],
                                      button[BTN_Y],
                                      button[BTN_WIDTH],
                                      button[BTN_HEIGHT],
                                      color)


def draw_button_1(button_1):
    if button_1[BTN_IS_CLICKED]:
        color = [BTN_CLICKED_COLOR]
    else:
        color = [BTN_COLOR]
    draw_xywh_rectangle_filled(button_1[BTN_X],
                                      button_1[BTN_Y],
                                      button_1[BTN_WIDTH],
                                      button_1[BTN_HEIGHT],
                                      button_1[BTN_COLOR])


def draw_instruction_button(instruction_button):
    draw_xywh_rectangle_filled(instruction_button[BTN_X],
                                      instruction_button[BTN_Y],
                                      instruction_button[BTN_WIDTH],
                                      instruction_button[BTN_HEIGHT],
                                      instruction_button[BTN_COLOR])


def draw_game_button(game_button):
    draw_xywh_rectangle_filled(game_button[BTN_X],
                                      game_button[BTN_Y],
                                      game_button[BTN_WIDTH],
                                      game_button[BTN_HEIGHT],
                                      game_button[BTN_COLOR])


def draw_instructions(instructions):
    draw_text("1. Collect fabric to make plants.", 200, 600, color.BLACK, font_size=15)
    draw_text("2. Plant the pants on the yard.", 200, 520, color.BLACK, font_size=15)
    draw_text("3. As the zombies keep coming, plant more pants.", 200, 440, color.BLACK, font_size=15)
    draw_text("4. Repeat step 2 and 3.", 200, 360, color.BLACK, font_size=15)
    draw_text("5. Clean it up afterwards.", 200, 280, color.BLACK, font_size=15)


if __name__ == '__main__':
    setup()
