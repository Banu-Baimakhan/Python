import pygame
import random
import time
import psycopg2
from config import load_config
pygame.init()

score_now = 0

def create_table():
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("""CREATE TABLE IF NOT EXISTS users(
                                    id BIGSERIAL NOT NULL PRIMARY KEY,
                                    name VARCHAR(150) NOT NULL,
                                    score INTEGER NOT NULL,
                                    level INTEGER NOT NULL,
                                    max_score INTEGER NOT NULL
                            )""")
        print("Created users table")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
    
def insert_table(name):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users WHERE name = %s", (name,))
                user = cur.fetchone()

                if user:
                    print("User has found")
                    return user
                else:
                    cur.execute("INSERT INTO users(name, score, level, max_score) VALUES(%s, %s, %s, %s) RETURNING *", (name, 0, 1, 0))
                    new_user = cur.fetchone()
                    print("Added a new user")
                    return new_user
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def update_table(name):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE users SET score = %s, level = %s WHERE name = %s", (score_now, current_level, name))
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def reset_table(name):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("""UPDATE users SET score = %s, level = %s, max_score = %s WHERE name = %s""", (0, 1, 0, name))
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def set_max(name):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE users SET max_score = %s WHERE name = %s", (max_score, name))
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

is_created = False
if not is_created:
    create_table()
    is_created = True


W, H = 900, 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)

sc = pygame.display.set_mode((W, H))
sc.fill(BLACK)

