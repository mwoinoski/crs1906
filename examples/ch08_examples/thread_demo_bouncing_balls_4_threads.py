"""
thread_demo_bouncing_balls_4_balls.py - demo of multithreading.

This program has a dependency on the pygame module:
    pip install pygame
"""

import pygame
import threading
import time
import random

# Screen setup
WIDTH, HEIGHT = 500, 500
BG_COLOR = (240, 240, 255)

# Ball class
class Ball:
    def __init__(self, color, radius, speed):
        self.x = random.randint(radius, WIDTH - radius)
        self.y = random.randint(radius, HEIGHT - radius)
        self.vx = speed * random.choice([-1, 1])
        self.vy = speed * random.choice([-1, 1])
        self.color = color
        self.radius = radius
        self.lock = threading.Lock()

    def move(self):
        with self.lock:
            self.x += self.vx
            self.y += self.vy

            if self.x < self.radius or self.x > WIDTH - self.radius:
                self.vx *= -1
            if self.y < self.radius or self.y > HEIGHT - self.radius:
                self.vy *= -1

    def draw(self, surface):
        with self.lock:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 
                               self.radius)


# task for worker threads
def ball_thread(ball):
    while running:
        ball.move()
        time.sleep(0.01)


def init_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Multithreaded Bouncing Balls Demo")
    return screen


def run_game(screen, balls):
    global running
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)
        for ball in balls:
            ball.draw(screen)

        pygame.display.flip()
        clock.tick(60)


def create_balls():
    return [
        Ball(color=(255, 0, 0), radius=20, speed=3),
        Ball(color=(0, 0, 255), radius=20, speed=4),
        Ball(color=(255, 200, 0), radius=20, speed=5),
        Ball(color=(0, 255, 255), radius=20, speed=2),
    ]


def start_threads(balls):
    threads = []
    for ball in balls:
        thread = threading.Thread(target=ball_thread, args=(ball,))
        thread.start()
        threads.append(thread)
    return threads


def cleanup(threads):
    for thread in threads:
        thread.join()

    pygame.quit()


def main():
    screen = init_game()

    balls = create_balls()

    threads = start_threads(balls)

    run_game(screen, balls)

    cleanup(threads)


if __name__ == '__main__':
    clock = pygame.time.Clock()
    running = True
    main()
