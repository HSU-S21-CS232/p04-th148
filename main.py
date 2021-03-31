import os, sys, random
import pygame as pgy

pgy.init()

SCRN_WIDTH = 1200
SCRN_HEIGTH = 800

game_screen = pgy.display.set_mode((SCRN_WIDTH,SCRN_HEIGTH))
clock = pgy.time.Clock()

# specific colors
black = (0,0,0)
white = (255,255,255)
dark_grey = (50,50,50)
mid_grey = (150,150,150)
lite_grey = (200,200,200)
orange = (255,225,143)
font_size = 24

snowing1 = []
for i in range(40):
    snow1_x = random.randrange(0, SCRN_WIDTH)
    snow1_y = random.randrange(0, SCRN_HEIGTH)
    snowing1.append([snow1_x, snow1_y])

snowing2 = []
for i in range(20):
    snow2_x = random.randrange(0, SCRN_WIDTH)
    snow2_y = random.randrange(0, SCRN_HEIGTH)
    snowing2.append([snow2_x, snow2_y])

pgy.display.set_caption('Behemoth of Drought')

class Hellhound:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.Hellhound_img = pgy.image.load(os.path.join('sprite-files','hellhound.png'))
        self.dead = False

    def draw(self, surface):
        surface.blit(self.Hellhound_img, (self.x, self.y))

    def move(self, direction):
        self.x += direction

class Traitor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.Traitor_img = pgy.image.load(os.path.join('sprite-files','traitor3.png'))
        self.dead = False

    def draw(self, surface):
        surface.blit(self.Traitor_img, (self.x, self.y))

class Foliage:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dead = False
        self.Foliage_img = None

    def draw(self, surface):
        surface.blit(self.Foliage_img, (self.x, self.y))

    def move(self, direction):
        self.x += direction


def main():

    running = False
    game_over = False

    FPS = 60

    text_timer = 0
    dialogue_text = ''

    font = pgy.font.Font(None, font_size)
    snow1_direction = .1
    snow2_direction = -.05

    The_Traitor = Traitor(300, 645)

    level = 0

    Hellhound_positions = []
    Foliage_positions = []

    Hellhound_direction = -2

    Hellhound_quant = 5
    Foliage_quant  = 1

    def game_screen_update(my_text, snow_direct1, snow_direct2):
        game_screen.fill(black)

        text_label = font.render(f'{my_text}', 1, orange)
        game_screen.blit(text_label, (320,500))

        # snow code block vvv

        for i in range(len(snowing1)):
            pgy.draw.circle(game_screen, dark_grey, snowing1[i], 1)
            snowing1[i][1] += 1
            snowing1[i][0] += snow_direct1
            if (snowing1[i][1] % 2) == 0:
                snow_direct1 *= -1

            if snowing1[i][1] > 700:
                snow1_x = random.randrange(0, SCRN_WIDTH)
                snowing1[i][0] = snow1_x

                snow1_y = random.randrange(-100, -10)
                snowing1[i][1] = snow1_y

        for i in range(len(snowing2)):
            pgy.draw.circle(game_screen, mid_grey, snowing2[i], 1)
            snowing2[i][1] += 1

            snowing2[i][0] += snow_direct2
            if (snowing2[i][1] % 2) == 0:
                snow_direct2 *= -1

            if snowing2[i][1] > 700:
                snow2_x = random.randrange(0, SCRN_WIDTH)
                snowing2[i][0] = snow2_x

                snow2_y = random.randrange(-100, -10)
                snowing2[i][1] = snow2_y
        

        pgy.draw.rect(game_screen, lite_grey, (0, 700, 1200, 200))

        The_Traitor.draw(game_screen)

        for hellhound in Hellhound_positions:
            hellhound.draw(game_screen)

        if game_over:
            lose_text = font.render("Your fight has ended. Press C to Continue playing or X to eXit."
            , 1 , white)
            game_screen.blit(lose_text, (SCRN_WIDTH / 2 - lose_text.get_width()/2), 400)


        pgy.display.update()

    while running == False:

        for event in pgy.event.get():
            if event.type == pgy.QUIT:
                pgy.quit()
                sys.exit()

        if text_timer == 50:
            dialogue_text = 'Hello.'

        if text_timer == 150:
            dialogue_text = ''

        if text_timer == 200:
            dialogue_text = 'Press [c] if the color and text match.'

        if text_timer == 350:
            dialogue_text = 'If the color and text do not match, press [x].'

        if text_timer == 500:
            dialogue_text = ''

        text_timer += 1

        game_screen_update(dialogue_text, snow1_direction, snow2_direction)

        if len(Hellhound_positions) < 5:
            level += 1
            Hellhound_quant += 2
            Foliage_quant += 1
            for i in range(Hellhound_quant):
                hellhound = Hellhound(random.randrange(2000, 3000), 645)
                Hellhound_positions.append(hellhound)

        # CONTROLS
        # key_press = pgy.key.get_pressed()
        # if key_press[pgy.K_x]:
        # if key_press[pgy.K_c]:

        for hellhound in Hellhound_positions:
            hellhound.move(Hellhound_direction)

        clock.tick(FPS)

if __name__ == '__main__':
    main()
    pgy.quit()