bg = pygame.image.load('bg.jpg').convert()
bg = pygame.transform.scale(bg, (900, 600))
icon = pygame.image.load('icon.png').convert_alpha()
icon = pygame.transform.scale(icon, (icon.get_height()//3, icon.get_width()//3))
icon_rect = icon.get_rect(center=(450, 200))

start_button = pygame.image.load("play.png").convert_alpha()
start_button = pygame.transform.scale(start_button, (start_button.get_height()//3, start_button.get_width()//3))
start_button_rect =  start_button.get_rect(center=(450, 400))
pause_button = pygame.image.load("pause.png").convert_alpha()
pause_button = pygame.transform.scale(pause_button, (pause_button.get_height()//8, pause_button.get_width()//8))
pause_button_rect = pause_button.get_rect(center=(850, 20))
enter = pygame.image.load('enter.png').convert_alpha()
enter = pygame.transform.scale(enter, (enter.get_width()//15, enter.get_height()//15))
enter_rect = enter.get_rect(center=(450, 450))
save_button = pygame.image.load('save.png').convert_alpha()
save_button = pygame.transform.scale(save_button, (save_button.get_height()//45, save_button.get_width()//45))
save_button_rect = save_button.get_rect(center=(800, 500))
reset_button = pygame.image.load("reset.png").convert_alpha()
reset_button = pygame.transform.scale(reset_button, (reset_button.get_height()//30, reset_button.get_width()//30))
reset_button_rect = reset_button.get_rect(center=(100, 100))

snake_pos = [120, 210]
snake_head = pygame.image.load("head.png").convert_alpha()
snake_head = pygame.transform.scale(snake_head, (30, 30))
snake_head = pygame.transform.rotate(snake_head, 90)
snake_head_rect = snake_head.get_rect(topleft=(snake_pos))
sc.blit(snake_head, snake_head_rect)

snake_body = [[120, 210], [90, 210], [60, 210], [30, 210]]

fruits = [
    {"color": RED, "score": 10, "lifetime": 5},
    {"color": BLUE, "score": 20, "lifetime": 4},
    {"color": YELLOW, "score": 30, "lifetime": 3},
]

def spawn_fruit():
    pos = [random.randrange(0, W//30)*30, random.randrange(0, H//30)*30]
    fruit = random.choice(fruits)
    spawn_time = time.time()
    return {"pos": pos, "fruit": fruit, "spawn_time": spawn_time}

fruit_now = spawn_fruit()

spawn = True

def game_over():
    update_table(user_now[1])
    time.sleep(1)
    exit()


count = 0
snake_speed = 5
levels = {
    1: 5,
    2: 7,
    3: 9,
    4: 11,
    5: 13
}
current_level = 0
max_score = 0

def show_score(score, name, current_level, max_score, sc):
    font = pygame.font.Font("font_user.ttf", 25)
    text = font.render(f"SCORE {score}", True, PURPLE)
    text2 = font.render(f"User: {name}", True,PURPLE)
    text3 = font.render(f"Level: {current_level}", True, PURPLE)
    text4 = font.render(f"Max score: {max_score}", True, PURPLE)
    sc.blit(text, (10, 25))
    sc.blit(text2, (10, 5))
    sc.blit(text3, (10, 45))
    sc.blit(text4, (10, 65))

direction = "RIGHT"
direction_head = "RIGHT"
change_to = direction

clock = pygame.time.Clock()

is_started = False
is_pause = False
is_active = False
is_name = None

name = ""

count = 0
count_level = 0

fn = pygame.font.Font("font_user.ttf", 70)
fn2 = pygame.font.Font("font_user.ttf", 35)
fn3 = pygame.font.Font("font_user.ttf", 20)

user_now = None



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = "UP"
                pygame.mixer.Sound('bubble.mp3').play()
            if event.key == pygame.K_DOWN:
                change_to = "DOWN"
                pygame.mixer.Sound('bubble.mp3').play()
            if event.key == pygame.K_LEFT:
                change_to = "LEFT"
                pygame.mixer.Sound('bubble.mp3').play()
            if event.key == pygame.K_RIGHT:
                change_to = "RIGHT"
                pygame.mixer.Sound('bubble.mp3').play()
        
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            
            if start_button_rect.collidepoint(event.pos) and count == 0:
                is_started = not is_started
                is_active = not is_active
                count = 1
            
            if pause_button_rect.collidepoint(event.pos) and pygame.mouse.get_pressed()[0]:
                is_pause = not is_pause

            if start_button_rect.collidepoint(event.pos):
                is_pause = not is_pause

            if save_button_rect.collidepoint(event.pos):
                update_table(user_now[1])
                print("Updated")

            if reset_button_rect.collidepoint(event.pos):
                reset_table(user_now[1])
                score_now = 0
                current_level = 1
                max_score = 0
                print("Successfully done!")

        if event.type == pygame.KEYDOWN:
            if is_active:
                
                if event.key == pygame.K_RETURN and name!="":
                    is_name = name
                    print(f"Your name is {name}")
                elif event.key == pygame.K_BACKSPACE:
                    name=name[:-1]
                elif event.key == pygame.K_RETURN and name=="":
                    print("Enter a name")
                else:
                    name+=event.unicode
    

    if not is_started and count == 0:
        sc.blit(bg, (0, 0))
        sc.blit(icon, icon_rect)
        sc.blit(start_button, start_button_rect)


    if is_active:
        sc.blit(bg, (0, 0))
        sc.blit(enter, enter_rect)
        text2 = fn.render("Enter your name", True, GREEN)
        sc.blit(text2, (150, 100))
        text = fn.render(name, True, YELLOW)
        sc.blit(text, (100, 400))
        if is_name:
            user_now = insert_table(is_name)
            score_now = user_now[2]
            current_level = user_now[3]
            max_score = user_now[4]
            print(user_now)
            # text3 = fn.render(f"You're welcome, {user_now[1]}!Your score is {user_now[2]}", True, RED)
            # sc.blit(text3, (150, 200))
            # print(user_now)

            # time.sleep(3)
            is_active = not is_active

    if is_pause and user_now:
        sc.blit(bg, (0, 0))
        sc.blit(icon, icon_rect)
        sc.blit(start_button, start_button_rect)
        sc.blit(reset_button, reset_button_rect)
        text_score_now = fn.render(f"Score now: {score_now}", True, GREEN)
        text_max = fn2.render(f"Max score: {max_score}", True, GREEN)
        text_level = fn2.render(f"Current level: {current_level}", True, GREEN)
        text_reset = fn3.render("Reset", True, BLACK)
        sc.blit(text_reset, (100, 200))
        sc.blit(text_score_now, (150, 500))
        sc.blit(text_level, (150, 550))
        sc.blit(text_max, (150, 600))
        sc.blit(save_button, save_button_rect)

    if is_started and is_name and not is_pause:
        head_clone = snake_head
        
        temprory_direction = direction
        if change_to == "UP" and direction != "DOWN":
            direction = "UP"
            if temprory_direction == "LEFT":
                head_clone = pygame.transform.rotate(head_clone, -90)
            if temprory_direction == "RIGHT":
                head_clone = pygame.transform.rotate(head_clone, 90)
        if change_to == "DOWN" and direction != "UP":
            direction = "DOWN"
            if temprory_direction == "LEFT":
                head_clone = pygame.transform.rotate(head_clone, -90)
            if temprory_direction == "RIGHT":
                head_clone = pygame.transform.rotate(head_clone, 90)
        if change_to == "LEFT" and direction != "RIGHT":
            direction = "LEFT"
            if temprory_direction == "UP":
                head_clone = pygame.transform.rotate(head_clone, 90)
            if temprory_direction == "DOWN":
                head_clone = pygame.transform.rotate(head_clone, -90)
        if change_to == "RIGHT" and direction != "LEFT":
            direction = "RIGHT"
            if temprory_direction == "UP":
                head_clone = pygame.transform.rotate(head_clone, 90)
            if temprory_direction == "DOWN":
                head_clone = pygame.transform.rotate(head_clone, -90)

        snake_head = head_clone
        if direction == "UP":
            snake_pos[1] -= 30
        if direction == "DOWN":
            snake_pos[1] += 30
        if direction == "RIGHT":
            snake_pos[0] += 30
        if direction == "LEFT":
            snake_pos[0] -= 30
        
        
        snake_body.insert(0, list(snake_pos))

        if snake_pos[0] == fruit_now["pos"][0] and snake_pos[1] == fruit_now["pos"][1]:
            score_now += fruit_now["fruit"]["score"]
            count_level += 1
            fruit_now = spawn_fruit()
            spawn = False
        else:
            snake_body.pop()
        
        if time.time() - fruit_now["spawn_time"] > fruit_now["fruit"]["lifetime"]:
            fruit_now = spawn_fruit()
        
        if count_level == 4 and snake_speed <= 13:
            snake_speed += 2
            current_level += 1
            count_level = 0

        if score_now > max_score:
            max_score = score_now
            set_max(user_now[1])
        sc.fill(BLACK)


        for pos in snake_body[1:]:
            pygame.draw.rect(sc, GREEN, (pos[0], pos[1], 30, 30))
        
        sc.blit(head_clone, snake_pos)
        sc.blit(pause_button, pause_button_rect)
        pygame.draw.rect(sc, fruit_now["fruit"]["color"], (fruit_now["pos"][0], fruit_now["pos"][1], 30, 30))

        for blocks in snake_body[1:]:
            if snake_body[0] == blocks:
                game_over()

        if snake_body[0][0] < 0 or snake_body[0][0] > W-30:
            game_over()
        if snake_body[0][1] < 0 or snake_body[0][1] > H-30:
            game_over()
        show_score(score_now, user_now[1], current_level, max_score, sc)

    
    pygame.display.update()
    clock.tick(snake_speed)