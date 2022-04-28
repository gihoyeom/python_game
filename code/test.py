import pygame  # 1. pygame 선언
import random
from datetime import datetime
from datetime import timedelta

pygame.init()  # 2. pygame 초기화

# 3. pygame에 사용되는 전역변수 선언
GRASS = (114, 183, 106)
GREEN = (172, 206, 94)
RED = (233, 67, 37)
BLUE = (88, 125, 255)
size = [500, 500]
screen = pygame.display.set_mode(size)

done = False
clock = pygame.time.Clock()
last_moved_time = datetime.now()

KEY_DIRECTION = {
    pygame.K_UP: 'N',
    pygame.K_DOWN: 'S',
    pygame.K_LEFT: 'W',
    pygame.K_RIGHT: 'E',
}


def draw_block(screen, color, position):
    block = pygame.Rect((position[1] * 20, position[0] * 20),
                        (20, 20))
    pygame.draw.rect(screen, color, block)


class Snake:
    def __init__(self):
        self.positions = [(0, 2), (0, 1), (0, 0)]  # 뱀의 위치
        self.direction = ''

    def draw(self):
        for position in self.positions:
            draw_block(screen, BLUE, position)

    def move(self):
        head_position = self.positions[0]
        y, x = head_position
        if self.direction == 'N':
            self.positions = [(y - 1, x)] + self.positions[:-1]
        elif self.direction == 'S':
            self.positions = [(y + 1, x)] + self.positions[:-1]
        elif self.direction == 'W':
            self.positions = [(y, x - 1)] + self.positions[:-1]
        elif self.direction == 'E':
            self.positions = [(y, x + 1)] + self.positions[:-1]

    def grow(self):
        tail_position = self.positions[-1]
        y, x = tail_position
        if self.direction == 'N':
            self.positions.append((y - 1, x))
        elif self.direction == 'S':
            self.positions.append((y + 1, x))
        elif self.direction == 'W':
            self.positions.append((y, x - 1))
        elif self.direction == 'C':
            self.positions.append((y, x + 1))


class Apple:
    def __init__(self, position=(5, 5)):
        self.position = position

    def draw(self):
        draw_block(screen, RED, self.position)


# 4. pygame 무한루프
def runGame():
    global done, last_moved_time
    # 게임 시작 시, 뱀과 사과를 초기화
    snake = Snake()
    apple = Apple()

    while not done:
        clock.tick(10)
        screen.fill(GREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key in KEY_DIRECTION:
                    snake.direction = KEY_DIRECTION[event.key]

        if timedelta(seconds=0.1) <= datetime.now() - last_moved_time:
            snake.move()
            last_moved_time = datetime.now()

        if snake.positions[0] == apple.position:
            snake.grow()
            apple.position = (random.randint(0, 19), random.randint(0, 19))

        if snake.positions[0] in snake.positions[1:]:
            done = True

        snake.draw()
        apple.draw()
        pygame.display.update()


runGame()
pygame.quit()