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
red = (203,10,10)
blue = (168,168,255)
green = (10,203,10)
yellow = (213,213,0)
cyan = (0,255,255)
purple = (203,10,203)
font_size = 24
L_font_size = 60

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

hellhound_image = pgy.image.load(os.path.join('sprite-files','hellhound.png'))
pgy.display.set_icon(hellhound_image)

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

class Hellhound:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.Hellhound_img = hellhound_image
        self.dead = False
        self.mask = pgy.mask.from_surface(self.Hellhound_img)

    def draw(self, surface):
        if self.dead == False:
            surface.blit(self.Hellhound_img, (self.x, self.y))

    def move(self, direction):
        self.x += direction

    def collision(self, obj):
        return collide(obj, self)

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

SWING_IMG = pgy.image.load(os.path.join('sprite-files','flameburst.png'))

class Destructive_Swing:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.large = False
        self.Swing_img = SWING_IMG
        self.mask = pgy.mask.from_surface(self.Swing_img)
        self.dead = False

    def draw(self, surface):
        if self.dead == False:
            surface.blit(self.Swing_img, (self.x, self.y))

    def collision(self, obj):
        obj.dead = True
        self.dead = True
        return collide(obj, self)

def main():

    not_running = False
    game_over = False

    FPS = 60

    text_timer = 0
    dialogue_text = ''

    font = pgy.font.Font(None, font_size)
    L_font = pgy.font.Font(None, L_font_size)
    snow1_direction = .1
    snow2_direction = -.05

    The_Traitor = Traitor(300, 645)
    Traitor_attack = Destructive_Swing(330,800)

    level = 0

    Hellhound_positions = []
    Foliage_positions = []
    flame_timer = 0
    color_timer = 0
    attack_cooldown = 0

    Hellhound_direction = -2

    Hellhound_quant = 5
    Foliage_quant  = 1

    game_over_timer = 160

    def color_text_generator(test_text, text_color):
        color_text = L_font.render(f'{test_text}'
        , 1 , text_color)
        game_screen.blit(color_text, (400, 400))

    def one_thru_six():
        random_int = random.randint(1,6)
        return random_int

    def text_randomizer(randomized_int):
        random_int = randomized_int
        if random_int == 1:
            new_test_text = 'Red'
        elif random_int == 2:
            new_test_text = 'Blue'
        elif random_int == 3:
            new_test_text = 'Green'
        elif random_int == 4:
            new_test_text = 'Yellow'
        elif random_int == 5:
            new_test_text = 'Cyan'
        elif random_int == 6:
            new_test_text = 'Purple'
        return new_test_text

    def color_randomizer(randomized_int):
        random_int2 = randomized_int
        if random_int2 == 1:
            new_test_color = red
        elif random_int2 == 2:
            new_test_color = blue
        elif random_int2 == 3:
            new_test_color = green
        elif random_int2 == 4:
            new_test_color = yellow
        elif random_int2 == 5:
            new_test_color = cyan
        elif random_int2 == 6:
            new_test_color = purple
        return new_test_color

    def game_screen_update(my_text, snow_direct1, snow_direct2, random_int1, random_int2):
        game_screen.fill(black)

        text_label = font.render(f'{my_text}', 1, orange)
        game_screen.blit(text_label, (320,500))

        color_text_generator(text_randomizer(random_int1), color_randomizer(random_int2))

        if flame_timer == 0:
            Traitor_attack.x = 330
            Traitor_attack.y = 800


        if flame_timer > 0:
            if Traitor_attack.x > 344:
                Traitor_attack.x = 330
            Traitor_attack.y = 650
            Traitor_attack.draw(game_screen)

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
            lose_text = font.render("Your fight has ended. Prepare to exit..."
            , 1 , white)
            game_screen.blit(lose_text, (300, 600))


        pgy.display.update()

    while not not_running:

        for event in pgy.event.get():
            if event.type == pgy.QUIT:
                pgy.quit()
                sys.exit()

        if game_over_timer < 0:
            pgy.quit()
            sys.exit()

        if game_over:
            game_over_timer -= 1

        color_timer += 1

        if attack_cooldown > 0:
            attack_cooldown -= 1

        if color_timer < 60:
            rand_int1 = 1
            rand_int2 = 1
            do_match = True

        if (color_timer % 60) == 0:
            do_match = True
            rand_int0 = random.randint(1,2)
            if rand_int0 == 1:
                rand_int1 = one_thru_six()
                rand_int2 = one_thru_six()
                if rand_int1 == rand_int2:
                    do_match = True
                elif rand_int1 != rand_int2:
                    do_match = False
            elif rand_int0 == 2:
                matching_int = one_thru_six()
                rand_int1 = matching_int
                rand_int2 = matching_int
                do_match = True


        if flame_timer > 0:
            flame_timer -= 1

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

        if text_timer < 500:
            text_timer += 1

        # CONTROLS
        key_press = pgy.key.get_pressed()
        if key_press[pgy.K_x]:
            if attack_cooldown == 0:
                if not do_match:
                    flame_timer = 14
                    attack_cooldown += 36
                elif do_match:
                    Hellhound_direction -= 1
                    attack_cooldown += 22
        if key_press[pgy.K_c]:
            if attack_cooldown == 0:
                if do_match:
                    flame_timer = 14
                    attack_cooldown += 36
                elif not do_match:
                    Hellhound_direction -= 1
                    attack_cooldown += 22

        game_screen_update(dialogue_text, snow1_direction, snow2_direction, rand_int1, rand_int2)

        if len(Hellhound_positions) < 5:
            level += 1
            Hellhound_quant += 2
            Foliage_quant += 1
            for i in range(Hellhound_quant):
                hellhound = Hellhound(random.randrange(2000, 2600), 645)
                Hellhound_positions.append(hellhound)

        Traitor_attack.x += 1

        for hellhound in Hellhound_positions[:]:
            hellhound.move(Hellhound_direction)
            if hellhound.x < 340:
                game_over = True
            if hellhound.collision(Traitor_attack):
                Hellhound_positions.remove(hellhound)

        clock.tick(FPS)

if __name__ == '__main__':
    main()
    pgy.quit()