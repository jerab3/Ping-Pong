from pygame import *
import random
##Proměnné okna
win_heigth = 500
win_width = 800

#Ball
ballMaxSpeed = 2
#Proměnné herní smyčky
isGameRunning = True
isGameFinished = False
leftWon = None

#FPS proměnné
clock = time.Clock()
FPS = 60

#CLASSY######################################
class GameSprite(sprite.Sprite):
    def __init__(self, sprite, position_x, position_y, size_x,size_y, speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite),(size_x,size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = position_x 
        self.rect.y = position_y
        self.size_x = size_x
        self.size_y = size_y

    def displaySprite(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, sprite, position_x, position_y, size_x, size_y, speed, isLeft):
        super().__init__(sprite, position_x, position_y, size_x, size_y, speed)
        self.isLeft = isLeft

    def handleMovement(self):
        keys= key.get_pressed()

        if self.isLeft:
            if keys[K_w] and self.rect.y > 0:
                self.rect.y -= self.speed
            elif keys[K_s] and self.rect.y < win_heigth - self.size_y:
                self.rect.y += self.speed
        else:
            if keys[K_UP] and self.rect.y > 0:
                self.rect.y -= self.speed
            elif keys[K_DOWN] and self.rect.y < win_heigth - self.size_y:
                self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, sprite, position_x, position_y, size_x, size_y,speed,x_speed, y_speed):
        super().__init__(sprite, position_x, position_y, size_x, size_y, speed)
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        global win_width
        global isGameFinished
        global isGameRunning
        global leftWon

        if(self.rect.y <=0):
            self.y_speed *=-1
        if(self.rect.y > win_heigth-self.size_y):
            self.y_speed *=-1
        self.rect.y += self.y_speed
        self.rect.x += self.x_speed
        
        if(self.rect.x <= 0):
            isGameFinished = True
            leftWon = False
        elif self.rect.x > win_width-self.size_x:
            isGameFinished = True
            leftWon = True
#Okno
window = display.set_mode((win_width,win_heigth))
display.set_caption("Ping Pong")

#Pozadí
backgroundImage = transform.scale(
    image.load("Assets/bg.png"),
    (win_width, win_heigth)
) 
#Inicializace

leftPlayer = Player("Assets/player.png",10,win_heigth/2-50,20,100,8,True)
rightPlayer = Player("Assets/player.png",win_width-30,win_heigth/2-50,20,100,8,False)

balls = sprite.Group()
randomX = 0
randomY = 0
while randomX == 0 or randomY == 0:
    randomX = random.randint(ballMaxSpeed*-1,ballMaxSpeed)
    randomY = random.randint(ballMaxSpeed*-1,ballMaxSpeed)

randomX*=2
randomY*=2


ball = Ball("Assets/ball.png", win_width/2-10,win_heigth/2-10,20,20,1,randomX,randomY)
balls.add(ball)
font.init()
font = font.Font(None,50)
left_win = font.render("LEFT PLAYER WON!", True, (0,255,0))
left_win_rect = left_win.get_rect(center=(win_width/2, win_heigth/2))
right_win = font.render("RIGHT PLAYER WON!", True, (0,255,0))
right_win_rect = right_win.get_rect(center=(win_width/2, win_heigth/2))
#Herní smyčka
while isGameRunning:

    #Vykreslení pozadí
    window.blit(backgroundImage,(0,0))
    
    #Event handler
    for e in event.get():
        
        if e.type == QUIT:
            isGameRunning = False

    #Pokud hra není dokončené
    if not(isGameFinished):
        #Zobrazeni
        leftPlayer.displaySprite()
        rightPlayer.displaySprite()
        balls.draw(window)
        #Pohyb
        leftPlayer.handleMovement()
        rightPlayer.handleMovement()
        balls.update()

        if sprite.collide_rect(leftPlayer, ball) or sprite.collide_rect(rightPlayer,ball):
            ball.x_speed *= -1
            chanceToMultiply = random.randint(1,2)
            if(chanceToMultiply == 1):
                randomX = 0
                randomY = 0
                while randomX == 0 or randomY == 0:
                    randomX = random.randint(ballMaxSpeed*-1,ballMaxSpeed)
                    randomY = random.randint(ballMaxSpeed*-1,ballMaxSpeed)

                randomX*=2
                randomY*=2


                ball = Ball("Assets/ball.png", win_width/2-10,win_heigth/2-10,20,20,1,randomX,randomY)
                balls.add(ball)
         

    else:
        if leftWon:
            window.blit(left_win, left_win_rect)
        else: 
            window.blit(right_win, right_win_rect)


    #FPS
    display.update()
    clock.tick(FPS)