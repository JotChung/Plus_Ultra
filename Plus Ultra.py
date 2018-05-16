#Pygame template - skeleton for a new pygame project 
import pygame
import RPi.GPIO as GPIO
from random import randint, choice, random
import os
from os import path

#Finds img and snd folders 
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 800
HEIGHT = 450
FPS = 60

#Defined Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

POWERUP_TIME = 5000



        
#initialize pygame and create window 
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()


#Finds the closest font match to the font attempting to be used 
font_name = pygame.font.match_font('arial')
#Draw Lives
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)
#Draw Shield Bar Function
def draw_shield_bar(surf, x, y, pct):
    #Ensure bar doesnt reach negative values
    if( pct < 0):
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = player.shield
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_boss_bar(surf, x, y, pct):
    #Ensure bar doesnt reach negative values
    if( pct < 0):
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = boss.health
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_boss_bar2(surf, x, y, pct):
    #Ensure bar doesnt reach negative values
    if( pct < 0):
        pct = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 10
    fill = boss2.health
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

#Game over screen Funciton
def show_go_screen():
    #Erases leftover game details after death - reset screen
    screen.blit(background, background_rect)
    #Game over screen text 
    draw_text(screen, "PLUS ULTRA!", 64, WIDTH/2, HEIGHT / 4)
    draw_text(screen, "Buttons to move and to fire", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press any button to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    #flip the screen so players can see it
    pygame.display.flip()
    #Another init cuz an error was popping up saying "video system not initialized" 
    pygame.init()
    waiting = True
    while(waiting):
        clock.tick(FPS)
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
            if(event.type == pygame.KEYUP):
                waiting = False

#Game Won screen Function
def show_gw_screen():
    #Erases leftover game details after death - reset screen
    screen.blit(background, background_rect)
    #Game over screen text 
    draw_text(screen, "CONGRATS!", 64, WIDTH/2, HEIGHT / 4)
    draw_text(screen, "You survived!!!", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a button to play again", 18, WIDTH / 2, HEIGHT * 3 / 4)
    #flip the screen so players can see it
    pygame.display.flip()
    #Another init cuz an error was popping up saying "video system not initialized" 
    pygame.init()
    waiting = True
    while(waiting):
        clock.tick(FPS)
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
            if(event.type == pygame.KEYUP):
                waiting = False
    
#Create mob function
### *Remember to Add way to randomize which mobs are created 
def newmob():
    r = Mob2()
    all_sprites.add(r)
    mobs.add(r)

def newmob2():
    r = Mob()
    all_sprites.add(r)
    mobs.add(r)

def randmob():
    mobs = [newmob(), newmob2()]
    choice(mobs)

def spawn_boss():
    boss = Player2()
    all_sprites.add(boss)
    bosses.add(boss)
    
#Draw text onto screen
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
    

class Player(pygame.sprite.Sprite):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH /2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        #Starts game with sull shield
        self.shield = 100
        #Delays each shot by 250 miliseconds 
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        #Player lives 
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        #Gun powerup info
        #Changes according to "power level" ie: 1 = normal shooting and 2 = the powerup effect 
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        

    def update(self):
        #Timeout gun powerup/stop it 
        if (self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME):
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
            
        #Unhide if hidden and place player back at starting point 
        if (self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000):
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        #Player Movements 
        self.speedx = 0
        self.speedy = 0 
        #Moves Sprite left
        if (GPIO.input(19) == 1):
            self.speedx = -8
        #Moves Sprite right 
        if (GPIO.input(22) == 1):
            self.speedx = 8 
        self.rect.x += self.speedx
        #Stops Sprite from passing left and right borders 
        if (self.rect.right > WIDTH):
            self.rect.right = WIDTH
        if (self.rect.left < 0):
            self.rect.left = 0
        #Allows the player to shoot constantly instead of repeated presses
        if (GPIO.input(24) == 1):
            self.shoot()

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

        
    def shoot(self):
        now = pygame.time.get_ticks()
        if (now - self.last_shot > self.shoot_delay):
            self.last_shot = now
            if(self.power == 1):
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            #Gun Powerup lvl 1 
            if(self.power >= 2 and self.power < 5):
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
            #Gun Powerup Lvl 2 
            if(self.power >= 5):
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                bullet3 = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet2)
                self.shoot_delay = 100
                shoot_sound.play()
            #Gun Powerup Lvl God
            if(self.power >= 7):
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                bullet3 = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet2)
                self.shoot_delay = 10
                shoot_sound.play()
             

    def hide(self):
        #hides the player temporarily after death
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT * 200)

