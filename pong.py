# ==============================
# Shahzeb Pong Game (Professional)
# ==============================

import pygame
import random
import math
import os
import sys

# ---------------- INITIALIZE ----------------
pygame.init()
pygame.mixer.init()

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 800, 600
FPS = 60
WIN_SCORE = 5

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 60, 60)
GRAY = (150, 150, 150)

# Paddle
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_SPEED = 6

# Ball
BALL_SIZE = 20
BALL_SPEED = 6

# Music ducking
MUSIC_VOL = 0.4
DUCK_VOLUME = 0.05
DUCK_MS = 300  # milliseconds to keep music ducked on hit


# Fonts
FONT_BIG = pygame.font.Font(None, 48)
FONT_MED = pygame.font.Font(None, 32)
FONT_SMALL = pygame.font.Font(None, 24)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shahzeb Pong")
clock = pygame.time.Clock()

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_DIR = os.path.join(BASE_DIR, "sounds")

# ---------------- SAFE SOUND LOADING ----------------
def load_sound(filename):
    try:
        return pygame.mixer.Sound(os.path.join(SOUND_DIR, filename))
    except pygame.error:
        return None

# Load sounds (MP3)
sound_hit = load_sound("hit.mp3")
sound_score = load_sound("success.mp3")
sound_gameover = load_sound("gameover.mp3")

# Background music
try:
    pygame.mixer.music.load(os.path.join(SOUND_DIR, "bg_music.mp3"))
    pygame.mixer.music.set_volume(MUSIC_VOL)
except pygame.error:
    pass

# ---------------- GAME OBJECTS ----------------
left_paddle = pygame.Rect(40, HEIGHT // 2 - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 60, HEIGHT // 2 - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)

ball_dx = 0
ball_dy = 0

score_left = 0
score_right = 0

# Game states
game_started = False
paused = False
game_over = False
muted = False
AI_MODE = True

# music duck timer (pygame time in ms)
music_duck_end = 0


# ---------------- FUNCTIONS ----------------
def reset_ball():
    global ball_dx, ball_dy
    ball.center = (WIDTH // 2, HEIGHT // 2)
    angle = random.uniform(-math.pi / 4, math.pi / 4)
    direction = random.choice([-1, 1])
    ball_dx = direction * BALL_SPEED * math.cos(angle)
    ball_dy = BALL_SPEED * math.sin(angle)

def draw_center_line():
    for y in range(0, HEIGHT, 30):
        pygame.draw.rect(screen, GRAY, (WIDTH // 2 - 2, y, 4, 15))

def draw_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def paddle_collision(paddle):
    global ball_dx, ball_dy
    global music_duck_end
    offset = (ball.centery - paddle.centery) / (PADDLE_HEIGHT / 2)
    angle = offset * (math.pi / 3)
    ball_dx *= -1
    ball_dy = BALL_SPEED * math.sin(angle)
    if sound_hit and not muted:
        sound_hit.play()
        # Duck background music briefly so hit sound is prominent
        music_duck_end = pygame.time.get_ticks() + DUCK_MS

def toggle_mute():
    global muted
    muted = not muted
    if muted:
        pygame.mixer.music.set_volume(0)
    else:
        pygame.mixer.music.set_volume(0.4)

# ---------------- GAME LOOP ----------------
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    # -------- EVENTS --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            # Mode selection: 1 = AI, 2 = Two Players (only before starting)
            if not game_started and event.key == pygame.K_1:
                AI_MODE = True

            if not game_started and event.key == pygame.K_2:
                AI_MODE = False

            if event.key == pygame.K_SPACE and not game_started:
                reset_ball()
                game_started = True
                pygame.mixer.music.play(-1)

            if event.key == pygame.K_p:
                paused = not paused
                if paused:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

            if event.key == pygame.K_r:
                score_left = score_right = 0
                game_started = False
                game_over = False
                ball_dx = ball_dy = 0
                pygame.mixer.music.stop()

            if event.key == pygame.K_m:
                toggle_mute()

    # -------- INPUT --------
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PADDLE_SPEED

    # Right paddle control: AI or player 2
    if AI_MODE:
        if ball_dx > 0:
            if right_paddle.centery < ball.centery:
                right_paddle.y += PADDLE_SPEED - 2
            elif right_paddle.centery > ball.centery:
                right_paddle.y -= PADDLE_SPEED - 2
    else:
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += PADDLE_SPEED

    # -------- GAME LOGIC --------
    if game_started and not paused and not game_over:
        ball.x += ball_dx
        ball.y += ball_dy

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_dy *= -1

        if ball.colliderect(left_paddle):
            paddle_collision(left_paddle)

        if ball.colliderect(right_paddle):
            paddle_collision(right_paddle)

        if ball.left <= 0:
            score_right += 1
            if sound_score and not muted:
                sound_score.play()
            reset_ball()

        if ball.right >= WIDTH:
            score_left += 1
            if sound_score and not muted:
                sound_score.play()
            reset_ball()

        if score_left == WIN_SCORE or score_right == WIN_SCORE:
            game_over = True
            pygame.mixer.music.stop()
            if sound_gameover and not muted:
                sound_gameover.play()

    # -------- DRAW --------
    draw_center_line()
    pygame.draw.rect(screen, GREEN, left_paddle)
    pygame.draw.rect(screen, GREEN, right_paddle)
    pygame.draw.ellipse(screen, RED, ball)

    draw_text(str(score_left), FONT_BIG, WHITE, WIDTH // 2 - 80, 20)
    draw_text(str(score_right), FONT_BIG, WHITE, WIDTH // 2 + 50, 20)

    draw_text("Developed by Shahzeb", FONT_SMALL, GRAY, 10, HEIGHT - 28)

    if not game_started:
        draw_text("Press SPACE to Start", FONT_MED, WHITE, 270, 240)
        draw_text("Press 1: Play vs AI    Press 2: Two Players", FONT_SMALL, WHITE, 230, 280)
        mode_name = "AI" if AI_MODE else "Two-Player"
        draw_text(f"Selected Mode: {mode_name}", FONT_SMALL, GRAY, 320, 310)

    if paused:
        draw_text("PAUSED", FONT_BIG, WHITE, 340, 260)

    if game_over:
        if AI_MODE:
            winner = "You Win!" if score_left > score_right else "AI Wins!"
        else:
            winner = "Player 1 Wins!" if score_left > score_right else "Player 2 Wins!"
        draw_text(winner, FONT_BIG, WHITE, 320, 230)
        draw_text("Press R to Restart", FONT_SMALL, WHITE, 330, 280)

    draw_text("M: Mute | P: Pause | R: Restart | ESC: Quit",
              FONT_SMALL, GRAY, 170, HEIGHT - 50)

    pygame.display.flip()

pygame.quit()
sys.exit()
