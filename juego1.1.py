import pygame
import math

Pygameinit = pygame.init()
display = pygame.display.set_mode((1200,800))
clock = pygame.time.Clock()

score = 0

class Basket():
    def __init__(self,x,y,width,height,color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x,y,width,height)
        self.rect.center = (self.x,self.y)

    def draw(self):
        self.rect = pygame.draw.rect(display,self.color,self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= 5
        if keys[pygame.K_RIGHT]:
            self.x += 5

        if keys[pygame.K_UP]:
            self.y -= 5
        if keys[pygame.K_DOWN]:
            self.y += 5

        self.rect.center = (self.x,self.y)

class Ball():
    def __init__(self,x,y,radius,color,angle):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = 5
        self.vel = pygame.math.Vector2(self.speed,self.speed)
        self.throw = False
        self.angle = angle
        self.rect = pygame.Rect(x,y,radius*2,radius*2)
        self.rect.center = (self.x,self.y)

    def draw(self):
        self.rect = pygame.draw.circle(display,self.color,(self.rect.center),self.radius)

    def bounce(self,axis):
        if axis == "x":
            self.vel.x *= -1
        if axis == "y":
            self.vel.y *= -1

    def update(self):
        self.x += self.vel.x
        self.y += self.vel.y

        self.rect.x = self.x
        self.rect.y = self.y

        if self.x + self.radius > 1200 or self.x - self.radius < 0:
            self.bounce("x")

        if self.y + self.radius > 800 or self.y - self.radius < 0:
            self.bounce("y")

        if self.throw:
            self.vel.y += 0.3

    def move(self):
        if pygame.mouse.get_pressed()[0]:
            if not self.throw:
                print("pressed")
                mouseX,mouseY = pygame.mouse.get_pos()

                self.x = mouseX
                self.y = mouseY
                self.rect.center = (self.x,self.y)

        if pygame.mouse.get_pressed()[2]:
            if not self.throw:
                print("pressed")
                mouseX,mouseY = pygame.mouse.get_pos()

                run = mouseX - self.x
                rise = mouseY - self.y
                self.angle = math.atan2(rise,run)
                self.vel.x = self.speed * math.cos(self.angle)
                self.vel.y = self.speed * math.sin(self.angle)

        if pygame.mouse.get_pressed()[0]:
            if self.throw:
                if self.x + self.radius > 1200 or self.x - self.radius < 0:
                    self.bounce("x")

                if self.y + self.radius > 800 or self.y - self.radius < 0:
                    self.bounce("y")

        if pygame.mouse.get_pressed()[1]:
            if self.throw:
                self.throw = False
                self.vel.x = 0
                self.vel.y = 0


def collision(obj1,obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.rect.colliderect(obj2.rect)

def drawScore(score):
    font = pygame.font.SysFont(":D",40)
    text = font.render("Puntuacion: " + str(score),1,(255,255,255))
    display.blit(text,(10,10))


basket = Basket(600,400,100,100,(255,0,0))
ball = Ball(600,350,20,(0,0,255),0)

run = True

while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    basket.move()
    ball.move()
    ball.update()

    if collision(basket,ball):
        score += 1

    display.fill((0,0,0))
    basket.draw()
    ball.draw()
    drawScore(score)
    pygame.display.update()

pygame.quit()