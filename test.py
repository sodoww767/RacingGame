import pygame
import random
import sys

# Ініціалізація Pygame
pygame.init()

pygame.mixer.init()
pygame.mixer.music.load('12.mp3')
pygame.mixer.music.play(loops=-1)
crash_sound = pygame.mixer.Sound("2.mp3")

# Параметри екрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game")

background = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH, HEIGHT))

# Кольори
WHITE = (255, 255, 255)
BLACK = (66, 135, 245)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# FPS і годинник
FPS = 60
clock = pygame.time.Clock()

# Завантаження автомобілів
player_car = pygame.image.load("player_car.png")
player_car = pygame.transform.scale(player_car, (110, 90))

# Завантажуємо 5 різних машин для ворогів
enemy_cars = [
    pygame.transform.scale(pygame.image.load("enemy_car_1.png"), (170, 100)),
    pygame.transform.scale(pygame.image.load("enemy_car_2.png"), (130, 110)),
    pygame.transform.scale(pygame.image.load("enemy_car_3.png"), (80, 100)),
    pygame.transform.scale(pygame.image.load("enemy_car_4.png"), (80, 90)),
    pygame.transform.scale(pygame.image.load("enemy_car_5.png"), (130, 150))
]

# Початкові позиції
player_x = WIDTH // 2 - 25
player_y = HEIGHT - 120

# Швидкість
player_speed = 8
enemy_speed = 5
background_speed = 4  # Швидкість скролінгу фону

# Шрифт для відображення результатів
font = pygame.font.Font("Oi-Regular.ttf", 40)  # Збільшено до 50
score = 0
lives = 3  # Початково 3 життя

# Функція для перевірки, чи не накладаються машини
def check_collision_between_enemies(enemy_x, enemy_y, enemies, min_distance=150):
    for other_x, other_y, _, _ in enemies:
        distance = ((enemy_x - other_x) ** 2 + (enemy_y - other_y) ** 2) ** 0.5
        if distance < min_distance:  # Якщо відстань менша, ніж мінімальна, то машини занадто близько
            return True
    return False

# Функція для генерації ворогів
def generate_enemies():
    enemies = []
    for _ in range(8):
        while True:
            # Визначаємо випадкову сторону для ворога
            enemy_x = random.randint(50, WIDTH - 100)
            enemy_y = random.randint(-600, -100)
            side = "left" if enemy_x < WIDTH // 2 else "right"  # Ліва або права частина
            # Якщо ворог на лівій стороні, вибираємо тільки дві машини (enemy_car_1, enemy_car_2)
            car_type = random.randint(0, 4)  # Для будь-якої машини (з 0 по 4)
            # Перевіряємо, чи не зіштовхуються нові машини з іншими
            if not check_collision_between_enemies(enemy_x, enemy_y, enemies):
                enemies.append([enemy_x, enemy_y, side, car_type])
                break  # Якщо машина не накладається на інші, додаємо її
    return enemies

# Початкові вороги
enemies = generate_enemies()

def check_collision(px, py, enemies):
    """Перевірка на зіткнення"""
    player_rect = pygame.Rect(px, py, 50, 100)
    for enemy_x, enemy_y, _, _ in enemies:
        enemy_rect = pygame.Rect(enemy_x, enemy_y, 50, 100)
        if player_rect.colliderect(enemy_rect):
            return True
    return False

# Головний ігровий цикл
running = True
game_over = False
you_win = False

# Позиція фону для скролінгу
background_y1 = 0
background_y2 = -HEIGHT  # Другий екземпляр фону для нескінченності

while running:
    screen.fill(WHITE)

    # Рух фону для скролінгу
    background_y1 += background_speed
    background_y2 += background_speed

    # Якщо один з фонів вийшов за межі екрану, переміщаємо його назад
    if background_y1 >= HEIGHT:
        background_y1 = -HEIGHT
    if background_y2 >= HEIGHT:
        background_y2 = -HEIGHT

    # Малюємо фони
    screen.blit(background, (0, background_y1))
    screen.blit(background, (0, background_y2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over and not you_win:
        # Управління гравцем
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < HEIGHT - 50:
            player_y += player_speed

        # Рух ворогів
        for enemy in enemies:
            enemy_x, enemy_y, side, car_type = enemy

            if side == "left":
                # Вороги з лівої частини екрана рухаються вниз
                enemy[1] += enemy_speed
                if enemy[1] > HEIGHT:  # Якщо ворог вийшов за межі екрану, то знову з'являється
                    enemy[1] = random.randint(-600, -100)
                    enemy[0] = random.randint(50, WIDTH // 2 - 100)
                    score += 1
            elif side == "right":
                # Вороги з правої частини екрана рухаються вниз
                enemy[1] += enemy_speed
                if enemy[1] > HEIGHT:  # Якщо ворог вийшов за межі екрану, то знову з'являється
                    enemy[1] = random.randint(-600, -100)
                    enemy[0] = random.randint(WIDTH // 2 + 50, WIDTH - 100)
                    score += 1

        # Перевірка на зіткнення
        if check_collision(player_x, player_y, enemies):
            crash_sound.play()
            lives -= 1  # Втрачаємо одне життя
            if lives <= 0:
                game_over = True
            else:
                # Відновлення автомобіля після зіткнення
                player_x = WIDTH // 2 - 25
                player_y = HEIGHT - 120
                enemies = generate_enemies()  # Очищаємо перешкоди і генеруємо нові
                pygame.time.wait(500)  # Коротка пауза перед наступним зіткненням

        # Перевірка на перемогу
        if score >= 50:
            you_win = True

        # Малювання об'єктів
        screen.blit(player_car, (player_x, player_y))
        for enemy_x, enemy_y, _, car_type in enemies:
            screen.blit(enemy_cars[car_type], (enemy_x, enemy_y))  # Малюємо машину ворога

        # Відображення рахунку та життів
        score_text = font.render(f"Рахунок: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        lives_text = font.render(f"Життя: {lives}", True, RED)
        screen.blit(lives_text, (450, 10))

    elif game_over:
        # Якщо гра закінчена
        game_over_text = font.render("Гра Закінчилась!", True, RED)
        screen.blit(game_over_text, (90, HEIGHT // 2 - 30))  # Центрування тексту

        restart_text = font.render("R - перезапустити", True, BLACK)
        screen.blit(restart_text, (50, HEIGHT // 2 + 30))

        quit_text = font.render("Q - вийти", True, BLACK)
        screen.blit(quit_text, (WIDTH // 2 - 160, 400))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Перезапуск гри
            player_x = WIDTH // 2 - 25
            player_y = HEIGHT - 120
            enemies = generate_enemies()
            score = 0
            lives = 3  # Відновлення життів
            game_over = False
            you_win = False
        elif keys[pygame.K_q]:
            # Вихід з гри
            pygame.quit()
            sys.exit()

    elif you_win:
        # Якщо гравець виграв
        win_text = font.render("Ти Виграв!", True, BLUE)
        screen.blit(win_text, (200, HEIGHT // 2 - 30))  # Центрування тексту

        restart_text = font.render("R - перезапустити", True, BLACK)
        screen.blit(restart_text, (45, HEIGHT // 2 + 30))

        quit_text = font.render("Q - вийти", True, BLACK)
        screen.blit(quit_text, (WIDTH // 2 - 160, 400))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Перезапуск гри
            player_x = WIDTH // 2 - 25
            player_y = HEIGHT - 120
            enemies = generate_enemies()
            score = 0
            lives = 3  # Відновлення життів
            game_over = False
            you_win = False
        elif keys[pygame.K_q]:
            # Вихід з гри
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(FPS)
