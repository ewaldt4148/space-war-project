# Imports
import pygame

# Initialize game engine
pygame.init()


# Window
WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
TITLE = "Space War"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Images
cat_board_img = pygame.image.load('assets/images/cat_left.png')
poop_img = pygame.image.load('assets/images/bird_poop.png')
bird1_img = pygame.image.load('assets/images/bird1.jpg')
bird2_img = pygame.image.load('assets/images/bird2.jpg')

# Game classes
class Cat(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = 3
        self.shield = 10

    def move_left(self):
        self.rect.x -= self.speed
        
    def move_right(self):
        self.rect.x += self.speed

    def shoot(self):
        las = Laser(poop_img)
        
        las.rect.centerx = self.rect.centerx
        las.rect.centery = self.rect.top
        
        lasers.add(las)
        print("Pew!")

    def update(self):
        pass


    
class Laser(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        self.speed = 3
        
    def update(self):
        self.rect.y -= self.speed



    
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self, lasers):
        hit_list = pygame.sprite.spritecollide(self, lasers, True)

        if len(hit_list) > 0:
            #sound.play()
            self.kill()
            

class Bomb:
    
    def __init__(self):
        pass

    def update(self):
        pass
    
    
class Fleet:

    def __init__(self):
        pass

    def update(self):
        pass

    
# Make game objects
cat = Cat(400, 400, cat_board_img )
bird1 = Mob( 128, 64, bird1_img)
bird2 = Mob( 200, 64, bird2_img)

# Make sprite groups
player = pygame.sprite.Group()
player.add(cat)

lasers = pygame.sprite.Group()

mobs = pygame.sprite.Group()
mobs.add(bird1, bird2)

# Game loop
done = False

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ship.shoot()

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_LEFT]:
        ship.move_left()
    elif pressed[pygame.K_RIGHT]:
        ship.move_right()
        
    
    # Game logic (Check for collisions, update points, etc.)
    lasers.update()
    mobs.update(lasers)
        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.fill(BLACK)
    lasers.draw(screen)
    player.draw(screen)
    mobs.draw(screen)

    
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
