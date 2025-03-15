import pygame
import datetime

# Pygame кітапханасын бастау
pygame.init()

# Экран өлшемдерін орнату
W, H = 600, 400
sc = pygame.display.set_mode((W, H))

# Қаріп (шрифт) жүктеу
time_font = pygame.font.Font('font_user.ttf', 24)

# Түстерді анықтау
WHITE = (255, 255, 255)  # Ақ түс
RED = (255, 0, 0)  # Қызыл түс
YELLOW = (239, 228, 176)  # Сары түс

# Уақытты экранға шығару функциясы
def system_time(now):
    global time_font
    
    min = now.strftime('%M')  # Ағымдағы минутты алу
    sec = now.strftime('%S')  # Ағымдағы секундты алу
    
    # Уақыт мәтінін жасау (қызыл түсті, сары фонда)
    sc_text = time_font.render(f"{min}:{sec}", 1, RED, YELLOW)
    pos = sc_text.get_rect()

    # Уақыттың экрандағы орны (төменгі оң жақ бұрыш)
    pos.x, pos.y = 500, 350
    sc.blit(sc_text, pos)  # Мәтінді экранға шығару

# Сағаттың және тілдердің суреттерін жүктеу
clock_sc = pygame.image.load('clock.png').convert_alpha()  # Сағат фоны
leftarm_sc = pygame.image.load('leftarm.png').convert_alpha()  # Секунд тілі
rightarm_sc = pygame.image.load('rightarm.png').convert_alpha()  # Минут тілі

# Сағаттың өлшемін экранға бейімдеу
clock_sc = pygame.transform.scale(clock_sc, (W, H))

# Тілдердің өлшемдерін өзгерту (2.5 есе кішірейту)
leftarm_sc = pygame.transform.scale(leftarm_sc, (leftarm_sc.get_width()//2.5, leftarm_sc.get_height()//2.5))
rightarm_sc = pygame.transform.scale(rightarm_sc, (rightarm_sc.get_width()//2.5, rightarm_sc.get_height()//2.5))

# Тілдердің бастапқы бұрышын анықтау
angle = 0

# Pygame-нің ішкі сағатын бастау
clock = pygame.time.Clock()

# Тілдердің айналу нүктесін (ортасын) орнату
leftarm_rect = leftarm_sc.get_rect(center=(W//2, H//2))
rightarm_rect = rightarm_sc.get_rect(center=(W//2, H//2))

# Бастапқы тілдерді экранға орналастыру
sc.blit(leftarm_sc, leftarm_rect)
sc.blit(rightarm_sc, rightarm_rect)

# Негізгі цикл (сағатты үздіксіз жұмыс істеу үшін)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Егер терезені жабу батырмасы басылса, бағдарламаны тоқтату
            exit()

    now = datetime.datetime.now()  # Ағымдағы уақытты алу
    sc.fill((255, 255, 255))  # Экранды ақ түспен бояу
    sc.blit(clock_sc, (0, 0))  # Сағаттың фонын экранға шығару

    # Тілдердің бұрышын есептеу (секунд сайын қозғалады)
    angle = -(now.second+1)*6  # Секунд тілі (1 секунд = 6°)
    angle2 = -(now.minute)*6  # Минут тілі (1 минут = 6°)

    # Секунд тілін айналдыру және экранға орналастыру
    leftarm_sc_rotated = pygame.transform.rotate(leftarm_sc, angle)
    leftarm_rect_rotated = leftarm_sc_rotated.get_rect(center=leftarm_rect.center)
    sc.blit(leftarm_sc_rotated, leftarm_rect_rotated)

    # Минут тілін айналдыру және экранға орналастыру
    rightarm_sc_rotated = pygame.transform.rotate(rightarm_sc, angle2-54)
    rightarm_rect_rotated = rightarm_sc_rotated.get_rect(center=rightarm_rect.center)
    sc.blit(rightarm_sc_rotated, rightarm_rect_rotated)

    # Экранға уақытты шығару
    system_time(now)

    # Экранды жаңарту
    pygame.display.update()

    # Сағатты 1 FPS жылдамдықпен жаңарту (әр секунд сайын)
    clock.tick(1)
