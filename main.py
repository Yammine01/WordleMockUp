import pygame
import os
from os import system
from random import randint

CURRENT_DIR = os.path.dirname(__file__)
os.chdir(CURRENT_DIR)

system("cls")

pygame.init()

scale = 75

display_x, display_y = 16 * scale, 9 * scale

background_color = [0, 0, 0]
grey = (38, 38, 38)
green = (50, 150, 75)
yellow = (255, 200, 50)

background = pygame.display.set_mode((display_x,display_y))
pygame.display.set_icon(pygame.image.load("icon.png"))

cell_size = scale * 4 // 3
letter_size = int(cell_size // 1.5)


# ===================================================== Classes ===================================================== #

class Grid:

    def __init__(self, x, y, i, j, thickness, cell_size, color = "white"):
        
        self.x, self.y, self.i, self.j, self.thickness, self.cell_size, self.color = x, y, i, j, thickness, cell_size, color
        self.draw_x, self.draw_y = self.x - self.i * self.cell_size // 2, self.y - self.j * self.cell_size // 2

        self.coordinates = []
        for i in range(self.j):

            row = i * self.cell_size + self.thickness

            for j in range(self.i):

                self.coordinates.append((self.draw_x + j * self.cell_size + self.thickness, self.draw_y + row))


    def draw(self):

        for i in range(self.i + 1):

            draw_rect(self.draw_x + i * self.cell_size, self.draw_y, self.thickness, self.j * self.cell_size + self.thickness, self.color)

        for j in range(self.j + 1):

            draw_rect(self.draw_x, self.draw_y + j * self.cell_size, self.i * self.cell_size + self.thickness, self.thickness, self.color)


    def fill_cell(self, number, color):

        x, y = self.coordinates[number][0], self.coordinates[number][1]

        draw_rect(x, y , self.cell_size - self.thickness, self.cell_size - self.thickness, color)


    def place_letter(self, number, letter, bg_color = background_color):

        x, y = self.coordinates[number][0], self.coordinates[number][1]
        display_text(x + self.cell_size // 2 - self.thickness // 2, y + self.cell_size // 2 - self.thickness // 2, letter, int(self.cell_size // 1.5), "white", bg_color)

# ==================================================== Functions ==================================================== #

def draw_rect(x, y, width, height, color):

    pygame.draw.rect(background, color, (x, y, width, height))


def display_text(x, y, text, size, color, bg_color, center = True):

    if center:
        
        font = pygame.font.Font("freesansbold.ttf", size)
        text_render = font.render(text, True, color, bg_color)
        background.blit(text_render, text_render.get_rect(center = (x, y)))\
    
    else:
        font = pygame.font.Font("freesansbold.ttf", size)
        background.blit(font.render(text, True, color, bg_color), [x, y])


def place_button(x, y, text, text_size, text_color, color, border_thickness, border_color):

    border_width = len(text) * text_size // 1.8
    border_height = text_size * 1.5

    draw_rect(x - border_width // 2, y - border_height // 2, border_width + border_thickness, border_height + border_thickness, border_color)
    draw_rect(x - border_width // 2 + border_thickness, y - border_height // 2 + border_thickness, border_width - border_thickness, border_height - border_thickness, color)

    display_text(x, y, text, text_size, text_color, color)


def is_valid(key_name):

    if not key_name.isalpha() or len(key_name) > 1: return False
    return True


def receivable():

    if len(letter_array) == 25 or len(input_array) == 5: return False
    return True


def get_input():

    key = pygame.key.name(event.key).upper()

    if not is_valid(key) or not receivable(): return

    letter_array.append(key)
    input_array.append(key)

    map_letters()


def map_letters():

    for number in range(len(input_array)):

        main_grid.place_letter(5 * (input_amount) + number, input_array[number])


def generate_word():

    return words_array[randint(0, len(words_array) - 1)]


def display_message():

    pass


def color_line():

    for i in range(5):

        if input_array[i] == word[i]:

            main_grid.fill_cell(5 * input_amount + i, green)
            main_grid.place_letter(5 * input_amount + i, input_array[i], green)
        
        elif input_array[i] in word:

            main_grid.fill_cell(5 * input_amount + i, yellow)
            main_grid.place_letter(5 * input_amount + i, input_array[i], yellow)
        
        else:

            main_grid.fill_cell(5 * input_amount + i, grey)
            main_grid.place_letter(5 * input_amount + i, input_array[i], grey)


def win_event():

    hide_tutorial()

    display_text(display_y + (display_x - display_y) // 2, scale // 1.5, "YOU WON!", letter_size // 2, "white", background_color)

    line_spacing = 1.2

    end = "tries"
    if input_amount == 0:
        end = "try"

    display_text(display_y + scale // 4, scale * line_spacing, f"You guessed the word in {input_amount + 1} {end}!", int(letter_size // 3.5), "white", background_color, False)


def lose_event():

    hide_tutorial()

    display_text(display_y + (display_x - display_y) // 2, scale // 1.5, "YOU LOST!", letter_size // 2, "white", background_color)

    line_spacing = 1.2

    display_text(display_y + scale // 4, scale * line_spacing, f"The word was \"{word.lower()}\".", int(letter_size // 3.5), "white", background_color, False)


def draw_seperater():

    draw_rect(display_y - 2, 0, 5, display_y, grey)


def place_tutorial_button():

    background.blit(tutorial_icon, (display_y + 12, 10))


def show_keybinds():

    draw_rect(display_y, display_y / 2 + 2, display_x - display_y, 5, grey)

    display_text(display_y + (display_x - display_y) // 2, scale * 5, "STATISTICS", letter_size // 2, "white", background_color)


def show_tutorial():

    global tutorial_in_view

    tutorial_in_view = True

    reset_right_side()

    display_text(display_y + (display_x - display_y) // 2, scale // 1.5, "HOW TO PLAY", letter_size // 2, "white", background_color)

    line_spacing = 1.2
    for sentence in sentences_section1:

        if not sentence.endswith((".", ":", "!")):
            display_text(display_y + scale // 4, scale * line_spacing, sentence, int(letter_size // 3.5), "white", background_color, False)
            line_spacing += .3

        else:
            display_text(display_y + scale // 4, scale * line_spacing, sentence, int(letter_size // 3.5), "white", background_color, False)
            line_spacing += .5

    tutorial_grid = Grid(display_y + scale // 4 + cell_size * .75 * 2.5, scale * line_spacing + cell_size * .75 // 2, 5, 1, 2, cell_size * .75)
    tutorial_grid.draw()

    tutorial_grid.fill_cell(0, green)
    tutorial_grid.fill_cell(1, grey)
    tutorial_grid.fill_cell(2, grey)
    tutorial_grid.fill_cell(3, yellow)
    tutorial_grid.fill_cell(4, grey)
    tutorial_grid.place_letter(0, "O", green)
    tutorial_grid.place_letter(1, "T", grey)
    tutorial_grid.place_letter(2, "H", grey)
    tutorial_grid.place_letter(3, "E", yellow)
    tutorial_grid.place_letter(4, "R", grey)

    line_spacing += tutorial_grid.cell_size // scale + .5

    for sentence in sentences_section2:

        if not sentence.endswith((".", ":", "!")):
            display_text(display_y + scale // 4, scale * line_spacing, sentence, int(letter_size // 3.5), "white", background_color, False)
            line_spacing += .3

        else:
            display_text(display_y + scale // 4, scale * line_spacing, sentence, int(letter_size // 3.5), "white", background_color, False)
            line_spacing += .5

    line_spacing += .5


def reset_right_side():

    draw_rect(display_y + 3, 0, display_x - display_y, display_y, background_color)


def hide_tutorial():

    global tutorial_in_view

    tutorial_in_view = False

    reset_right_side()
    place_tutorial_button()
    show_keybinds()


def hovering_over_tutorial_button():

    x, y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]

    if x > display_y + 12 and x < display_y + 38 and y > 10 and y < 36: return True

    return False


def reset_main_grid():

    for number in range(25):

        main_grid.fill_cell(number, background_color)


def restart_game():

    global input_amount
    global word

    word = generate_word()

    letter_array.clear()
    input_array.clear()
    input_amount = 0

    reset_main_grid()

    show_tutorial()

# ===================================================== Keybinds ==================================================== #

def escape_event():

    global close_window

    if len(letter_array) != 0:
        restart_game()
    else:
        close_window = True


def enter_event():

    global input_amount

    if len(input_array) != 5: return

    if "".join(input_array) not in words_array:
        display_message()
        return
    
    color_line()

    if "".join(input_array) == word:
        win_event()
        return

    elif input_amount == 4:
        lose_event()
    
    input_amount += 1
    input_array.clear()


def backspace_event():

    if len(input_array) > 0 and "".join(input_array) != word and input_amount != 5:

        input_array.pop()
        letter_array.pop()
        
        main_grid.fill_cell(5 * input_amount + len(input_array), background_color)

# ==================================================== Characters =================================================== #

letter_array = []
input_array = []
input_amount = 0

with open("words.txt", "r") as words_file:

    words_array = [word[:-1] for word in words_file.readlines()]

word = generate_word()

tutorial_in_view = True

# ==================================================== Instances ==================================================== #

main_grid = Grid(display_y // 2, display_y //2, 5, 5, 2, cell_size)

tutorial_icon = pygame.image.load("question_mark.png")

sentences_section1 = ["Guess the word in five tries.", "Each guess must be a valid five-letter word.", "Hit the enter button to submit.", "After each guess, the color of tiles will change in ", "the following manner:"]
sentences_section2 = ["The letter O is in the correct spot.", "The letter E is in the word but not the correct spot.", "The rest of the letters are not not in the word.", "Good Luck!"]

# ==================================================== Main Game ==================================================== #

close_window = False
background.fill(background_color)

main_grid.draw()
draw_seperater()
show_tutorial()

while not close_window:

    PING = 50
    pygame.display.set_caption("Wordle Guess The Word")
    pygame.time.delay(PING)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            close_window = True

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_ESCAPE:
                escape_event()

            if event.key == pygame.K_RETURN:
                enter_event()

            if event.key == pygame.K_BACKSPACE:
                backspace_event()

            get_input()


    if hovering_over_tutorial_button() and pygame.mouse.get_pressed()[0]:

        if not tutorial_in_view:
            show_tutorial()


    pygame.display.update()