from pygame import*
# класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        # Вызываем конструктор класс (Sprite):
        sprite.Sprite.__init__(self)
        # каждый спрайт должен хранить свойство image - изображение 
        self.image = transform.scale(image.load(player_image), (size_x, size_y))

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    #метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    
#класс MAIN character
class Player(GameSprite):
    #мктод, в котором реализовано управление спрайтом по кнопкам стрелками клавиатуры
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        #Вызываем конструктор класса (sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)

        self.x_speed = player_x_speed
        self.y_speed = player_y_speed

    def update(self):
        if packman.rect.x <= win_width-80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0: 
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched: 
                self.rect.left = max(self.rect.left, p.rect.right)
        if packman.rect.y <= win_height-80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.y_speed = 0
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.y_speed = 0
                self.rect.top = max
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):

    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.side = "left"

    def update(self):
            if self.rect.x <= 420:
                self.side = "right"
            if self.rect.x >= win_width - 85:
                self.side = "left"
            if self.side == "left":
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width + 10:
            self.kill()

win_width = 700
win_height = 500
display.set_caption("Лабиринт ฅ•ω•ฅ")
window = display.set_mode((win_width, win_height))
back = (160, 119, 201)

mixer.init()
mixer.music.load("alexander-nakarada-chase.mp3")
mixer.music.play()
sound_fire = mixer.Sound("puffing.ogg")

barriers = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()

w1 = GameSprite('brick.png',win_width / 2 - win_width / 3, win_height / 2, 300, 50)
w2 = GameSprite('brick.png', 370, 100, 50, 400)
barriers.add(w1)
barriers.add(w2)

packman = Player('hero.png', 5, win_height - 80, 80, 80, 0, 0)
final_sprite = GameSprite('istockphoto-1199025903-612x612.jpg', win_width - 85, win_height - 100, 80, 80)

monster1 = Enemy('enemy.png', win_width - 80, 180, 80, 0, 5)
monster2 = Enemy('enemy.png', win_width - 80, 230, 80, 4, 5)
monsters.add(monster1)
monsters.add(monster2)

finish = False
run = True
while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
            elif e.key == K_SPACE:
                sound_fire.play()
                packman.fire()
        
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0

    if not finish:
        window.fill(back)

        packman.update()
        bullets.update()

        packman.reset()

        bullets.draw(window)
        barriers.draw(window)
        final_sprite.reset()

        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)

        if sprite.spritecollide(packman, monsters, False):
            finish = True

            img = image.load()
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
    display.update()