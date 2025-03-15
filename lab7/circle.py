import pygame

# Pygame кітапханасын бастау
pygame.init()

# Экран өлшемдерін орнату
W, H = 600, 400
sc = pygame.display.set_mode((W, H))

# Түстерді анықтау
WHITE = (255, 255, 255)  # Ақ түс
RED = (255, 0, 0)  # Қызыл түс

# Шардың қозғалу жылдамдығы
speed = 20

# Шардың бастапқы орны (экранның ортасы)
x, y = W // 2, H // 2

# Pygame-нің ішкі сағатын бастау
clock = pygame.time.Clock()

# Негізгі цикл (ойын үздіксіз жұмыс істеуі үшін)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Егер терезені жабу батырмасы басылса, бағдарламаны тоқтату
            exit()

    sc.fill(WHITE)  # Экранды ақ түспен бояу

    # Пернетақта батырмаларын тексеру
    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_DOWN]:  # Төменгі стрелка басылса
        if y > H - 27:
            y = H - 26
        else:
            y += speed
    if pressed[pygame.K_UP]:  # Жоғарғы стрелка басылса
        if y < 27:
            y = 26
        else:
            y -= speed
    if pressed[pygame.K_LEFT]:  # Сол жақ стрелка басылса
        if x < 27:
            x = 26
        else:
            x -= speed
    if pressed[pygame.K_RIGHT]:  # Оң жақ стрелка басылса
        if x > W - 27:
            x = W - 26
        else:
            x += speed

    # Қызыл түсті шеңберді экранға шығару
    circle = pygame.draw.circle(sc, RED, (x, y), 25)

    # Экранды жаңарту
    pygame.display.update()
    clock.tick(60)  # 60 FPS жылдамдықпен жаңарту (жылдам әрі тегіс жұмыс)
