import pygame
from enum import Enum

pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont(None, 25, bold=True)

pygame.mixer.music.load('music.mp3')
pygame.mixer.music.set_volume(2)
pygame.mixer.music.play(-1)

boom = pygame.mixer.Sound('boom.wav')

def message(msg, color, cords):
    txt = font.render(msg, True, color)
    screen.blit(txt, cords)


def GameOver(msg):
    screen.fill((255, 255, 255))
    message(msg, (0, 0, 0), [400, 300])
    message('Press esc to exit', (0, 0, 0), [400, 500])
    pygame.display.flip()

class Bull():
    def __init__(self, x, y, r, color, facing, target, timing):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.facing = facing
        self.vel = 8
        self.target = target
        self.timing = timing

    def life(self):
        if ticks - self.timing > 5 * FPS:
            return False
        return True

    def getTarget(self):
        if self.target == 1:
            #print(self.x, self.y, tank1.x, tank1.y)
            if abs(self.x - (tank1.x + tank1.width // 2)) <= 20 and abs(self.y - (tank1.y + tank1.width // 2)) <= 20:
                tank1.health -= 1
                return True
            return False
        else:
            #print(self.x, self.y, tank2.x, tank2.y)
            if abs(self.x - (tank2.x + tank1.width // 2)) <= 20 and abs(self.y - (tank1.y + tank2.width // 2)) <= 20:
                tank2.health -= 1
                return True
            return False


    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def movement(self):
        if self.facing == Direction.LEFT:
            self.x -= self.vel
        if self.facing == Direction.RIGHT:
            self.x += self.vel
        if self.facing == Direction.UP:
            self.y -= self.vel
        if self.facing == Direction.DOWN:
            self.y += self.vel
        if self.x + self.r <= 0:
            self.x = 800
        elif self.x >= 800:
            self.x = 0
        if self.y + self.r <= 0:
            self.y = 600
        elif self.y >= 600:
            self.y = 0
        self.draw()


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Tank:

    def __init__(self, x, y, speed, color, health, lastShot, delay=60, d_right=pygame.K_RIGHT, d_left=pygame.K_LEFT,
                 d_up=pygame.K_UP, d_down=pygame.K_DOWN):
        self.x = abs(x % 800)
        self.y = abs(y % 600)
        self.speed = speed
        self.color = color
        self.width = 40
        self.direction = Direction.RIGHT
        self.health = health
        self.lastShot = lastShot
        self.key = {d_right: Direction.RIGHT, d_left: Direction.LEFT, d_up: Direction.UP, d_down: Direction.DOWN}
        self.delay = delay

    def shoot(self, target):
        if ticks - self.lastShot < self.delay:
            return
        boom.play()
        bult = Bull(self.x, self.y + self.width // 2, 7, (255, 0, 0), self.direction, target, ticks)
        bullets.append(bult)
        self.lastShot = ticks

    def draw(self):
        tank_c = (self.x + int(self.width / 2), self.y + int(self.width / 2))
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width), 2)
        pygame.draw.circle(screen, self.color, tank_c, int(self.width / 2))

        if self.direction == Direction.RIGHT:
            pygame.draw.line(screen, self.color, tank_c,
                             (self.x + self.width + int(self.width / 2), self.y + int(self.width / 2)), 4)

        if self.direction == Direction.LEFT:
            pygame.draw.line(screen, self.color, tank_c, (self.x - int(self.width / 2), self.y + int(self.width / 2)),
                             4)

        if self.direction == Direction.UP:
            pygame.draw.line(screen, self.color, tank_c, (self.x + int(self.width / 2), self.y - int(self.width / 2)),
                             4)

        if self.direction == Direction.DOWN:
            pygame.draw.line(screen, self.color, tank_c,
                             (self.x + int(self.width / 2), self.y + self.width + int(self.width / 2)), 4)

    def change_direction(self, direction):
        self.direction = direction

    def move(self):
        if self.direction == Direction.LEFT:
            self.x -= self.speed
        if self.direction == Direction.RIGHT:
            self.x += self.speed
        if self.direction == Direction.UP:
            self.y -= self.speed
        if self.direction == Direction.DOWN:
            self.y += self.speed
        if self.x + self.width <= 0:
            self.x = 800
        elif self.x >= 800:
            self.x = 0
        if self.y + self.width <= 0:
            self.y = 600
        elif self.y >= 600:
            self.y = 0
        self.draw()


mainloop = True
tank1 = Tank(300, 300, 5, (255, 123, 100), 3, -500)
tank2 = Tank(300, 300, 5, (100, 230, 40), 3, -500, 60, pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)
FPS = 30
bullets = []
clock = pygame.time.Clock()
millis = clock.tick(FPS)
ticks = 0
over = ''

while mainloop:
    while over:
        GameOver(over)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
    # print(ticks, len(bullets))
    ind = 0
    l = []
    millis = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
            if event.key == pygame.K_SPACE:
                tank2.shoot(1)
            if event.key == pygame.K_RETURN:
                tank1.shoot(2)
            if event.key in tank1.key.keys():
                tank1.change_direction(tank1.key[event.key])
            if event.key in tank2.key.keys():
                tank2.change_direction(tank2.key[event.key])

    screen.fill((0, 0, 0))
    for bullet in bullets:
        bullet.movement()
        if bullet.getTarget() or not bullet.life():
            #print('Hello')
            l.append(ind)

    for current in l:
        bullets.pop(ind)
    message(str(tank1.health), (255, 255, 255), [20, 20])
    message(str(tank2.health), (255, 255, 255), [700, 20])
    tank1.move()
    tank2.move()
    pygame.display.flip()
    ticks += 1
    if tank1.health == 0:
        over = 'tank2 win'
    elif tank2.health == 0:
        over = 'tank1 win'

pygame.quit()