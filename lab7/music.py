import pygame
import os

# Pygame және аудио микшерін бастау
pygame.init()
pygame.mixer.init()

# Экран параметрлері
WIDTH, HEIGHT = 600, 150
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Музыка ойнатқыш")

# Шрифт орнату
font = pygame.font.Font(None, 36)

# Суреттерді жүктеу (барлығы кодпен бір папкада орналасқан)
pause_img = pygame.image.load("pause.png")  # Пауза түймесі
play_img = pygame.image.load("play.png")  # Ойнату түймесі
prev_img = pygame.image.load("previous.png")  # Алдыңғы ән түймесі
skip_img = pygame.image.load("skip.png")  # Келесі ән түймесі

# Түймелердің өлшемін өзгерту (егер өте үлкен болса)
button_size = (50, 50)
pause_img = pygame.transform.scale(pause_img, button_size)
play_img = pygame.transform.scale(play_img, button_size)
prev_img = pygame.transform.scale(prev_img, button_size)
skip_img = pygame.transform.scale(skip_img, button_size)

# Түймелердің экрандағы орналасуы
pause_rect = pause_img.get_rect(topleft=(200, 80))
play_rect = play_img.get_rect(topleft=(260, 80))
prev_rect = prev_img.get_rect(topleft=(320, 80))
skip_rect = skip_img.get_rect(topleft=(380, 80))

# Папкадағы барлық MP3 файлдарын табу
songs = [f for f in os.listdir() if f.endswith(".mp3")]

if not songs:  # Егер MP3 файлдар жоқ болса, қате шығару
    print("Қате: Папкада MP3 файлдары жоқ! Музыка қосу керек.")
    pygame.quit()
    exit()

current_song_index = 0  # Қазіргі ойналып жатқан әннің индексі

# Музыканы ойнату функциясы
def play_music(index):
    if songs:  # Егер әндер бар болса ғана ойнату
        pygame.mixer.music.load(songs[index])
        pygame.mixer.music.play()

# Егер әндер табылса, бірінші әнді ойнату
play_music(current_song_index)

running = True  # Бағдарлама жұмыс істеп тұрғанын білдіретін айнымалы
paused = False  # Әннің паузада екенін тексеру

# Негізгі цикл (GUI интерфейсі мен басқару жүйесі)
while running:
    screen.fill((255, 255, 255))  # Фонды ақ түске бояу

    # Ойнатылып жатқан әннің атауын шығару (Paused немесе Playing)
    state_text = "Пауза" if paused else "Ойнатылып жатыр"
    label = font.render(f"{songs[current_song_index]} ({state_text})", True, (0, 0, 0))
    screen.blit(label, (50, HEIGHT // 2 - 30))

    # Түймелерді экранға шығару
    screen.blit(pause_img, pause_rect)
    screen.blit(play_img, play_rect)
    screen.blit(prev_img, prev_rect)
    screen.blit(skip_img, skip_rect)

    # Оқиғаларды тексеру (пернетақта немесе тінтуір басу)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Егер терезені жабу батырмасы басылса, цикл тоқтайды

        # Пернетақта арқылы басқару
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Пробел (пауза/ойнату)
                if paused:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()
                paused = not paused

            elif event.key == pygame.K_RIGHT:  # Келесі ән (оң жақ стрелка)
                current_song_index = (current_song_index + 1) % len(songs)
                play_music(current_song_index)
                paused = False
            elif event.key == pygame.K_LEFT:  # Алдыңғы ән (сол жақ стрелка)
                current_song_index = (current_song_index - 1) % len(songs)
                play_music(current_song_index)
                paused = False

        # Тінтуір арқылы басқару
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()  # Тінтуірдің басылған жерін анықтау
            
            if pause_rect.collidepoint(mouse_pos):  # Егер "pause" батырмасы басылса
                pygame.mixer.music.pause()
                paused = True
            elif play_rect.collidepoint(mouse_pos):  # Егер "play" батырмасы басылса
                pygame.mixer.music.unpause()
                paused = False
            elif prev_rect.collidepoint(mouse_pos):  # Егер "previous" батырмасы басылса
                current_song_index = (current_song_index - 1) % len(songs)
                play_music(current_song_index)
                paused = False
            elif skip_rect.collidepoint(mouse_pos):  # Егер "skip" батырмасы басылса
                current_song_index = (current_song_index + 1) % len(songs)
                play_music(current_song_index)
                paused = False

    pygame.display.flip()  # Экранды жаңарту

pygame.quit()  # Программаны жабу
