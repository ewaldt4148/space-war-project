# Imports
import pygame
import random

# Initialize game engine
pygame.init()


# Window
WIDTH = 1000
HEIGHT = 650
SIZE = (WIDTH, HEIGHT)
TITLE = "Bye-Bye Birdie"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

#stages
START = 0
PLAYING = 1
LOSE = 2
WIN = 3
# Timer
clock = pygame.time.Clock()
refresh_rate = 60



# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)


#Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font("assets/fonts/barking_cat.otf", 32)
FONT_XL = pygame.font.Font("assets/fonts/barking_cat.otf", 96)
FONT_S = pygame.font.Font("assets/fonts/score.ttf", 32)

# Images
ship_img = pygame.image.load('assets/images/cat_right.png')
cat_icon = pygame.image.load('assets/images/cat_start_screen_gun.png')
bird_icon = pygame.image.load('assets/images/bird_start.png')
cat_hit1 = pygame.image.load('assets/images/cat_hit1.png')
cat_hit2 = pygame.image.load('assets/images/cat_hit2.png')
cat_hit3 = pygame.image.load('assets/images/cat_hit3.png')
cat_hit4 = pygame.image.load('assets/images/cat_hit4.png')
cat_hit5 = pygame.image.load('assets/images/cat_hit5.png')
laser_img = pygame.image.load('assets/images/bullet.png')
enemy_img = pygame.image.load('assets/images/bird1.png')
enemy_img_1 = pygame.image.load('assets/images/bird2.png')
enemy_img_2 = pygame.image.load('assets/images/bird3.png')
bomb_img = pygame.image.load('assets/images/bird_poop.png')
background = pygame.image.load('assets/images/background.png')
# Sounds
music = pygame.mixer.music.load('assets/sounds/music.wav')
gun = pygame.mixer.Sound('assets/sounds/gun.wav')
# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        self.mask = pygame.mask.from_surface(image)
        self.rect.x = x
        self.rect.y = y

        self.cooldown = 60

        self.speed = 3
        self.shield = 5
        self.direc = 'right'
        
    def move_left(self):
        self.rect.x -= self.speed
        if self.direc == 'right':
            self.image = pygame.transform.flip(self.image,1,0)
        self.direc = 'left'
        
    def move_right(self):
        self.rect.x += self.speed
        if self.direc == 'left':
            self.image = pygame.transform.flip(self.image,1,0)
        self.direc = 'right'
    def shoot(self):
        las = Laser(laser_img)
        las.rect.centerx = self.rect.centerx
        las.rect.centery = self.rect.top

        if self.cooldown == 60:
            lasers.add(las)
            gun.play()
            self.cooldown = 0

    def update(self, bombs):
        if self.cooldown != 60:
            self.cooldown += 1
    

        
        hit_list = pygame.sprite.spritecollide(self, bombs, True)

        for hit in hit_list:
            #OOF.play()
            self.shield -= 1

        if self.shield == 0:
            #EXPLOSION.play()
            self.kill()
        hit_list_mobs = pygame.sprite.spritecollide(self, mobs, True)

        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH 

            
class Laser(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        
        self.speed = 6

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()
    
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.image2 = self.image = pygame.transform.flip(self.image,1,0)
        self.mask = pygame.mask.from_surface(image)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)

    def update(self, lasers, player):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            #EXPLOSION.play()
            player.score += 1
            self.kill()
            stage = WIN

class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        self.mask = pygame.mask.from_surface(image)
        
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()
    

    
class Fleet:

    def __init__(self, mobs):
        self.mobs = mobs
        self.bomb_rate = 60
        self.speed = 5
        self.moving_right = True
        
        
    def move(self):
        reverse = False

        if self.moving_right:
            for m in mobs:
                m.rect.x += self.speed
                if m.rect.right >= WIDTH*2:
                    reverse = True
        else:
            for m in mobs:
                m.rect.x -= self.speed
                if m.rect.left <= -800:
                    reverse = True
        if reverse:
            self.moving_right = not self.moving_right

            for m in mobs:
                m.image, m.image2 = m.image2, m.image
                m.rect.y += 32


    def choose_bomber(self):
        rand = random.randrange(0, self.bomb_rate)
        all_mobs = mobs.sprites()
        
        if len(all_mobs) > 0 and rand == 0:
            return random.choice(all_mobs)
        else:
            return None
    
    def update(self):
        self.move()

        bomber = self.choose_bomber()
        if bomber != None:
            bomber.drop_bomb()

    
#Moving Road
num_lines = 5
lines = []
x = -100
for i in range(num_lines):

    y = 600
    loc = [x, y]
    lines.append(loc)
    x += 200
    
def draw_line(loc):
    x = loc[0] 
    y = loc[1]
    pygame.draw.rect(screen, YELLOW, [x, y, 100, 20])

#Screens
def start():
    global stage
    stage = START
    screen.fill(BLACK)
    title_text = FONT_XL.render("Bye Bye Birdie!", True, WHITE)
    text2 = FONT_MD.render("(Press ENTER to play.)", True, WHITE)
    screen.blit(title_text, [200, 150])
    screen.blit(text2, [300, 300])
    screen.blit(cat_icon, [270, 300])
    screen.blit(bird_icon, [800, 20])
    
def show_stats(player):
    score_text = FONT_S.render(str(player.score), 1, WHITE)
    screen.blit(score_text, [32, 32])

def win():
    screen.fill(BLACK)
    font1 = pygame.font.Font(None, 48)
    text = font1.render("Stage Cleared!", 1, RED)
    screen.blit(text, [300, 200])
    text2 = font1.render("(Press SPACE to continue.)", True, WHITE)
    screen.blit(text2, [210, 500])
# Make game objects
ship = Ship(384, 550, ship_img)
mob1 = Mob(128, 64, enemy_img)
mob2 = Mob(256, 64, enemy_img_1)
mob3 = Mob(384, 64, enemy_img_2)

# Make sprite groups
player = pygame.sprite.Group()
player.add(ship)
player.score = 0

lasers = pygame.sprite.Group()

mobs = pygame.sprite.Group()
mobs.add(mob1, mob2, mob3)

bombs = pygame.sprite.Group()

#Sound
pygame.mixer.music.play(-1)
# Make fleet
fleet = Fleet(mobs)
start()
# Game loop
done = False

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_RETURN:
                    stage = PLAYING
            if stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()
    if stage == PLAYING:
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()
        
    
    # Game logic (Check for collisions, update points, etc.)
    for c in lines:
        c[0] -= 4

        if c[0] < -100:
            c[0] = 1000

    if stage == PLAYING:
        player.update(bombs) 
        lasers.update()
        bombs.update()
        mobs.update(lasers, player)
        fleet.update()
        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)

    if stage == START:
        start()

    if stage == PLAYING:
        screen.fill(BLACK)
        screen.blit(background, (0,0))
        for c in lines:
            draw_line(c)
        lasers.draw(screen)
        bombs.draw(screen)
        player.draw(screen)
        mobs.draw(screen)
        show_stats(player)

    
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
