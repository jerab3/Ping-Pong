from pygame import *

##Proměnné okna
win_heigth = 500
win_width = 800

#Proměnné herní smyčky
isGameRunning = True
isGameFinished = False

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
        #Pohyb
        leftPlayer.handleMovement()
        rightPlayer.handleMovement()




    #FPS
    display.update()
    clock.tick(FPS)