class Player2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(boss1_img, (100,100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = 850
        self.rect.bottom = 100
        self.speedx = 5
        #Boss health
        self.health = 100
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.shoot_delay = 800
        self.last_shot = pygame.time.get_ticks()
        self.boss_shoot = False
        self.boss_shot_timer = pygame.time.get_ticks()
        

    def update(self):
        #Stops boss from shooting if it is "dead" 
        if (self.rect.bottom < 500):
            self.shoot()
 
            
        self.rect.x += self.speedx 
        #Boss Movements
        #Stops Sprite from passing left and right borders 
        if (self.rect.right > WIDTH):
            self.speedx = -5
        if (self.rect.left < 0):
            self.speedx = 5

    def shoot(self):
        #Times when the boss will shoot
        now = pygame.time.get_ticks()
        if (now - self.last_shot > self.shoot_delay):
            self.last_shot = now
            bullet = BossBullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(bullet)
            bbullet.add(bullet)
            shoot_sound.play()

    def hide(self):
        #hides the player temporarily after death
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.bottom = 720
        
class Player3(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(boss2_img, (100,100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = 850
        self.rect.bottom = 100
        self.speedx = 5
        #Boss health
        self.health = 100
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.shoot_delay = 800
        self.last_shot = pygame.time.get_ticks()
        self.boss_shoot = False
        self.boss_shot_timer = pygame.time.get_ticks()
        

    def update(self):
        #Stops boss from shooting if it is "dead" 
        if (self.rect.bottom < 500):
            self.shoot()
 
            
        self.rect.x += self.speedx 
        #Boss Movements
        #Stops Sprite from passing left and right borders 
        if (self.rect.right > WIDTH):
            self.speedx = -5
        if (self.rect.left < 0):
            self.speedx = 5

    def shoot(self):
        #Times when the boss will shoot
        now = pygame.time.get_ticks()
        if (now - self.last_shot > self.shoot_delay):
            self.last_shot = now
            bullet = BossBullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(bullet)
            bbullet.add(bullet)
            shoot_sound.play()

    def hide(self):
        #hides the player temporarily after death
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.bottom = 720

class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 15

    def update(self):
        self.rect.y += self.speedy

        #kill if it moves oof the top of the screen
        if (self.rect.bottom > HEIGHT):
            self.kill()
        

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.transform.scale(meteor_img, (50,38))
        self.image_orig.set_colorkey(BLACK)
        #Copy of image for animation
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 /2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = randint(0, WIDTH - self.rect.width)
        self.rect.y = randint(-100, -40)
        self.speedy = randint(1, 8)
        self.speedx = randint(-3, 3)
        #Animation
        self.rot = 0
        self.rot_speed = randint(-8, 8)
        self.last_update = pygame.time.get_ticks()
        
    def rotate(self):
        now = pygame.time.get_ticks()
        if (now - self.last_update > 50):
            self.last_update = (self.rot * self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.image_orig, self.rot)
            

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if (self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20):
            self.rect.x = randint(0, WIDTH - self.rect.width)
            self.rect.y = randint(-100, -40)
            self.speedy = randint(1, 8)


    
            
class Mob2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        #Copy of image for animation (rotating)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 /2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = randint(0, WIDTH - self.rect.width)
        self.rect.y = randint(-150, -100)
        self.speedy = randint(1, 8)
        self.speedx = randint(-3, 3)
        #Animation "rotate"
        self.rot = 0
        self.rot_speed = randint(-8, 8)
        self.last_update = pygame.time.get_ticks()
        
    def rotate(self):
        now = pygame.time.get_ticks()
        if (now - self.last_update > 50):
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.image_orig, self.rot)
            #Creates a new center each time the rock rotates to help rotate cleaner 
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center 
            

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if (self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20):
            self.rect.x = randint(0, WIDTH - self.rect.width)
            self.rect.y = randint(-100, -40)
            self.speedy = randint(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy

        #kill if it moves oof the top of the screen
        if (self.rect.bottom < 0):
            self.kill()

#Powerup Class 
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 4

    def update(self):
        self.rect.y += self.speedy

        #kill if it moves oof the top of the screen
        if (self.rect.top > HEIGHT):
            self.kill()

class Explosion(pygame.sprite.Sprite):
    #places the explosion at the center of what was hit
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        #Choses between a large/small explosion depending on what was hit
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        #The framrate "speed" of the the explosion "Animation" 
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if (now - self.last_update > self.frame_rate):
            self.last_update = now
            self.frame += 1
            if(self.frame == len(explosion_anim[self.size])):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center 
        

#Load all game graphics
#Backround image
background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background_rect = background.get_rect()

#Player/Mob Images 
player_img = pygame.image.load(path.join(img_dir, "Bulldog.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
boss1_img = pygame.image.load(path.join(img_dir, "Ulm- logo.png")).convert()
boss2_img = pygame.image.load(path.join(img_dir, "lsu-logo.png")).convert()
meteor_img = pygame.image.load(path.join(img_dir, "enemyBlack1.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserBlue16.png")).convert()
rock_img = pygame.image.load(path.join(img_dir, "meteorBrown_med1.png")).convert()
meteor_images = []
meteor_list = ["Charlotte_49ers_logo.png", "fiu-golden-panthers.png", "Marshall-Logo.png",
               "mktg_logo.png", "MT-logo.png", "north_logo.png", "ntex-lg.png", "old-dominion-logo.png",
               "Southern-Miss-logo.png", "UAB_logo.png", "utep-miners.png", "utsa-logo.png", "rice-owls.png"]
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

#Explosion Animations
explosion_anim = {}
#Large explosions
explosion_anim['lg'] = []
#Small Explosions
explosion_anim['sm'] = []
#Player Explosion Animation
explosion_anim['player'] = []

for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    #Resizes the explosons *Keep Width and height the same 
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)

    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

#Powerup images
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'powerupYellow_shield.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()
    
    
    

#Load all game sounds: Explosions and Laser
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'laser_sound.wav'))
shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'Shieldpowerup.wav'))
power_sound = pygame.mixer.Sound(path.join(snd_dir, 'gun_powerup.wav'))
expl_sounds = []
for snd in ["expl1.wav", "expl2.wav"]:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
#Player Death Sound
player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
#Background music 
pygame.mixer.music.load(path.join(snd_dir, "tgfcoder-FrozenJam-SeamlessLoop.ogg"))
pygame.mixer.music.set_volume(0.4) #Lowers volume 

#Come back later Tony

pygame.mixer.music.play(loops = -1)

#Game Loop
game_won = 0 
game_over = True 
running = True
while(running):
    #Gamve over screen
    if (game_over):
        show_go_screen()
        game_over = False
        #Reset Game 
        #Sprite Group
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        bosses = pygame.sprite.Group()
        bbullet = pygame.sprite.Group()
        #Sprites
        player = Player()
        all_sprites.add(player)
        #Boss information 
        boss = Player2()
        boss2 = Player3()
        boss2.shoot_delay = 100
        boss2.health = 200
        boss2.rect.bottom = 200
        score = 0
        level = 1
        #Make highscore thingy

        #Mobs
        for mob in range(5):
            mob = newmob()

        for mob in range(5):
            mob = newmob2()



    if (game_won >= 1):
        player.speedy = 10
        show_gw_screen()
        game_won = False
        #Reset Game 
        #Sprite Group
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        bosses = pygame.sprite.Group()
        bbullet = pygame.sprite.Group()
        #Sprites
        player = Player()
        all_sprites.add(player)
        #Boss information 
        boss = Player2()
        boss2 = Player2()
        boss2.shoot_delay = 100
        boss2.health = 200
        boss2.rect.bottom = 200
        score = 0
        level = 1     
            
        #Mobs
        for mob in range(5):
            mob = newmob()

        for mob in range(5):
            mob = newmob2()
        

        
##    if(score == 10):
##        print "here"
##        for i in range(1):
##            mob2 = newmob2()
        
    clock.tick(FPS)
    
    #Process input (events)
    for event in pygame.event.get():
        #check for window closing
        if(event.type == pygame.QUIT):
            running = False

    #Update
    all_sprites.update()


    #Check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        #Score updater
        #score += (50 - hit.radius)
        score += 1
        if(score == 10):
            for i in range(10):
                mob2 = newmob2()

        if(score == 15):
            for i in range(10):
                mob3 = newmob()
        #Spawn boss
        if(score == 30):
            all_sprites.add(boss)
            level += 1

        if(score == 60):
                all_sprites.add(boss2)
                level += 1

        if(score == 45):
                for i in range(10):
                    mob3 = newmob()

        


        choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        #Gives a chance at dropping a powerup after hitting a mob
        if (random() > 0.9):
            p = Pow(hit.rect.center)
            all_sprites.add(p)
            powerups.add(p)
            
            
        
        
    #Check to see if a mob hit a player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle) 
    for hit in hits:
        #Shield damage
        player.shield -= hit.radius * 2
        #Player hit explosion
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob2()
        #Game Ends if player shield is gone
        if(player.shield <= 0):
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    #Check to see if a boss his a player
    hits = pygame.sprite.spritecollide(player, bbullet, True, pygame.sprite.collide_circle)
    for hit in hits:
        #Shield damage
        player.shield -= 20
        #Player hit explosion
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        #Game Ends if player shield is gone
        if(player.shield <= 0):
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    #Check to see if a bullet hit a boss
    hits = pygame.sprite.spritecollide(boss, bullets, True, pygame.sprite.collide_circle)
    for hit in hits:
        #Shield damage
        boss.health -= 15
        #Player hit explosion
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        #Game Ends if player shield is gone
        if(boss.health <= 0):
            player_die_sound.play()
            boss_death = Explosion(boss.rect.center, 'player')
            all_sprites.add(boss_death)
            boss.hide()
            score += 10

            if(score == 40):
                for i in range(10):
                    mob2 = newmob2()

##            if(score == 45):
##                for i in range(10):
##                    mob3 = newmob()

    hits = pygame.sprite.spritecollide(boss2, bullets, True, pygame.sprite.collide_circle)
    for hit in hits:
        #Shield damage
        boss2.health -= 20
        #Player hit explosion
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        #Game Ends if player shield is gone
        if(boss2.health <= 0):
            player_die_sound.play()
            boss_death = Explosion(boss.rect.center, 'player')
            all_sprites.add(boss_death)
            boss2.hide()
            game_won += 1

    #Check to see if a boss hit a player
    
            

    #If the player hit a powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        #Shield Powerup, returns a random amount of shield "hp"
        if (hit.type == 'shield'):
            player.shield += randint(10,30)
            shield_sound.play()
            #Caps shield at 100
            if(player.shield >= 100):
                player.shield = 100
        #Gun Powerup,
        if( hit.type == 'gun'):
            player.powerup()
            power_sound.play()            
            

    #If the player died and the explosion has finished
    if((player.lives == 0) and (death_explosion.alive() == False)):
        game_over = True 
   
    #Draw/Render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    #Score
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    #Level
    draw_text(screen, "Level {}".format(str(level)), 18, 25, 50)
    #Player Health 
    draw_shield_bar(screen, 5,5, player.shield)
    #Boss health 
    draw_boss_bar(screen, 5,20, boss.health)
    draw_boss_bar2(screen, 5,35, boss2.health)
    #Player lives 
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    
    # *after* drawing everything, flip the display 
    pygame.display.flip()

#Brings user back to Main menu
###

pygame.quit()
