import sys, random
import pygame as pgy

pgy.init()

scrn_width = 1200
scrn_height = 800

game_screen = pgy.display.set_mode((scrn_width,scrn_height))
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
    snow1_x = random.randrange(0, scrn_width)
    snow1_y = random.randrange(0, scrn_width)
    snowing1.append([snow1_x, snow1_y])

snowing2 = []
for i in range(20):
    snow2_x = random.randrange(0, scrn_width)
    snow2_y = random.randrange(0, scrn_width)
    snowing2.append([snow2_x, snow2_y])

pgy.display.set_caption('Behemoth of Drought')

def main():

    text_timer = 0
    font = pgy.font.Font(None, font_size)

    while True:

        for event in pgy.event.get():
            if event.type == pgy.QUIT:
                pgy.quit()
                sys.exit()

        # CONTROLS
        # mouse_pressed = pgy.key.get_pressed()
        # if mouse_pressed[pgy.K_x]:

        game_screen.fill(black)
        text_timer += 1

        for i in range(len(snowing1)):
            pgy.draw.circle(game_screen, dark_grey, snowing1[i], 1)
            snowing1[i][1] += 1
            if ((snowing1[i][1] % 3) / (i + 1)) >= 7:
                snowing1[i][0] += .1

            if ((snowing1[i][1] % 3) / (i + 1)) < 7:
                snowing1[i][0] -= .1

            if snowing1[i][1] > 700:
                snow1_x = random.randrange(0, scrn_width)
                snowing1[i][0] = snow1_x

                snow1_y = random.randrange(-100, -10)
                snowing1[i][1] = snow1_y

        for i in range(len(snowing2)):
            pgy.draw.circle(game_screen, mid_grey, snowing2[i], 1)
            snowing2[i][1] += 1

            if ((snowing2[i][1] % 3) / (i + 1)) >= 7:
                snowing2[i][0] += .05

            if ((snowing2[i][1] % 3) / (i + 1)) < 7:
                snowing2[i][0] -= .05

            if snowing2[i][1] > 700:
                snow2_x = random.randrange(0, scrn_width)
                snowing2[i][0] = snow2_x

                snow2_y = random.randrange(-100, -10)
                snowing2[i][1] = snow2_y

        text_screen = game_screen.subsurface(scrn_width / 2 - 150,scrn_height / 2,500,128)

        dialogue_string1 = "Hello."
        dialogue_string2 = "If the color of the word matches, press [C]."
        dialogue_string3 = "If the color of the word doesn't match, press [X]."

        dialogue = font.render(dialogue_string1, 0, orange)
        dialogue2 = font.render(dialogue_string2, 0, orange)
        dialogue3 = font.render(dialogue_string3, 0, orange)
        text_screen.blit(dialogue, (70, 0))
        if text_timer < 50:
            text_screen.fill(black)

        if (text_timer >= 200) & (text_timer < 250):
            text_screen.fill(black)

        if (text_timer >= 250) & (text_timer < 900):
            text_screen.fill(black)
            text_screen.blit(dialogue2, (50, 0))

        if (text_timer >= 500) & (text_timer < 900):
            text_screen.blit(dialogue3, (60, 40))

        if (text_timer >= 900):
            text_screen.fill(black)

        pgy.draw.rect(game_screen, lite_grey, (0, 700, 1200, 200))

        pgy.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
    pgy.quit()