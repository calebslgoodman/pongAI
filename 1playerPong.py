import pygame
import random
pygame.init()

WIDTH, HEIGHT = 400, 1000
wn = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Single Player Pong")
clock = pygame.time.Clock()



white = (255,255,255)
black = (0,0,0)

radius = 5

ball_x, ball_y = random.randint(WIDTH // 2 - 50, WIDTH // 2 + 50), random.randint(HEIGHT // 4 - 50, HEIGHT // 4 + 50)
paddle_x, paddle_y, paddle_width, paddle_height = 170, 900, 60, 15
run = True
wall_x, wall_y, wall_width, wall_height = 0, 200, 600, 15
wall_velocity = 0.08
speed = random.uniform(3,6)
if random.choice([True, False]):
        speed *= -1
ball_xvel, ball_yvel = speed, abs(speed)

paddle_vel = 0

score = 0

while run:
    wn.fill(black)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_LEFT:
                paddle_vel = -3
            if i.key == pygame.K_RIGHT:
                paddle_vel = 3
        if i.type == pygame.KEYUP:
            paddle_vel = 0
    
    if ball_x <= 0 + radius or ball_x >= WIDTH - radius:
        ball_xvel *= -1





    ball_x += ball_xvel
    ball_y += ball_yvel
    wall_y += wall_velocity
    paddle_x += paddle_vel

    paddle_x = max(0, min(WIDTH - paddle_width, paddle_x))

    #collisions
    if paddle_y - paddle_height <= ball_y <= paddle_y and ball_yvel > 0:
        if paddle_x <= ball_x <= paddle_x + paddle_width:
            ball_y = paddle_y - radius
            ball_yvel *= -1
    
    if ball_y <= wall_y + wall_height and ball_yvel < 0:
        ball_y = wall_y + wall_height
        ball_yvel *= -1
        score += 1
        ball_xvel *= 1.01
        ball_yvel *= 1.01
        wall_velocity *= 0.99

    if ball_y >= 1000:
        run = False
    pygame.draw.circle(wn, white, (ball_x, ball_y), radius)
    pygame.draw.rect(wn, white, pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height))
    pygame.draw.rect(wn, white, pygame.Rect(wall_x, wall_y, wall_width, wall_height))
    pygame.display.update()
    clock.tick(60)

print(score)