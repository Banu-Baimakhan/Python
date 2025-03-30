import pygame
import random
import time

# Жыланның бастапқы жылдамдығы
snake_speed = 5

# Pygame-ді бастау
pygame.init()

# Терезе өлшемі
W, H = 720, 480

# Түстерді анықтау
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)

# Терезе тақырыбы мен өлшемі
pygame.display.set_caption("Snake Game")
screen = pygame.display.set_mode((W, H))

# FPS басқаруға арналған сағат
FPS = pygame.time.Clock()

# Жыланның бастапқы орны мен денесі
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

# Әр түрлі салмақтағы жемістер (ұпай мен уақытқа байланысты)
food_types = [
    {"color": RED, "score": 10, "lifetime": 5},     # кәдімгі жеміс
    {"color": BLUE, "score": 20, "lifetime": 4},    # сирек жеміс
    {"color": YELLOW, "score": 30, "lifetime": 3}   # өте сирек жеміс
]

# Жаңа жеміс тудыру функциясы
def spawn_fruit():
    pos = [random.randrange(1, (W//10)) * 10, random.randrange(1, (H//10)) * 10]
    food = random.choice(food_types)
    spawn_time = time.time()
    return {"pos": pos, "type": food, "spawn_time": spawn_time}

# Бірінші жеміс
fruit = spawn_fruit()

# Бағыт айнымалылары
direction = "RIGHT"
change_to = direction

# Ұпай мен жеміс санау
score = 0
count_food = 0

# Ұпайды экранға шығару функциясы
def show_score(choice, color, font, size):
    score_font = pygame.font.Font(font, size)
    score_surf = score_font.render('Score: ' + str(score), True, color)
    score_rect = score_surf.get_rect()
    screen.blit(score_surf, score_rect)

# Ойынның аяқталуы
def game_over():
    my_font = pygame.font.Font("font_user.ttf", 30)
    game_over_surf = my_font.render("Your score is: " + str(score), True, RED)
    game_over_rect = game_over_surf.get_rect()
    game_over_rect.midtop = (W/4, H/4)
    screen.blit(game_over_surf, game_over_rect)
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    exit()

# Негізгі ойын циклі
while True:
    # Басқару оқиғалары
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            elif event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT:
                change_to = "LEFT"
            elif event.key == pygame.K_RIGHT:
                change_to = "RIGHT"

    # Қарама-қарсы бағытқа бұрылмау
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Жылан қозғалысы
    if direction == 'UP':
        snake_pos[1] -= 10
    elif direction == 'DOWN':
        snake_pos[1] += 10
    elif direction == 'RIGHT':
        snake_pos[0] += 10
    elif direction == 'LEFT':
        snake_pos[0] -= 10

    # Жаңа бастың орнын қосу
    snake_body.insert(0, list(snake_pos))

    # Егер жылан жемісті жесе
    if snake_pos == fruit["pos"]:
        score += fruit["type"]["score"]
        count_food += 1
        fruit = spawn_fruit()  # жаңа жеміс
    else:
        # Жемесең — құйрықтан алып таста
        snake_body.pop()

    # Егер жеміс уақыты өтіп кетсе
    if time.time() - fruit["spawn_time"] > fruit["type"]["lifetime"]:
        fruit = spawn_fruit()

    # Сурет салу
    screen.fill(BLACK)

    # Жыланды салу
    for pos in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

    # Жемісті салу
    pygame.draw.rect(screen, fruit["type"]["color"], pygame.Rect(fruit["pos"][0], fruit["pos"][1], 10, 10))

    # Қабырғаға соғылса — ойын бітті
    if snake_pos[0] < 0 or snake_pos[0] > W - 10 or snake_pos[1] < 0 or snake_pos[1] > H - 10:
        game_over()

    # Өзімен соғылса — ойын бітті
    for block in snake_body[1:]:
        if snake_pos == block:
            game_over()

    # Әр 4 жемістен кейін жылдамдықты арттыру
    if count_food == 4 and snake_speed < 24:
        snake_speed += 3
        count_food = 0

    # Ұпайды шығару
    show_score(1, PURPLE, 'font_user.ttf', 20)
    pygame.display.update()
    FPS.tick(snake_speed)
