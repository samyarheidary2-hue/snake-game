import turtle
import random
import time
import os
import winsound

# =========================
# SNAKE
# =========================

WIDTH = 800
HEIGHT = 700

# -------------------------
# High Score
# -------------------------
SAVE_FILE = "snake_highscore.txt"

if os.path.exists(SAVE_FILE):
    try:
        with open(SAVE_FILE, "r") as f:
            HIGH_SCORE = int(f.read())
    except:
        HIGH_SCORE = 0
else:
    HIGH_SCORE = 0

# -------------------------
# Screen
# -------------------------
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.bgcolor("#111111")
screen.title("SNAKE")
screen.tracer(0)

# -------------------------
# Game Variables
# -------------------------
STATE = "MENU"

score = 0
level = 1

difficulty = "MEDIUM"

game_delay = 0.10
ai_speed = 4

paused = False

# -------------------------
# Sounds
# -------------------------
def food_sound():
    try:
        winsound.Beep(900, 80)
    except:
        pass

def level_sound():
    try:
        winsound.Beep(1200, 180)
    except:
        pass

def gameover_sound():
    try:
        winsound.Beep(400, 350)
    except:
        pass

# -------------------------
# UI Writer
# -------------------------
writer = turtle.Turtle()
writer.hideturtle()
writer.penup()
writer.color("white")

# -------------------------
# Border
# -------------------------
border = turtle.Turtle()
border.hideturtle()
border.speed(0)
border.color("gray")

border.penup()
border.goto(-350, -300)
border.pendown()

for _ in range(2):
    border.forward(700)
    border.left(90)
    border.forward(600)
    border.left(90)

# -------------------------
# Snake Head
# -------------------------
head = turtle.Turtle()
head.shape("square")
head.color("lime")
head.penup()
head.goto(0, 0)

direction = "STOP"

# -------------------------
# Snake Body
# -------------------------
segments = []

# -------------------------
# Food
# -------------------------
food = turtle.Turtle()
food.shape("circle")
food.penup()
food.color("red")

food_types = [
    ("red", 1),
    ("yellow", 1),
    ("cyan", 1),
]

food_points = 1

# -------------------------
# Enemy AI
# -------------------------
enemy = turtle.Turtle()
enemy.shape("square")
enemy.color("orange")
enemy.penup()
enemy.goto(-250, -200)

# -------------------------
# Spawn Food
# -------------------------
def spawn_food():
    global food_points

    color, points = random.choice(food_types)

    food.color(color)
    food_points = points

    x = random.randint(-320, 320)
    y = random.randint(-270, 270)

    food.goto(x, y)

# -------------------------
# Menu
# -------------------------
def draw_menu():

    writer.clear()

    writer.goto(0, 200)
    writer.write(
        "SNAKE",
        align="center",
        font=("Arial", 32, "bold")
    )

    writer.goto(0, 120)
    writer.write(
        f"HIGH SCORE : {HIGH_SCORE}",
        align="center",
        font=("Arial", 16, "normal")
    )

    writer.goto(0, 40)
    align="center",
    font=("Arial", 18, "normal")

    writer.goto(0, 0)
    align="center",
    font=("Arial", 18, "normal")

    writer.goto(0, -40)
    align="center",
    font=("Arial", 18, "normal")

    writer.goto(0, -140)
    writer.write(
        "PRESS ENTER TO START",
        align="center",
        font=("Arial", 18, "bold")
    )

# -------------------------
# Difficulty
# -------------------------
def easy():
    global difficulty
    global game_delay
    global ai_speed

    difficulty = "EASY"
    game_delay = 0.12
    ai_speed = 3

def medium():
    global difficulty
    global game_delay
    global ai_speed

    difficulty = "MEDIUM"
    game_delay = 0.10
    ai_speed = 4

def hard():
    global difficulty
    global game_delay
    global ai_speed

    difficulty = "HARD"
    game_delay = 0.07
    ai_speed = 5

# -------------------------
# Start Game
# -------------------------
def start_game():
    global STATE
    global score
    global level
    global direction

    STATE = "PLAY"

    score = 0
    level = 1

    direction = "STOP"

    head.goto(0, 0)

    for seg in segments:
        seg.goto(1000, 1000)

    segments.clear()

    enemy.goto(-250, -200)

    spawn_food()

# -------------------------
# Controls
# -------------------------
def go_up():
    global direction
    if direction != "DOWN":
        direction = "UP"

def go_down():
    global direction
    if direction != "UP":
        direction = "DOWN"

def go_left():
    global direction
    if direction != "RIGHT":
        direction = "LEFT"

def go_right():
    global direction
    if direction != "LEFT":
        direction = "RIGHT"

# -------------------------
# Start Key
# -------------------------
def enter_start():
    if STATE == "MENU":
        start_game()

# -------------------------
# Keyboard
# -------------------------
screen.listen()

screen.onkeypress(go_up, "Up")
screen.onkeypress(go_down, "Down")
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")

screen.onkeypress(easy, "1")
screen.onkeypress(medium, "2")
screen.onkeypress(hard, "3")

screen.onkeypress(enter_start, "Return")

# -------------------------
# Initial Menu
# -------------------------
draw_menu()
spawn_food()# =========================
# Move Snake
# =========================
def move():

    x = head.xcor()
    y = head.ycor()

    if direction == "UP":
        head.sety(y + 20)

    elif direction == "DOWN":
        head.sety(y - 20)

    elif direction == "LEFT":
        head.setx(x - 20)

    elif direction == "RIGHT":
        head.setx(x + 20)

