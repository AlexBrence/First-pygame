import pygame
pygame.init()

win = pygame.display.set_mode((500, 480))  # width, height 

pygame.display.set_caption("First Game")
font = pygame.font.SysFont("comicsans", 30, True)

walkRight = [pygame.image.load('media/R1.png'), pygame.image.load('media/R2.png'), pygame.image.load('media/R3.png'), pygame.image.load('media/R4.png'), pygame.image.load('media/R5.png'), pygame.image.load('media/R6.png'), pygame.image.load('media/R7.png'), pygame.image.load('media/R8.png'), pygame.image.load('media/R9.png')]
walkLeft = [pygame.image.load('media/L1.png'), pygame.image.load('media/L2.png'), pygame.image.load('media/L3.png'), pygame.image.load('media/L4.png'), pygame.image.load('media/L5.png'), pygame.image.load('media/L6.png'), pygame.image.load('media/L7.png'), pygame.image.load('media/L8.png'), pygame.image.load('media/L9.png')]
bg = pygame.image.load('media/bg.jpg')
char = pygame.image.load('media/standing.png')

clock = pygame.time.Clock()


""" CLASSES """

class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 20, self.y, 28, 60)


    def draw(self, win):
        if self.walkCount + 1 >= 27:    # Because we got 9 sprites and each one of them will be shown in 3 frames. You would run into index error otherwise.
            self.walkCount = 0

        if not (self.standing):        
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))

            else:
                win.blit(walkLeft[0], (self.x, self.y))

        self.hitbox = (self.x + 18, self.y + 12, 26, 50)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
        



class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)



class Enemy(object):
    walkRight = [pygame.image.load('media/R1E.png'), pygame.image.load('media/R2E.png'), pygame.image.load('media/R3E.png'), pygame.image.load('media/R4E.png'), pygame.image.load('media/R5E.png'), pygame.image.load('media/R6E.png'), pygame.image.load('media/R7E.png'), pygame.image.load('media/R8E.png'), pygame.image.load('media/R9E.png'), pygame.image.load('media/R10E.png'), pygame.image.load('media/R11E.png')]
    walkLeft = [pygame.image.load('media/L1E.png'), pygame.image.load('media/L2E.png'), pygame.image.load('media/L3E.png'), pygame.image.load('media/L4E.png'), pygame.image.load('media/L5E.png'), pygame.image.load('media/L6E.png'), pygame.image.load('media/L7E.png'), pygame.image.load('media/L8E.png'), pygame.image.load('media/L9E.png'), pygame.image.load('media/L10E.png'), pygame.image.load('media/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]    # This will define where enemy starts and finishes
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 20, self.y, 28, 60) 
        self.health = 10
        self.visible = True

    
    def move(self):
        if self.vel > 0:    # If we are moving to the right
            if self.x < self.path[1] + self.vel:    # If we have not reached the furthest right point on our path 
                self.x += self.vel
            else:   # Change the direction and move back the other way
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0

        else:   # If we are moving to the right
            if self.x > self.path[0] - self.vel:    # If we have not reached the furthest left point on our path
                self.x += self.vel
            else:   # Change direction
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0

        if self.visible: 
            self.hitbox = (self.x + 25, self.y, 20, 52) 

        else:
            self.hitbox = (0, 0, 0, 0) 

        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)



    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:    # Since we have 11 images for each animation our upper bound is 33. We will show each image for 3 frames - 3*11 = 33.
                self.walkCount = 0

            if self.vel > 0:    # If we are moving to the right we will display walkRight images
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))  
                self.walkCount += 1

            else:               # Otherwise we will display walkLeft images
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.x + 2, 32, 57)


    

    def hit(self):
        global score
        score += 1

        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False





def keyPressed():
    global shootLoop
    global run

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5:
            bullets.append(Projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (166,77,255), facing))
        
        shootLoop = 1


    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False

    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False

    else:
        man.standing = True
        man.walkCount = 0

    if not (man.isJump):

        if keys[pygame.K_UP]:
            man.isJump = True
            man.walkCount = 0

    else:
        if man.jumpCount >= -10:
            neg = 1

            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg     # ** is squared
            man.jumpCount -= 1

        else:
            man.isJump = False
            man.jumpCount = 10




""" FUNCTIONS """

def shootingLoop():
    global shootLoop

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0



def shooting():
    for bullet in bullets:
        goblin_got_hit = (bullet.x > goblin.x and bullet.x < goblin.x + goblin.width) and (bullet.y > goblin.y and bullet.y < goblin.y + goblin.height)

        if goblin_got_hit and goblin.visible: 
                goblin.hit()
                bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel

        else:
            bullets.pop(bullets.index(bullet))    # We don't need to have a bullet that is off the screen so we are finding it and deleting it.



def redrawGameWindow():
    win.blit(bg, (0, 0))

    man.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    goblin.draw(win)
    text = font.render("Score: " + str(score), 1, (0, 0, 0))

    pygame.display.update()







# Just some variables for the game
score = 0
man = Player(200, 410, 64, 64)
bullets = []
shootLoop = 0
goblin = Enemy(100, 420, 64, 64, 300)
run = True

""" MAINLOOP """
while run:
    clock.tick(27)
    
    shootingLoop()
    shooting()
    keyPressed()
    

    redrawGameWindow()
            

pygame.quit()