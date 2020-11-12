#Author: Michael Bradshaw
#Date: Start: 2020/08/05
#File Name: New_Worlds.py
#Desription: A Game that has a art sytle to teraria, and is a space, world game.
#place single pixel with pygame.Surface.set_at().

import pygame
import random #import necessary librarys for the program.
import math 
import time

#Classes:d

class SpriteManager():    
    def __init__(self, tag, image, x, y):
        self.tag = tag
        self.x = x
        self.y = y
        if self.tag == 'Background':
            self.image = pygame.image.load(image).convert()#optimes the background that have fill interiors.
        elif image != 'Sprites/Grass.png' or image != 'Sprites/Dirt.png':
            self.image = pygame.image.load(image)
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        else:
            if self.tag == 'Grass':
                self.image = blocksAvailable[0]#sets the image from the location in the users computer.
            elif self.tag == 'Dirt':
                self.image = blocksAvailable[1]
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.rect = self.image.get_rect(topleft=(self.x, self.y)) #sets the rect of the player with x,y,w,h

    def displayImage(self): #Displays the image at the positons provided.
        self.rect = self.image.get_rect(topleft = (self.x, self.y)) #gest tge 
        ds.blit(self.image, (self.x, self.y))
    
    def pixelColldier(self, sprite1, sprite2):
        if pygame.sprite.collide_mask(sprite1, sprite2): #Perfect Collidier on pixel level
            return True
        else:
            return False

    def collidercheck(self, sprite_1, sprite_2):#checks to see if the two sprites collider with each other 

        # Uses the rectangle around the sprite to determine if they collide.
        if pygame.Rect.colliderect(sprite_1.rect, sprite_2.rect):#if the sprites collide it will return true or return false if no collion.
            return True
        return False

class Tools(SpriteManager):
    def __init__(self, spriteName, imageID, x, y, damage, derablity):
        super().__init__(spriteName, imageID, x, y)
        self.damage = damage #sets the tools info.
        self.derablity = derablity

class Player(SpriteManager): #enhartes from the spritemanger
    def __init__(self, spriteName, imageID, x, y, hunger = 100, health = 100):
        super().__init__(spriteName, imageID, x, y) #sends the sprite conditions to the enharaded class.
        self.health = health
        self.hunger = hunger
        self.allTools = []
        self.items = [] #set all things for the player.
        self.isJumping = False
        self.falling = False
        self.maxHeightForJump = 350
        self.counterOfDept = 150
        self.howManyUp = 0

    def jumpAndGravity(self, isCollidingWithGround, jumpLimit, initialLowHeight): #Need timer for when this instance goes....
        if self.isJumping:
            if initialLowHeight > blocksCreated[-1].y:
                if yJumpCheck(image):
                    blockMover(False,False, True, False)
                    self.y -= 2
                    self.howManyUp += 2
                    if self.howManyUp == 150:
                        self.isJumping = False
                        self.falling = True #makes the player jump. by looking at loops and stuff.
                else:
                    self.isJumping = False
                    self.falling = True #makes the player jump. by looking at loops and stuff.
            elif initialLowHeight == blocksCreated[-1].y:
                self.y -= 2
                if self.y <= self.maxHeightForJump or self.y >= 700 or not yJumpCheck(image):
                    self.isJumping = False
                    self.falling = True #makes the player jump. by looking at loops and stuff.

        if self.falling or isCollidingWithGround == False and self.y >= 500 and self.y <= 640 and not self.isJumping :#The player falls when no block is under.
            if isCollidingWithGround and yJumpCheck(image):
                self.falling = False
            else:#this is the problem
                if self.y <= 625 or blocksCreated[-1].y >= 688 and self.y <= 625 and isCollidingWithGround == False:
                    self.y += 2
                if self.y >= 625 and blocksCreated[-1].y >= 689 and isCollidingWithGround == False: 
                    blockMover(False,False, False, True)
                elif self.y >= 625 and isCollidingWithGround == False:
                    print('YOU DIED!')
                    return True
        if dieCheck == False:
            return False

    def controlPlayer(self): #Player Controls
        keys = pygame.key.get_pressed() #gets all keys pressed.
        if keys[pygame.K_d] and not blockAndPlayerColliderCheck(image) and foreheadCheck(image, True):
            if self.x <= 1000 or blocksCreated[-1].x <= 1250 and self.x <= 1220:
                self.x += 1
            if self.x >= 1000 and blocksCreated[-1].x >= 1250:
                blockMover(True)
        if keys[pygame.K_a] and not blockAndPlayerColliderCheck(image) and foreheadCheck(image, False, True):
            if self.x >= 280 or blocksCreated[0].x >= -10 and self.x >= 0:
                self.x -= 1 
            if self.x <= 280 and blocksCreated[0].x <= -10: #moves the player in a ddddddset x and y, camera follows.
                blockMover(False,True)      
        if keys[pygame.K_SPACE] and blockCollided: #and not self.falling:
            self.isJumping = True
            self.howManyUp = 0

class Blocks(SpriteManager):

    def __init__(self, spriteName, imageID, x, y, damage = 0, derablity = 0):
        super().__init__(spriteName, imageID, x, y) #Send info to the class that manages sprites.
        self.damage = damage
        self.derablity = derablity #sets damage and deribity to the blocks

#Functions:

def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #checks for the events that pygame get through the program.
            return False

        if event.type == pygame.KEYDOWN: #ends program if conditions are true.
            if event.key == pygame.K_q:
                return False
    return True
    
