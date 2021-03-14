"""
FILLER

X basic python setup
X create Tile class (color, owned, x, y)
X plan the design/numbers of everything
X make a function that can generate a grid of tiles of random color (6 colors)
    X but! all adjacent colors must be unique...
X a separate class for the buttons for choosing color...
X draw all the ColorButtons... how will they function? what happens when you click on it?
X should there be a player class ? (num tiles, current color, which tiles are owned?
X user instance and ai instance (ig since it's not learning it would tech. be just cpu)
X tiles that are the same color and are touching the tiles owned get changed to owned = True
    X after you change the color, change that color_button back to selectable = True
X make algorithm for cpu... test all colors and see which one would give the most...
X fix bug: players are able add tiles from the other side of the board (10-->1 ugh) (YES I FIXED IT)
X fix bug: cpu adds all the colors instead of just one (reset doesn't work)
X check who wins at the end... when all tiles are owned...
X draw the text: FILLER, score
IT ONLY TOOK 2 DAYS TO IMPLEMENT ALL OF THIS !! ^

extra/ UI/UX:
X if the color button is not selectable it's smaller
- make cursor go to hand when it's hovering over a selectable color button
- tiles that you own flash a dif color when it's your turn
- there's a delay before the computer moves / make an animation for adding the blocks
- "you win" end screen (i like the confetti... maybe i can import it or something? that'd be cool if i could use it
across all my games!)
- "you lose" end screen
- add sound effects
- add music
- add a settings where you can toggle music/sfx (top right corner)
- add a shop (top right) where you can get different color schemes!! (free, for now)

or maybe, the time taken for the animation (switch from each color) is the delay. again, the color change must only
effect the tiles that are owned my that player (separate color variable)

pulsing color
X figure out how to universally lighten the color (just try +50 ig)
- find relationship between og and light color, experiment with math.sin and pygame.time.ticks()
- it only happens when it's users turn

"""

import pygame
import sys
import random
import math

pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 450
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Filler!")

# GAME VARIABLES
colors = [[188, 237, 102], [102, 224, 237], [102, 140, 237], [131, 102, 237], [206, 102, 237], [255, 138, 183]]
col_leng = 10
row_leng = 18
size = 25
turn = "user"


"""CLASSES"""


class Tile:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, size, size)  # w, h
        self.color = color
        self.display_color = color.copy()
        self.owned = False

    def draw(self):
        pygame.draw.rect(screen, self.display_color, self.rect)
        pass

    """
    ISSUE: when i change self.color it changes it's official color, even the color buttons
    fix: make another variable that's a copy of the og color. when turn = user, rect's color will be the copy,
    and otherwise (i still need to make a delay before cpu's move) the og color will be the rect's color
    """
    def blink(self):
        print("blink he")
        num = math.sin(pygame.time.get_ticks()/0.5)
        og_color = self.color.copy()
        for i in range(3):
            self.color[i] = og_color[i] + 50*num
            if self.color[i] > 255:
                self.color[i] = 255
            if self.color[i] < 0:
                self.color[i] = 0

    # blend from previous color to new color
    def transition(self, new_color):
        while self.display_color != self.color:
            for i in range(3):
                if new_color[i] > self.display_color[i]:
                    factor = 1
                elif new_color[i] < self.display_color[i]:
                    factor = -1
                else:
                    factor = 0
                self.display_color[i] += factor
            self.draw()


class ColorButton:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 35, 35)
        self.color = color
        self.selectable = True

    def draw(self):
        if self.selectable:
            self.rect.update(self.x, self.y, 35, 35)
        else:
            self.rect.update(self.x+7.5, self.y+7.5, 20, 20)
        pygame.draw.rect(screen, self.color, self.rect)

    def check_click(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.selectable:
            if self.rect.left < mouse_x < self.rect.right:
                if self.rect.top < mouse_y < self.rect.bottom:
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)   # ahh
                    return self


class Player:
    def __init__(self, start_index):
        self.origin = start_index
        self.tiles_owned = 1
        self.color = tiles[start_index].color
        # there is a small chance that both players will start with the same color... o well idc
        self.tiles = [tiles[start_index]]
        tiles[start_index].owned = True

        # update color button selectability
        for btn in color_btns:
            if self.color == btn.color:
                btn.selectable = False

    def add_tile(self, i):
        tiles[i].owned = True
        self.tiles.append(tiles[i])
        self.tiles_owned += 1

    def switch_color(self, color):
        self.color = color
        for tile in self.tiles:
            tile.color = color
            tile.transition(color)

    def count_tiles(self):
        i = 0
        for row in range(col_leng):
            for col in range(row_leng):
                if (not tiles[i] in self.tiles) and tiles[i].color == self.color:
                    # top edge
                    if row == 0:
                        if tiles[i+row_leng] in self.tiles:
                            self.add_tile(i)
                            i += 1  # because the continue skips over the i+=1 that's at the bottom
                            continue
                    else:
                        if tiles[i-row_leng] in self.tiles:
                            self.add_tile(i)
                            i += 1
                            continue

                    # bottom edge
                    if row+1 == col_leng:
                        if tiles[i - row_leng] in self.tiles:
                            self.add_tile(i)
                            i += 1
                            continue
                    else:
                        if tiles[i + row_leng] in self.tiles:
                            self.add_tile(i)
                            i += 1
                            continue

                    # left edge
                    if col == 0:
                        if tiles[i + 1] in self.tiles:
                            self.add_tile(i)
                            i += 1
                            continue
                    else:
                        if tiles[i - 1] in self.tiles:
                            self.add_tile(i)
                            i += 1
                            continue

                    # right edge
                    if col+1 == row_leng:
                        if tiles[i - 1] in self.tiles:
                            self.add_tile(i)
                            i += 1
                            continue
                    else:
                        if tiles[i + 1] in self.tiles:
                            self.add_tile(i)
                            i += 1
                            continue

                i += 1

    def update(self, color_btn):
        self.switch_color(color_btn.color)

        # makes the old color selectable again
        for color_btn in color_btns:
            if user.color == color_btn.color or cpu.color == color_btn.color:
                color_btn.selectable = False
            else:
                color_btn.selectable = True
        self.count_tiles()
        # update score somehow

    def blink_tiles(self):
        for tile in self.tiles:
            tile.blink()


