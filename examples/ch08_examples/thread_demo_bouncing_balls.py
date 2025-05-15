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
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)


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


def run_game(screen, ball1, ball2):
    global running
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)

        ball1.draw(screen)
        ball2.draw(screen)

        pygame.display.flip()
        clock.tick(60)


def create_balls():
    ball1 = Ball(color=(255, 0, 0), radius=20, speed=3)
    ball2 = Ball(color=(0, 0, 255), radius=20, speed=4)
    return ball1, ball2

def start_threads(ball1, ball2):

    thread1 = threading.Thread(target=ball_thread, args=(ball1,))
    thread1.start()

    thread2 = threading.Thread(target=ball_thread, args=(ball2,))
    thread2.start()

    return thread1, thread2


def cleanup(thread1, thread2):
    thread1.join()
    thread2.join()

    pygame.quit()


def main():
    screen = init_game()

    ball1, ball2 = create_balls()

    thread1, thread2 = start_threads(ball1, ball2)

    run_game(screen, ball1, ball2)

    cleanup(thread1, thread2)

if __name__ == '__main__':
    clock = pygame.time.Clock()
    running = True

    main()
