# Imports
import pygame
import random

# Initialize game engine
pygame.init()


# Window
WIDTH = 1000
HEIGHT = 650
SIZE = (WIDTH, HEIGHT)
TITLE = "Space War"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

#stages
START = 0
PLAYING = 1
LOSE = 2
WIN = 3
WIN_GAME = 4
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
fairy_img = pygame.image.load('assets/images/fairy1.png')
nip_img = pygame.image.load('assets/images/nip.png')
bomb_img = pygame.image.load('assets/images/bird_poop.png')
background = pygame.image.load('assets/images/background.png')
cat_hit = [cat_hit1, cat_hit2, cat_hit3 ,cat_hit4, cat_hit5]
# Sounds
music1 = pygame.mixer.music.load('assets/sounds/music.wav')
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
    

        hit_list_nip = pygame.sprite.spritecollide(self, nips, True)
        for hit in hit_list_nip:
            self.cooldown = 0
            self.speed += 1
        
        hit_list = pygame.sprite.spritecollide(self, bombs, True)

        for hit in hit_list:
            #OOF.play()
            self.shield -= 1
            self.image = cat_hit[4 - self.shield]
            
        if self.shield == 0:
            #EXPLOSION.play()
            self.kill()
        hit_list_mobs = pygame.sprite.spritecollide(self, mobs, True)

        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH

    def is_dead(self):
        return self.shield <= 0
        

            
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


class Fairy(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def drop_bomb(self):
        nip = Nip(nip_img)
        nip.rect.centerx = self.rect.centerx
        nip.rect.centery = self.rect.bottom
        nips.add(nip)

    def update(self, lasers, player):
        hit_list_fairy = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            #EXPLOSION.play()
            player.score += 1
            self.kill()
            stage = WIN


class Nip(pygame.sprite.Sprite):
    
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
                m.image = pygame.transform.flip(m.image,1,0)
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

    def is_empty(self):
        return len(mobs) == 0
    
class Helper:

    def __init__(self, fairy):
        self.fairy = fairy
        self.drop_rate = 60
        self.speed = 5
        self.moving_right = True
        
        
    def move(self):
        reverse = False

        if self.moving_right:
            for f in fairies:
                f.rect.x += self.speed
                if f.rect.right >= WIDTH*5:
                    reverse = True
        else:
            for f in fairies:
                f.rect.x -= self.speed
                if f.rect.left <= -800:
                    reverse = True
        if reverse:
            self.moving_right = not self.moving_right

            for f in fairies:
                f.image = pygame.transform.flip(f.image,1,0)
                f.rect.y += 32


    def choose_bomber(self):
        rand = random.randrange(0, self.drop_rate)
        all_fairies = fairies.sprites()
        
        if len(all_fairies) > 0 and rand == 0:
            return random.choice(all_fairies)
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

#Helper Fuctions

def mobbyboys(mobs):
    mob1 = Mob(128, 64, enemy_img)
    mob2 = Mob(256, 64, enemy_img_1)
    mob3 = Mob(384, 64, enemy_img_2)
    mob4 = Mob(150, 34, enemy_img)
    mob5 = Mob(300, 34, enemy_img_1)
    
    mob_options = [mob1, mob2, mob3, mob4, mob5]

    for i in range(0, level):
        mobs.add(mob_options[i])



# Make sprite groups
player = pygame.sprite.GroupSingle()
player.score = 0

lasers = pygame.sprite.Group()

mobs = pygame.sprite.Group()


bombs = pygame.sprite.Group()

fairies = pygame.sprite.Group()


nips = pygame.sprite.Group()

def reset_mobs():
    global mobs, fleet

    mobs.empty()
    mobbyboys(mobs)

    fleet = Fleet(mobs)


def reset_player():
    global ship

    ship = Ship(384, 550, ship_img)
    player.add(ship)
    player.score = 0
    player.shield = 5
    
def setup():
    global stage, level, player, ship
    stage = START

    reset_player()
    reset_mobs()
    player.shield = 5

    fairy = Fairy(-1000, 64, fairy_img)
    fairies.empty()
    fairies.add(fairy)

    level = 1
    
def start():
    global stage
    stage = START
    screen.fill(BLACK)
    title_text = FONT_XL.render("Bye Bye Birdie!", True, WHITE)
    t_rect = title_text.get_rect()
    t_rect.centerx = WIDTH / 2
    t_rect.bottom = HEIGHT /3 
    text2 = FONT_MD.render("(Press ENTER to play.)", True, WHITE)
    t2_rect = text2.get_rect()
    t2_rect.centerx = WIDTH / 2
    t2_rect.bottom = HEIGHT /2 
    screen.blit(title_text, t_rect)
    screen.blit(text2, t2_rect)
    screen.blit(cat_icon, [300, 300])
    screen.blit(bird_icon, [800, 20])
    
    
def show_stats(player):
    score_text = FONT_S.render("Score: " + str(player.score), 1, WHITE)
    screen.blit(score_text, [32, 32])
    lives_text = FONT_S.render("Lives: " + str(ship.shield), 1, WHITE)
    screen.blit(lives_text, [850, 32])
    

def win():
    screen.fill(BLACK)
    font1 = pygame.font.Font(None, 48)
    text = font1.render("Stage Cleared!", 1, RED)
    screen.blit(text, [400, 200])
    text2 = font1.render("(Press SPACE to continue.)", True, WHITE)
    screen.blit(text2, [210, 500])


def win_game():
    screen.fill(BLACK)
    font1 = pygame.font.Font(None, 48)
    text = font1.render("Stage Cleared!", 1, RED)
    screen.blit(text, [400, 200])
    text2 = font1.render("(Press SPACE to continue.)", True, WHITE)
    screen.blit(text2, [210, 500])

def lose():
    screen.fill(BLACK)
    font1 = pygame.font.Font(None, 48)
    text = font1.render("Game Over!", 1, RED)
    screen.blit(text, [400, 200])
    text2 = font1.render("(Press SPACE to continue.)", True, WHITE)
    screen.blit(text2, [210, 500])
    


#Sound
pygame.mixer.music.play(-1)
#Level
level = 1

# Make fleet
ship = Ship(384, 550, ship_img)
helper = Helper(fairies)
start()
# Game loop
setup()
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
            if stage == LOSE:
                if event.key == pygame.K_SPACE:
                    stage = START
                    reset_player()
                    reset_mobs()
            if stage == WIN:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
                    reset_player()
                    reset_mobs()
                    level += 1 
                    
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
        nips.update()
        mobs.update(lasers, player)
        helper.update()
        fleet.update()

        if fleet.is_empty():
            stage = WIN
        if fleet.is_empty() and level >= 6 :
            stage = WIN_GAME
        if ship.is_dead():
            stage = LOSE
            
        
        
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
        nips.draw(screen)
        player.draw(screen)
        mobs.draw(screen)
        fairies.draw(screen)
        show_stats(player)
    if stage == WIN:
        win()
    if stage == WIN_GAME:
        win_game()
    if stage == LOSE:
        lose()
    
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