# =========================
# Add Segment
# =========================
def add_segment():

    segment = turtle.Turtle()

    segment.shape("square")
    segment.color("green")
    segment.penup()

    segments.append(segment)

# =========================
# Follow Body
# =========================
def move_segments():

    for i in range(len(segments) - 1, 0, -1):

        x = segments[i - 1].xcor()
        y = segments[i - 1].ycor()

        segments[i].goto(x, y)

    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

# =========================
# AI Prediction
# =========================
def predicted_position():

    px = head.xcor()
    py = head.ycor()

    if direction == "UP":
        py += 80

    elif direction == "DOWN":
        py -= 80

    elif direction == "LEFT":
        px -= 80

    elif direction == "RIGHT":
        px += 80

    return px, py

# =========================
# Enemy AI
# =========================
def enemy_move():

    target_x, target_y = predicted_position()

    ex = enemy.xcor()
    ey = enemy.ycor()

    # ترکیب A و B
    dx = target_x - ex
    dy = target_y - ey

    if abs(dx) > 5:

        if dx > 0:
            enemy.setx(ex + ai_speed)

        else:
            enemy.setx(ex - ai_speed)

    if abs(dy) > 5:

        if dy > 0:
            enemy.sety(ey + ai_speed)

        else:
            enemy.sety(ey - ai_speed)

# =========================
# Food Collision
# =========================
def check_food():

    global score

    if head.distance(food) < 20:

        food_sound()

        score += food_points

        add_segment()

        spawn_food()

# =========================
# Level System
# =========================
def update_level():

    global level
    global game_delay
    global ai_speed

    new_level = (score // 10) + 1

    if new_level > level:

        level = new_level

        level_sound()

        # سرعت بازی بیشتر
        game_delay = max(
            0.03,
            game_delay - 0.01
        )

        # سرعت AI بیشتر
        ai_speed += 1

# =========================
# Enemy Collision
# =========================
def check_enemy_collision():

    global STATE

    # برخورد به سر
    if enemy.distance(head) < 20:

        gameover_sound()

        STATE = "GAMEOVER"

        return

    # برخورد به بدن
    for seg in segments:

        if enemy.distance(seg) < 20:

            gameover_sound()

            STATE = "GAMEOVER"

            return

# =========================
# Self Collision
# =========================
def check_self_collision():

    global STATE

    for seg in segments:

        if head.distance(seg) < 10:

            gameover_sound()

            STATE = "GAMEOVER"

            return

# =========================
# Border Collision
# =========================
def check_border():

    global STATE

    x = head.xcor()
    y = head.ycor()

    if (
        x > 340
        or x < -340
        or y > 290
        or y < -290
    ):

        gameover_sound()

        STATE = "GAMEOVER"

# =========================
# HUD
# =========================
def draw_hud():

    writer.clear()

    writer.goto(0, 320)

    writer.write(
        f"Score: {score}   Level: {level}   High Score: {HIGH_SCORE}",
        align="center",
        font=("Arial", 14, "bold")
    )# =========================
# Pause
# =========================
def toggle_pause():

    global paused

    paused = not paused

# =========================
# Restart
# =========================
def restart_game():

    global STATE

    if STATE == "GAMEOVER":
        start_game()

# =========================
# Save High Score
# =========================
def save_high_score():

    global HIGH_SCORE

    if score > HIGH_SCORE:

        HIGH_SCORE = score

        try:
            with open(SAVE_FILE, "w") as f:
                f.write(str(HIGH_SCORE))
        except:
            pass

# =========================
# Game Over Screen
# =========================
def draw_gameover():

    writer.clear()

    writer.goto(0, 120)
    writer.write(
        "GAME OVER",
        align="center",
        font=("Arial", 32, "bold")
    )

    writer.goto(0, 50)
    writer.write(
        f"Score : {score}",
        align="center",
        font=("Arial", 18, "normal")
    )

    writer.goto(0, 10)
    writer.write(
        f"Level : {level}",
        align="center",
        font=("Arial", 18, "normal")
    )

    writer.goto(0, -30)
    writer.write(
        f"High Score : {HIGH_SCORE}",
        align="center",
        font=("Arial", 18, "normal")
    )

    writer.goto(0, -120)
    writer.write(
        "Press R To Restart",
        align="center",
        font=("Arial", 18, "bold")
    )

# =========================
# Extra Keys
# =========================
screen.onkeypress(toggle_pause, "space")
screen.onkeypress(restart_game, "r")
screen.onkeypress(restart_game, "R")

# =========================
# Main Loop
# =========================
while True:

    screen.update()

    # ---------------------
    # MENU
    # ---------------------
    if STATE == "MENU":

        draw_menu()

        time.sleep(0.05)

        continue

    # ---------------------
    # GAME OVER
    # ---------------------
    if STATE == "GAMEOVER":

        save_high_score()

        draw_gameover()

        time.sleep(0.05)

        continue

    # ---------------------
    # PAUSE
    # ---------------------
    if paused:

        writer.clear()

        writer.goto(0, 0)

        writer.write(
            "PAUSED",
            align="center",
            font=("Arial", 26, "bold")
        )

        time.sleep(0.05)

        continue

    # ---------------------
    # BODY
    # ---------------------
    move_segments()

    # ---------------------
    # PLAYER
    # ---------------------
    move()

    # ---------------------
    # AI
    # ---------------------
    enemy_move()

    # ---------------------
    # COLLISIONS
    # ---------------------
    check_food()

    check_enemy_collision()

    check_self_collision()

    check_border()

    # ---------------------
    # LEVEL
    # ---------------------
    update_level()

    # ---------------------
    # HUD
    # ---------------------
    draw_hud()

    time.sleep(game_delay)