class Confetti:
    def __init__(self, colors, amount):
        self.sprinkles = []
        for i in range(50):
            self.sprinkles.append(Confetti.Sprinkle(colors))

    def draw(self):
        for sprinkle in self.sprinkles:
            sprinkle.draw()

    class Sprinkle:
        def __init__(self, colors):
            self.x = random.randint(0, SCREEN_WIDTH)
            self.y = random.randint(-200, 0)
            self.size = random.randint(15, 70) / 8
            self.speed = self.size / 3  # adjust this... small size --> slow speed
            self.color = random.choice(colors)

        def draw(self):
            pygame.draw.rect(screen, self.color, (self.x, self.y, int(self.size), int(self.size * 2.5)))
            self.y += self.speed


"""FUNCTIONS"""


def draw_tiles():
    for tile in tiles:
        tile.draw()


# cpu alg
def choose_color():
    # record initial list of tiles + length
    init_list = cpu.tiles.copy()
    init_num = cpu.tiles_owned
    options = []
    for btn in color_btns:
        if btn.selectable:
            # pass count_tiles() on a color and record the difference between initial length and new length
            cpu.switch_color(btn.color)
            cpu.count_tiles()
            options += [[cpu.tiles_owned - init_num]]
            options[-1] += [btn]

            # reset
            for tile in cpu.tiles:
                if tile not in init_list:
                    tile.owned = False
            cpu.tiles = init_list.copy()
            cpu.tiles_owned = len(init_list)

    # run update() on the color with the highest
    # if you specify which index to sort it by, it won't try to look at the other indexes to break ties
    options.sort(key=lambda x: x[0])
    return options[-1][1]


# returns True if user won
# an issue: it returns false/none if the game is incomplete (and triggers the "you lose" text down below)
# i can also just separate "game is on" and "who won" into 2 separate functions
def board_filled():
    if user.tiles_owned + cpu.tiles_owned == row_leng*col_leng:
        return True
    return False


def user_won():
    if user.tiles_owned > cpu.tiles_owned:
        return True
    return False


# makes a grid of tiles
tiles = []
unique_colors = colors.copy()
for row in range(col_leng):
    for col in range(row_leng):
        unique_colors = colors.copy()
        # remove the color before
        if col > 0:
            unique_colors.remove(tiles[-1].color)

        # remove the color in the row above
        if row > 0:
            # have to check if it's already been removed or not
            if tiles[row * row_leng + col - row_leng].color in unique_colors:
                unique_colors.remove(tiles[row * row_leng + col - row_leng].color)

        color = random.choice(unique_colors)
        tiles.append(Tile(125+col*size, 80+row*size, color))


# makes color buttons
color_btns = []
for i, color in enumerate(colors):
    color_btns.append(ColorButton(127+i*81, 372.5, color))


# makes user and cpu
user = Player(len(tiles)-row_leng)  # bottom left
cpu = Player(row_leng-1)


# text
font = pygame.font.SysFont("century gothic", 40, bold=True)
title = font.render("F   I   L   L   E   R", True, (255, 255, 255))
title_rect = title.get_rect(center=(350, 45))


# confetti
confetti = Confetti(colors, 100)


# game loop
while True:
    # pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND) # i'll deal with this later

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if turn == "user":
                for btn in color_btns:
                    color_btn = btn.check_click()
                    if color_btn:
                        user.update(color_btn)
                        turn = "cpu"

    if turn == "cpu":
        # cpu.blink_tiles()
        """
        ISSUE: I need to create a delay but I don't know hwo to have the blink andt he delay at the same time...
        """
        cpu.update(choose_color())
        turn = "user"



    # visuals
    screen.fill((210, 210, 210))

    # text
    screen.blit(title, title_rect)

    user_score = font.render(str(user.tiles_owned), True, (255, 255, 255))
    user_score_rect = user_score.get_rect(center=(62.5, 205))
    cpu_score = font.render(str(cpu.tiles_owned), True, (255, 255, 255))
    cpu_score_rect = cpu_score.get_rect(center=(637.5, 205))
    screen.blit(user_score, user_score_rect)
    screen.blit(cpu_score, cpu_score_rect)

    draw_tiles()
    for btn in color_btns:
        btn.draw()

        # check if someone has won the game
    if board_filled():
        if user_won():
            print("you won!")
            confetti.draw()
            # do some sort of win screen
        else:
            print("you lost!")
            # do some sort of lose screen
    # let the user reset?
    
    # check if someone has won the game
    if board_filled():
        if user_won():
            print("you won!")
            confetti.draw()
            # do some sort of win screen
        else:
            print("you lost!")
            # do some sort of lose screen
    # let the user reset?

    clock.tick(40)
    pygame.display.update()
