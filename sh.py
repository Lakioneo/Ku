import random
import time as t
from pygame import *



mixer.init()
font.init()

width = 700
height =  500

speed_mons = 3
speed_player = 10

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, speed, width = 40 , height = 65):
        sprite.Sprite.__init__(self)
        self.width = width
        self.image = transform.scale( image.load(img), (width,height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < width - self.width:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet( "img/bullet.png", self.rect.centerx, self.rect.top, 15, 15, 20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > height:
            self.rect.y = 0
            self.rect.x = random.randint(5 , width - self.width)
            self.speed = random.randint(1 , 5)
            lost += 1

class Asteroid(GameSprite):
    def __init__(self, img, x, y, speed, width=40, height=65):
        super().__init__(img, x, y, speed, width, height)
        self.hp = 2

    def update(self):
        self.rect.y += self.speed
        if sprite.spritecollide(self.rect,bullets,False):
            self.hp -= 2
        if self.hp < 0 or self.rect.y > height:
            self.kill()
        

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()



window = display.set_mode((width,height))
back = transform.scale(image.load("img/galaxy.jpg"),(width,height))

play = Player("img/rocket.png", (width + 40)/2, height - 75, speed_player, 40,65)

bullets = sprite.Group()

monsters  = sprite.Group()
for i in range(3):
    mons  = Enemy("img/ufo.png", random.randint(65,width-65), 0, random.randint(1,speed_mons), 65,40)
    monsters.add(mons)

asteroids  = sprite.Group()
asteroid  = Enemy("img/asteroid.png", random.randint(65,width-65), 0, random.randint(1,2),50,50)
asteroids.add(asteroid)

text = font.Font("font/Tataric2_0.ttf",20)
lost = 0
score = 0

mixer.music.load("song/space.ogg")
#mixer.music.play()

fire = mixer.Sound("song/fire.ogg")


clock = time.Clock()
fps = 60

game = True
run = True

start = t.time()
while game:
    for ev in event.get():
        if ev.type == QUIT:
            game = False
        if ev.type == KEYDOWN and run:
            if ev.key == K_SPACE:
                play.fire()
                #fire.play()

    window.blit(back,(0,0))

    if run:
        lost_text = text.render("Пропущено: " + str(lost), True, (255,255,255)) 
        window.blit(lost_text,(width - 150,height - 20))

        win_text = text.render("Уничтожено: " + str(score), True, (255,255,255)) 
        window.blit(win_text,(10,height - 20))

        play.update()
        bullets.update()
        monsters.update()
        asteroids.update()

        play.reset()
        bullets.draw(window)
        monsters.draw(window)
        asteroids.draw(window)

        collides = sprite.groupcollide(monsters,bullets,True,True)
        for collide in collides:
            score += 1
            monster = Enemy("img/ufo.png", random.randint(65,width-65), 0, random.randint(1,speed_mons), 65,40)
            monsters.add(monster)


        n = t.time()
        print(n - start)
        if n - start > 10:
            start = n
            if len(asteroids) < 3:
                asteroid  = Enemy("img/asteroid.png", random.randint(65,width-65), 0, random.randint(1,2),50,50)
                asteroids.add(asteroid)
            if len(monsters) < 6:
                mons  = Enemy("img/ufo.png", random.randint(65,width-65), 0, random.randint(1,speed_mons), 65,40)
                monsters.add(mons)



        if sprite.spritecollide(play,asteroids,False):
            run = False


    else:
        
        win_text = text.render("Уничтожено: " + str(score), True, (255,255,255)) 
        window.blit(win_text,(
                                width /2-win_text.get_rect().centerx,
                                height /2-win_text.get_rect().centery
                            )
                    )

    display.update()
    clock.tick(fps)

