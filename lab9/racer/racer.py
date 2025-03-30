import pygame, sys
from pygame.locals import *
import random, time

# Pygame кітапханасын бастау
pygame.init()

# FPS және сағат орнату
FPS = 60
clock = pygame.time.Clock()

# Түстерді анықтау
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Экран өлшемі мен бастапқы мәндер
W, H = 400, 600
SPEED = 5
SCORE = 0
COINS = 0

# Қаріптерді жүктеу және "Game Over" мәтінін дайындау
font = pygame.font.Font("font_user.ttf", 60)
font_small = pygame.font.Font("font_user.ttf", 20)
game_over = font.render("Game Over", True, BLACK)

# Монета иконкасын жүктеу және кішірейту
coin_icon = pygame.image.load("coin.png")
coin_icon = pygame.transform.scale(coin_icon, (coin_icon.get_width()//20, coin_icon.get_height()//20))

# Фон суретін жүктеу
bg = pygame.image.load("AnimatedStreet.png")

# Экран терезесін жасау
SC = pygame.display.set_mode((W, H))
SC.fill(WHITE)
pygame.display.set_caption("My game")

# Жаудың (Enemy) классы
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, W-40), 0)

    # Төменге қозғалады, экраннан шықса жаңартылады және ұпай қосылады
    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, W-40), 0)

# Ойыншы (Player) классы
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    # Солға немесе оңға қозғалу
    def move(self):
        pressed_key = pygame.key.get_pressed()
        if self.rect.left > 1:
            if pressed_key[K_LEFT]:
                self.rect.move_ip(-5, 0)
            if pressed_key[K_RIGHT]:
                self.rect.move_ip(5, 0)

# Монета (Coin) классы
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coin.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width()//12, self.image.get_height()//12))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, W-40), 0)

    # Монета төмен түседі, экраннан шықса орны жаңартылады
    def move(self):
        self.rect.move_ip(0, 5)
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, W-40), 0)

# Нысандарды жасау
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Спрайт топтары
enemies = pygame.sprite.Group()
enemies.add(E1)

coins_group = pygame.sprite.Group()
coins_group.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Жылдамдықты арттыру оқиғасы (әзірге сөндірулі)
'''INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 4000)'''

# Монета санау есептегіші
count = 0

# Ойын циклі
while True:
    for event in pygame.event.get():
        # Шығу оқиғасын тексеру
        if event.type == QUIT:
            pygame.quit()
            exit()

    # Фонды салу
    SC.blit(bg, (0, 0))

    # Монета иконкасы мен саны
    SC.blit(coin_icon, (10, 35))
    coins_v = font_small.render(f"X{str(COINS)}", True, BLACK)
    SC.blit(coins_v, (50, 50))

    # Барлық спрайттарды жаңарту және салу
    for entity in all_sprites:
        SC.blit(entity.image, entity.rect)
        entity.move()

    # Егер ойыншы жаумен соғылса
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)

        # Game Over экраны
        SC.fill(RED)
        SC.blit(game_over, (30, 250))
        result = font_small.render(f"Your result: {COINS}", True, BLACK)
        SC.blit(result, (120, 350))
        pygame.display.update()

        # Барлық спрайттарды жою және шығу
        for entity in all_sprites:
            entity.kill()
        
        time.sleep(2)
        pygame.quit()
        sys.exit()
    
    # Монета саны >5 болса, жылдамдықты арттыру
    if count > 5 and SPEED < 15:
        count = 0
        SPEED += 1

    # Егер ойыншы монетаны алса
    if pygame.sprite.spritecollideany(P1, coins_group):
        # Монета санына 1–4 аралығында қосу
        COINS += random.randint(1, 4)
        count += COINS
        for i in coins_group:
            i.rect.top = 0
            i.rect.center = (random.randint(40, W-40), 0)

    # Экранды жаңарту және уақытты өлшеу
    pygame.display.update()
    clock.tick(FPS)
