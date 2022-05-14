#Создай собственный Шутер!

from pygame import *
from random import *
font.init()

window = display.set_mode((700,500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700,500))


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w,h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10, 15, 30)
        bullets.add(bullet)
        
lost = 0
score = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(5,635)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(5,635)

hero = Player('rocket.png', 20, 420, 7, 65, 65)

monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()

for i in range(5):
    monster = Enemy('ufo.png', randint(0,635), 0, randint(1,2), 65, 40)
    monsters.add(monster)

for i in range(2):
    asteroid = Asteroid('asteroid.png', randint(0,635), 0, randint(1,2), 65, 40)
    asteroids.add(asteroid)

clock = time.Clock()
FPS = 60

font = font.SysFont('Arial', 36)

game = True
finish = False

win = font.render('YOU WIN', True, (255,215,0))
lose = font.render('YOU LOSE', True, (255,0,0))

num_fire = 0
rel_time = False
from time import time as timer

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN and e.key == K_SPACE:
            if num_fire < 5 and rel_time == False:
                hero.fire()
                num_fire += 1
            else:
                rel_time = True
                old_time = timer()

    if finish != True:
        window.blit(background, (0,0))
        hero.update()
        hero.reset()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()

        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        sprites_list1 = sprite.spritecollide(hero, monsters, False)
        sprites_list2 = sprite.spritecollide(hero, asteroids, False)

        for s in sprites_list:
            score += 1
            monster = Enemy('ufo.png', randint(0,635), 0, randint(1,4), 65, 40)
            monsters.add(monster)
        
        if len(sprites_list1) > 0:
            window.blit(lose, (200,200))
            finish = True

        if len(sprites_list2) > 0:
            window.blit(lose, (200,200))
            finish = True
        
        if lost >= 5:
            window.blit(lose, (200,200))
            finish = True
        
        if score >= 10:            
            window.blit(win, (200,200))
            finish = True

        if rel_time == True:
            new_time = timer()
            if new_time - old_time >= 3:
                num_fire = 0
                rel_time = False
            else:
                text1 = font.render('Wait, reload...', 1, (255, 255, 255))
                window.blit(text1, (270,450))

        text_lose = font.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (0,40))
        
        text_win = font.render('Счет:' + str(score), 1, (255, 255, 255))
        window.blit(text_win, (0,0))
        
    display.update()
    clock.tick(FPS)