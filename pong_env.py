import pygame
import random
import numpy as np

WIDTH, HEIGHT = 400, 1000
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
RADIUS = 5

class PongEnv:
    def __init__(self):
        pygame.init()
        self.wn = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong AI")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.ball_x = random.randint(WIDTH//2 - 50, WIDTH//2 + 50)
        self.ball_y = random.randint(HEIGHT//4 - 50, HEIGHT//4 + 50)
        self.paddle_x, self.paddle_y = 170, 900
        self.paddle_w, self.paddle_h = 60, 15
        speed = random.uniform(3, 6)
        if random.choice([True, False]):
            speed *= -1
        self.ball_xvel, self.ball_yvel = speed, abs(speed)
        self.wall_x, self.wall_y, self.wall_w, self.wall_h = 0, 200, 600, 15
        self.wall_vel = 0.08
        self.done = False
        return self.get_state()

    def get_state(self):
        return np.array([
            self.ball_x / WIDTH,
            self.ball_y / HEIGHT,
            self.ball_xvel / 10.0,
            self.ball_yvel / 10.0,
            self.paddle_x / WIDTH,
            self.wall_y / HEIGHT,
            self.wall_vel
        ], dtype=np.float32)

    def step(self, action):
        reward = 0
        if action == 1:
            self.paddle_x -= 3
        elif action == 2:
            self.paddle_x += 3

        self.paddle_x = max(0, min(WIDTH - self.paddle_w, self.paddle_x))
        self.ball_x += self.ball_xvel
        self.ball_y += self.ball_yvel
        self.wall_y += self.wall_vel

        if self.ball_x <= 0 + RADIUS or self.ball_x >= WIDTH - RADIUS:
            self.ball_xvel *= -1

        if self.paddle_y - self.paddle_h <= self.ball_y <= self.paddle_y and self.ball_yvel > 0:
            if self.paddle_x <= self.ball_x <= self.paddle_x + self.paddle_w:
                self.ball_y = self.paddle_y - RADIUS
                self.ball_yvel *= -1
                reward = 1

        if self.ball_y <= self.wall_y + self.wall_h and self.ball_yvel < 0:
            self.ball_y = self.wall_y + self.wall_h
            self.ball_yvel *= -1
            reward = 1
            self.ball_xvel *= 1.01
            self.ball_yvel *= 1.01
            self.wall_vel *= 0.99

        if self.ball_y >= HEIGHT:
            self.done = True
            reward = -1

        return self.get_state(), reward, self.done
