import pygame
import random
from datetime import datetime
from datetime import timedelta

# ---------- [게임 초기화] ----------

pygame.init()

# ---------- [전역 변수] ----------

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
    pygame.K_RIGHT: 'E'
}

def draw_block(screen, color, position):
    block = pygame.Rect((position[1] * 20, position[0] * 20), (20, 20))
    pygame.draw.rect(screen, color, block)

#뱀 클래스
class Snake:
    def __init__(self):
        self.positions = [(2, 0), (1, 0), (0, 0)]  # 뱀의 위치, (2, 0)이 머리
        self.direction = ''

    def draw(self):
        for position in self.positions:
            draw_block(screen, BLUE, position)

# move 함수 : 머리의 위치와 진행 방향을 가져와 현재 꼬리 위치를 머리가 움직일 위치로 이동시킴
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

    # 뱀의 길이를 늘려 주는 grow()함수 호출
    def grow(self):
        tail_position = self.positions[-1]  #[(2,0),(1,0),(0,0)]일 경우 (0,0)을 의미함
        x, y = tail_position
        if self.direction == "N":
            # positons.append()는 추가하는 값 뒤에 추가된다.
            # positions가 [(2, 0), (1, 0), (0, 0)] 라면, positions.append((10, 20))의 결과는 [(2, 0), (1, 0), (0, 0), (10, 20)]이 된다.
            self.positions.append((y - 1, x))
        elif self.direction == 'S':
            self.positions.append((y + 1, x))
        elif self.direction == 'W':
            self.positions.append((y, x - 1))
        elif self.direction == 'E':
            self.positions.append((y, x + 1))

#사과 클래스 : 사과가 랜덤 위치에 생성된다
class Apple:
    def __init__(self, position=(5, 5)):
        self.position = position

    def draw(self):
        draw_block(screen, RED, self.position)

# ---------- [게임 무한 루프] ----------


def runGame():
    global done, last_moved_time
    # 게임 시작시 뱀과 사과를 초기화, 뱀과 사과 객체를 만듦
    snake = Snake()
    apple = Apple()

    while not done:
        clock.tick(10)
        screen.fill(GREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key in KEY_DIRECTION:  # 키보드 입력값을 이용해 뱀의 이동방향 지정
                    snake.direction = KEY_DIRECTION[event.key]

        if timedelta(seconds=0.1) <= datetime.now() - last_moved_time:  # 시간 검증을 통해 0.1초마다 뱀 이동
            snake.move()
            last_moved_time = datetime.now()

        # 뱀이 사과에 닿은 것을 확인
        if snake.positions[0] == apple.position:
            snake.grow()
            apple.position = (random.randint(0, 19), random.randint(0, 19))

        # 뱀 충돌 처리
        if snake.positions[0] in snake.positions[1:]:
            done = True



        # 뱀과 사과를 게임판에 그려줌
        snake.draw()
        apple.draw()
        pygame.display.update()


# ---------- [게임 종료] ----------

runGame()
pygame.quit()