def generateBlocks():
    currentx = -150
    currenty = 564
    xDistance = 32 #sets the conditons
    yDistance = 32
    howDeep = 0
    lengthOfWorld = 100 #500 should be the maxium world size, large 500, medium 250, small 100.
    #whichBlock = random.choice(Blocks.blocksAvailable)
    depthOfWorld = 6
    generate = True
    while generate:
        if depthOfWorld == howDeep:
            generate = False
            break #leave the loop
        whichBlock = 'Grass'
        for x in range(0, lengthOfWorld): #generates the world base on the world size and makes the blocks by appending to the blocksCreated list.
            if currenty == 564:
                blocksCreated.append(Blocks('Grass', 'Sprites/Grass.png',currentx, currenty))
            else:
                blocksCreated.append(Blocks('Dirt', 'Sprites/Dirt.png',currentx, currenty))
            currentx += xDistance
        currenty += yDistance
        howDeep += 1
        currentx = -150

def checkRadius(image, block): #change this to the chunk method.
    r = math.sqrt((image.x - block.x)**2 + (image.y - block.y)**2)
    if r <= renderDistance: #checks if the blocks are in the radius of rendering.
        block.displayImage()

def blockMover(right = False, left = False, up = False, down = False):
    if right:
        for block in blocksCreated:         
            block.x -= 1
    if left:
        for block in blocksCreated: #moves all the blocks in the list to a new x or y.
            block.x += 1
    if up:
        for block in blocksCreated:
            block.y += 1
        image.maxHeightForJump += 1
    if down:
        for block in blocksCreated:
            block.y -= 1
        image.maxHeightForJump -= 1

def blockManager(blockCollided, image):
    blockPos = 0
    last = 0
    check = False
    change = False
    blockLength = len(blocksCreated) #goes through all the blocks in the list and checks uf they can be blit to the screen.
    for block in blocksCreated:
        if block.collidercheck(block, image):
            blockCollided = True
            change = True
        if not change:
            blockCollided = False
        checkRadius(image, block)
        check = mouseCheck(block)
        if check:
            del blocksCreated[blockPos]
        blockPos += 1
    return blockCollided

def blockAndPlayerColliderCheck(image):
    horizontalCheck = False
    change = False
    for block in blocksCreated:
        if block.collidercheck(block, image) and block.y == image.y - 64: #for under the player check
            horizontalCheck = True
            change = False
        if not change:
            horizontalCheck = False
    return horizontalCheck

def foreheadCheck(image, right = False, left = False):
    if right:
        canMove = True
        change = False
        for block in blocksCreated:
            if block.y + 2 >= image.y and block.y <= image.y + 60 and block.x == image.x + 64: #for under the player check
                canMove = False
                change = True
            if not change:
                canMove = True
        return canMove
    if left:
        canMove = True
        change = False# for jumping under blocks if image.y == block.y + 32: self.isjumping  = False
        for block in blocksCreated:
            if block.y + 2 >= image.y and block.y <= image.y + 60 and block.x + 32 == image.x: #for under the player check
                canMove = False
                change = True
            if not change:
                canMove = True
        return canMove

def yJumpCheck(image):
    canMove = True
    change = False
    for block in blocksCreated: #or block.x >= image.x and block.x <= image.x + 64
        if image.y >= block.y and image.y <= block.y + 32 and block.x >= image.x and block.x + 32 <= image.x + 64:# or image.y >= block.y and image.y <= block.y + 32 and image.x >= block.x and image.x <= block.x + 32: #for under the player check
            canMove = False
            change = True
        if not change:
            canMove = True
    return canMove

def mouse_click():
    click = pygame.mouse.get_pressed() #sees if the mouse is clicked.
    return click

def collider_Mouse_Check(sprite):
    mousex, mousey = pygame.mouse.get_pos()
    if mousex >= sprite.x and mousex <= sprite.x + sprite.w and mousey >= sprite.y and mousey <= sprite.y + sprite.h:#checks if the rectangle collider around the sprite is equal to that of the mouse pos.
        return True

def mouseCheck(image):
    if collider_Mouse_Check(image) and mouse_click()[0]:
        return True
    return False

def xCollided(sprite1, sprite2):
    if sprite1.x >= sprite2.x and sprite1.x <= sprite2.x:
        return True
    return False

def yCollided(sprite1, sprite2):
    if sprite1.y >= sprite2.y and sprite1.y <= sprite2.y:
        return True
    return False

#False for the head and side check for jumping, and true for feet check

def feetCheck(blocks, player):
    for block in blocks:
        if block.y >= player.y + 63 and player.y <= block.y + 32:
            if block.x >= player.x and player.x <= block.x + 32:
                return True
    return False
#Game:
#--> Window:
screenW = 1280
screenH = 720
fps = 144
clock = pygame.time.Clock()
ds = pygame.display.set_mode((screenW, screenH))
pygame.display.set_caption("New Worlds")
#--> Other:
event = True


blocksCreated = []
image = Player('Sprite', 'Sprites/test.png', 610, 501)
background = SpriteManager('Background', 'Sprites/Background.png', 0, 0)
blocksAvailable = [pygame.image.load('Sprites/Grass.png'), pygame.image.load('Sprites/Dirt.png')] #Contains all block names...
renderDistance = 1300
generateBlocks()
blockCollided = True
dieCheck = False
if len(blocksCreated) > 1:
    initialLowHeight = blocksCreated[-1].y

while event and not dieCheck:
    event = events() #Checks events from the player.
    background.displayImage()
    image.controlPlayer()
    blockCollided = blockManager(blockCollided, image)#Checks the blocks.
    dieCheck = image.jumpAndGravity(blockCollided, 350, initialLowHeight)  #Checks the player in the gravity area.
    image.displayImage() #Draws image.
    mouseCheck(image) #Mouse Check.
    clock.tick(fps) #The rate at which the screen refreshes.
    pygame.display.update() #Updates the Screen.
pygame.quit()
quit()