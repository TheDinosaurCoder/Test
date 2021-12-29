#Author: Michael Bradshaw
#Date: Start: 2020/08/05
#File Name: New_Worlds.py
#Desription: A Game that has a art sytle to teraria, and is a space, world game.
#place single pixel with pygame.Surface.set_at().

import pygame
import random #import necessary librarys for the program.
import math
import time
import noise #Import the perlin noise library
import json
import pickle

#Classes:

class SpriteManager():
    def __init__(self, tag, image, x, y):
        self.tag = tag
        self.x = x
        self.y = y
        if self.tag == 'Background':
            self.image = pygame.image.load(image).convert()#optimes the background that have fill interiors.
        elif self.tag != 'Grass' and self.tag != 'Dirt' and self.tag != 'Bedrock':
            self.image = pygame.image.load(image)
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
            self.w = self.image.get_width()
            self.h = self.image.get_height()
            #self.rect = self.image.get_rect(topleft=(self.x, self.y)) #sets the rect of the player with x,y,w,h
        else:
            if self.tag == 'Grass':
                self.w = blocksAvailable[0].get_width()
                self.h = blocksAvailable[0].get_height()
                self.rect = blocksAvailable[0].get_rect(topleft=(self.x, self.y))
            elif self.tag == 'Dirt':
                self.w = blocksAvailable[1].get_width()
                self.h = blocksAvailable[1].get_height()
                self.rect = blocksAvailable[1].get_rect(topleft=(self.x, self.y))
            elif self.tag == 'Bedrock':
                self.w = blocksAvailable[2].get_width()
                self.h = blocksAvailable[2].get_height()
                self.rect = blocksAvailable[2].get_rect(topleft=(self.x, self.y))

    #Converts the image to run faster:
    def convertImage(self, imageID):
        self.image = pygame.image.load(imageID).convert()

    def displayImage(self): #Displays the image at the positons provided.

        if self.tag == 'Dirt':
            self.rect = blocksAvailable[1].get_rect(topleft = (self.x, self.y)) #gest tge
            ds.blit(blocksAvailable[1], (self.x, self.y))
        elif self.tag == 'Grass':
            self.rect = blocksAvailable[0].get_rect(topleft = (self.x, self.y)) #gest tge
            ds.blit(blocksAvailable[0], (self.x, self.y))
        elif self.tag == 'Bedrock':
            self.rect = blocksAvailable[2].get_rect(topleft = (self.x, self.y)) #gest tge
            ds.blit(blocksAvailable[2], (self.x, self.y))
        else:
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
        self.maxDepthPlayer = 592
        self.change = False
        self.speed = 3

    def jumpAndGravity(self, isCollidingWithGround, jumpLimit, initialLowHeight): #Need timer for when this instance goes....
        if isCollidingWithGround == False and self.isJumping == False:
            self.isJumping = False
            self.falling = True

        if self.y < 450 and self.isJumping == False and self.change == False:
            self.maxHeightForJump = 200
            self.change = True
        elif self.y > 450 and self.isJumping == False:
            self.maxHeightForJump = 350
            self.change = False

        if self.isJumping:

            if initialLowHeight > chunkWorld[whichChunkRender][0][-1].y:

                if yJumpCheck(image) and canMoveUp(image) and topMoveCheck(image): #topMoveCheck(image) can move in block.
                    blockMover(False,False, True, False)
                    self.y -= 2 * dt * self.speed
                    self.howManyUp += 2 * dt * self.speed
                    if self.howManyUp == 150:# or not yJumpCheck(image) and not topRightCheck(image) or not yJumpCheck(image) and not topLeftCheck(image):
                        self.isJumping = False
                        self.falling = True #makes the player jump. by looking at loops and stuff.
                else:
                    self.isJumping = False
                    self.falling = True #makes the player jump. by looking at loops and stuff.

            elif initialLowHeight == chunkWorld[whichChunkRender][0][-1].y:

                self.y -= 2 * dt * self.speed
                if self.y <= self.maxHeightForJump or self.y >= 700 or not yJumpCheck(image):
                    self.isJumping = False
                    self.falling = True #makes the player jump. by looking at loops and stuff.

        if self.falling or isCollidingWithGround == False and self.y >= 500 and self.y <= 640 and not self.isJumping :#The player falls when no block is under.
            if isCollidingWithGround and yJumpCheck(image):
                self.falling = False

            else:#this is the problem #625 is the max depth for the player
                if chunkWorld[whichChunkRender][0][-1].y <= 690:
                    self.maxDepthPlayer = 625
                else:#Changes the maax depth for the player based on where the player is:
                    self.maxDepthPlayer = 592
                if self.y <= self.maxDepthPlayer or chunkWorld[whichChunkRender][0][-1].y >= 688 and self.y <= self.maxDepthPlayer and isCollidingWithGround == False:
                    self.y += 2 * dt * self.speed
                if self.y >= self.maxDepthPlayer and chunkWorld[whichChunkRender][0][-1].y >= 689 and isCollidingWithGround == False:
                    blockMover(False,False, False, True)
                elif self.y >= 625 and isCollidingWithGround == False:
                    print('YOU DIED!')
                    return True

        if isTopColliding(image):
            self.isJumping = False
            self.falling = True
            
        if dieCheck == False:
            return False

    def controlPlayer(self, canMoveRight, canMoveLeft): #Player Controls
        keys = pygame.key.get_pressed() #gets all keys pressed.
        if keys[pygame.K_d] and canMoveRight:
            if self.x < 1000 or chunkWorld[-1][1] + chunkWorld[-1][2] <= 1250 and self.x <= 1218:
                self.x += 1 * dt * self.speed
            if self.x >= 1000 and chunkWorld[-1][1] + chunkWorld[-1][2] >= 1250:
                blockMover(True) 
        if keys[pygame.K_a] and canMoveLeft:
            if self.x > 280 or chunkWorld[0][1] >= 0 and self.x > 1:
                self.x -= 1 * dt * self.speed
            if self.x == 280 and chunkWorld[0][1] < 0: #moves the player in a ddddddset x and y, camera follows.
                blockMover(False,True)
        if keys[pygame.K_SPACE] and check[1] and self.isJumping == False:
            self.isJumping = True
            self.howManyUp = 0

class Blocks(SpriteManager):

    def __init__(self, spriteName, imageID, x, y, damage = 0, derablity = 0):
        super().__init__(spriteName, imageID, x, y) #Send info to the class that manages sprites.
        self.damage = damage
        self.derablity = derablity #sets damage and deribity to the blocks

#Functions:

def events():
    pygame.display.set_caption("New Worlds FPS: " + str(int(clock.get_fps())))
    for event in eventLog:
        if event.type == pygame.QUIT: #checks for the events that pygame get through the program.
            return False

        if event.type == pygame.KEYDOWN: #ends program if conditions are true.
            if event.key == pygame.K_q:
                return False
            if event.key == pygame.K_f:
                print('Player in: ', whichChunkRender + 1, ' out of ', len(chunkWorld))
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
    if chunkWorld[whichChunkRender][0][0].y < 340:
        #distance = math.sqrt((image.x - block.x)**2 + (image.y - block.y)**2)
        #distance = (distance) / 32
        #if distance < 10:
        if block.x >= -64 and block.x <= 1300 and block.y >= -32 and block.y <= 720:
            block.displayImage()
        return True
    else:
        if block.x >= -64 and block.x <= 1300 and block.y >= -32 and block.y <= 720:
            block.displayImage()
            return True

def blockMover(right = False, left = False, up = False, down = False):
    if right:
        moveChunks(right)
    if left:
        moveChunks(right, left)
    if up:
        moveChunks(False, False, True)
        image.maxHeightForJump += 1
    if down:
        moveChunks(False, False, False, True)
        image.maxHeightForJump -= 1

def blockAndPlayerColliderCheck(image):#NOT USED!
    horizontalCheck = False
    change = False
    #print(blocksCreated[0])
    for block in chunkWorld[whichChunkRender][0]:
        if block.collidercheck(block, image) and block.y == image.y - 64: #for under the player check
            horizontalCheck = True
            change = False
        if not change:
            horizontalCheck = False
    return horizontalCheck

def foreheadCheck(image, block, right, left):
    if right:
        canMove = True
        change = False
           # if block.y + 1 == image.y:
            #    block.y + 1 >= image.y and block.y + 31 <= image.y + 64 and image.x + 64 >= block.x and image.x + 64 < block.x + 32
        if block.y + 2 >= image.y and block.y <= image.y + 60 and image.x + 64 >= block.x and image.x + 64 < block.x + 32: #for under the player check
            canMove = False
            change = True
        if change == False:
            canMove = True
        return canMove, change

    if left:
        canMove = True
        change = False# for jumping under blocks if image.y == block.y + 32: self.isjumping  = False
        if block.y + 2 >= image.y and block.y <= image.y + 60 and image.x > block.x and image.x <= block.x + 32: #for under the player check
            canMove = False
            change = True
        if change == False:
            canMove = True
        return canMove, change

def isTopColliding(image):
    collide = False
    change = False
    for block in chunkWorld[whichChunkRender][0]: 
        if image.collidercheck(image, block) and block.y <= image.y:
            collide = True
            change = True
        if not change:
            collide = False
    return collide

def yJumpCheck(image):
    canMove = True
    change = False
    for block in chunkWorld[whichChunkRender][0]: #or block.x >= image.x and block.x <= image.x + 64
        if image.y >= block.y and image.y <= block.y + 32 and block.x >= image.x and block.x + 32 <= image.x + 64:# or image.y >= block.y and image.y <= block.y + 32 and image.x >= block.x and image.x <= block.x + 32: #for under the player check
            canMove = False
            change = True
        if not change:
            canMove = True
    return canMove

def canMoveUp(image):
    canMove = True
    change = False
    for block in chunkWorld[whichChunkRender][0]: #or block.x >= image.x and block.x <= image.x + 64
        if image.x >= block.x and image.x < block.x + 32 and image.y - 3 <= block.y + 32 and image.y > block.y + 32: #Left
            canMove = False
            change = True
        if image.x + 32 >= block.x and image.x + 64 < block.x + 32 and image.y - 3 <= block.y + 32 and image.y > block.y + 32: #Right
            canMove = False
            change = True
        
        if not change:
            canMove = True
    return canMove


def topMoveCheck(image):
    canMove = True
    change = False
    for block in chunkWorld[whichChunkRender][0]:
        if image.x >= block.x and image.x < block.x + 32 and image.y - 3 >= block.y + 32 and image.y <= block.y + 32: #Left
            canMove = False
            change = True
        if image.x + 64 >= block.x and image.x + 64 < block.x + 32 and image.y - 3 >= block.y + 32 and image.y <= block.y + 32: #Right
            canMove = False
            change = True

        if change == False:
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

def mouseCheckRight(image):
    #Checks if the right mouse button is pressed.
    if collider_Mouse_Check(image) and mouse_click()[2]:
        return True
    return False

#False for the head and side check for jumping, and true for feet check
def feetCheck(blocks, player):
    for block in blocks:
        if block.y >= player.y + 63 and player.y <= block.y + 32:
            if block.x >= player.x and player.x <= block.x + 32:
                return True
    return False

def createChunkWorld(lengthoFWorld):
    #Varables that hold the length of each segment of the world.
    horizontalLength = lengthoFWorld[0]
    verticalLength = lengthoFWorld[1]
    numberOfBlocksPerChunk = 25
    numberChunks = int(horizontalLength / numberOfBlocksPerChunk) #-number of blocks per chunk, try 50 next.
    #number of blocks times the size in pixels.
    lengthofChunk = (numberOfBlocksPerChunk - 1) * 32 #So number of blocks - 1 since it starts at pos 0, muply by 32 the pixel size
    xDistance = 32 #sets the conditons
    yDistance = 32
    x = 0
    for chunk in range(numberChunks): #-The chunk index.

        chunkWorld.append([]) #Adds a list.
        chunkWorld[chunk].append([]) #at zero is a list of the blocks.
        #gets the current chunk pos by * currentChuck by lengthOfChunk
        currentChunkXPos = (chunk * lengthofChunk) - (horizontalLength / 2)

        #other:
        currentx = currentChunkXPos
        currenty = 564
        #adds the properties:

        chunkWorld[chunk].append(currentChunkXPos)#1 index
        chunkWorld[chunk].append(lengthofChunk)#2 index
        #Change in x and y is the 3 index:
        chunkWorld[chunk].append((0, 0))

        #Runs a loop through the vertical length of the world:
        for v in range(verticalLength):
            currentx = currentChunkXPos
            theChange = currenty
            #Runs a loop through the horizontal length of the chunk 25 blocks.
            for h in range(25):
                #based on the height it will add the number of blocks to the array
                if v < 1:
                    height = int(noise.pnoise1(x * 0.1, base = 6) * 8)
                    if height < 0:
                        height *= -1
                    theChange = currenty - (height * 32)
                    #For the first 10 levels let it get the anoise applied to it.
                    chunkWorld[chunk][0].append(Blocks('Grass', 'Sprites/Grass.png',currentx, theChange))
                    for i in range(1, height + 1):
                       add = (i * 32) + currenty - (height * 32)#The ting
                       chunkWorld[chunk][0].append(Blocks('Dirt', 'Sprites/Dirt.png',currentx, add))
                else:
                    theChange = currenty
                    # if v == 0:#This is the level where we add grass.
                    #     #adds a block to the block list in the chunk list.
                    #     $chunkWorld[chunk][0].append(Blocks('Grass', 'Sprites/Grass.png',currentx, theChange))
                    if v == verticalLength - 1:
                        chunkWorld[chunk][0].append(Blocks('Bedrock', 'Sprites/BedRock.png',currentx, theChange))
                    else:
                        #adds a block to the block list in the chunk list.
                        chunkWorld[chunk][0].append(Blocks('Dirt', 'Sprites/Dirt.png',currentx, theChange))
                currentx += xDistance
                x += 1
            currenty += yDistance

def manageChunkWorld(blockCollided):
    #Check where is player:
    #count how many blocks from player to border.
    for i in range(len(chunkWorld) - 1, - 1, -1): #Runs through the length of the chunk world list.
        #Check if player is in a chunk:
        if image.x >= chunkWorld[i][1] and image.x <= chunkWorld[i][1] + chunkWorld[i][2]:
            delete = False
            if i > 0 and i < len(chunkWorld) - 1: #frist one than its from player to 0
                if chunkWorld[i - 1][0][-1].x > -1:
                    #border = int((image.x - chunkWorld[i - 1][0][-1].x) / 32)
                    #counter = 0
                    #max = 25
                    blockPos = 0
                    #Render i - 1 and i + 1 and i:
                    for block in chunkWorld[i - 1][0]:#Displays the images for the blocks.
                        if block.x > 0:
                            delete = checkRadius(image, block)#Displays in this.
                            check = mouseCheck(block)
                            if check and delete:
                                del chunkWorld[i - 1][0][blockPos] #Deletes the block in the player chunk:
                        blockPos += 1

                if chunkWorld[i + 1][0][0].x < 1282:
                    blockPos = 0
                    for block in chunkWorld[i + 1][0]:#Displays the image for the blocks.
                        if block.x < 1281:
                            delete = checkRadius(image, block)#Displays in this.
                            check = mouseCheck(block)
                            if check and delete:
                                del chunkWorld[i + 1][0][blockPos] #Deletes the block in the player chunk:
                        blockPos += 1

            elif i == 0 and len(chunkWorld) > 1:
                blockPos = 0
                for block in chunkWorld[i + 1][0]:#Displays the image for the blocks.
                    delete = checkRadius(image, block)#Displays in this.
                    check = mouseCheck(block)
                    if check and delete:
                        del chunkWorld[i + 1][0][blockPos] #Deletes the block in the player chunk:
                    blockPos += 1

            elif i == len(chunkWorld) and len(chunkWorld) > 1:
                blockPos = 0
                for block in chunkWorld[i - 1][0]:#Displays the image for the blocks.
                    delete = checkRadius(image, block)#Displays in this.
                    check = mouseCheck(block)
                    if check and delete:
                        del chunkWorld[i - 1][0][blockPos] #Deletes the block in the player chunk:
                    blockPos += 1
            #----------------------------------------- i stuff!
            #Check Variables:
            change = False
            blockPos = 0 #Sets the blockPos to zero
            canMoveRight = False
            canMoveLeft = False
            moveMentChangeR = False
            moveMentChangeL = False
            #Runs through the blocks that the player is within:
            for block in chunkWorld[i][0]:
                if block.x > -1 and block.x < 1281 and block.y > 0 and block.y < 720:
                    #This happens for only the chunk the player is in:
                    if block.collidercheck(block, image):
                        blockCollided = True
                        change = True
                    if change == False:
                        blockCollided = False
                    if moveMentChangeR == False:
                        canMoveRight, moveMentChangeR = foreheadCheck(image, block, True, False)
                    if moveMentChangeL == False:
                        canMoveLeft, moveMentChangeL = foreheadCheck(image, block, False, True)
                    delete = checkRadius(image, block)
                    check = mouseCheck(block)
                    if check and delete:
                        del chunkWorld[i][0][blockPos] #Deletes the block in the player chunk:
                blockPos += 1
            return i, blockCollided, canMoveRight, canMoveLeft #Returns the chunk the player is within.

def moveUpDown(movementDirection):
    for i in range(len(chunkWorld)):
        chunkWorld[i][3] = (chunkWorld[i][3][0], chunkWorld[i][3][1] + movementDirection)

    if whichChunkRender != len(chunkWorld):
        if whichChunkRender > 0 and whichChunkRender != len(chunkWorld) - 1: #checks if the chunk is greater than zero and not the last chunk
            for i in range(len(chunkWorld[whichChunkRender - 1][0])):
                chunkWorld[whichChunkRender - 1][0][i].y += chunkWorld[whichChunkRender - 1][3][1]
            chunkWorld[whichChunkRender - 1][3] = (chunkWorld[whichChunkRender - 1][3][0], 0)

            #Then change the x values:
            for i in range(len(chunkWorld[whichChunkRender][0])):
                chunkWorld[whichChunkRender][0][i].y += chunkWorld[whichChunkRender][3][1]
            chunkWorld[whichChunkRender][3] = (chunkWorld[whichChunkRender][3][0], 0)

            for i in range(len(chunkWorld[whichChunkRender + 1][0])):
                chunkWorld[whichChunkRender + 1][0][i].y += chunkWorld[whichChunkRender + 1][3][1]
            chunkWorld[whichChunkRender + 1][3] = (chunkWorld[whichChunkRender + 1][3][0], 0)

        elif whichChunkRender == 0 and len(chunkWorld) > 1:
            #Then change the x values:
            for i in range(len(chunkWorld[whichChunkRender][0])):
                chunkWorld[whichChunkRender][0][i].y += chunkWorld[whichChunkRender][3][1]
            chunkWorld[whichChunkRender][3] = (chunkWorld[whichChunkRender][3][0], 0)
            for i in range(len(chunkWorld[whichChunkRender + 1][0])):
                chunkWorld[whichChunkRender + 1][0][i].y += chunkWorld[whichChunkRender + 1][3][1]
            chunkWorld[whichChunkRender + 1][3] = (chunkWorld[whichChunkRender + 1][3][0], 0)

        elif whichChunkRender == len(chunkWorld) - 1:
            #Then change the x values:
            for i in range(len(chunkWorld[whichChunkRender][0])):
                chunkWorld[whichChunkRender][0][i].y += chunkWorld[whichChunkRender][3][1]
            chunkWorld[whichChunkRender][3] = (chunkWorld[whichChunkRender][3][0], 0)

            for i in range(len(chunkWorld[whichChunkRender - 1][0])):
                chunkWorld[whichChunkRender - 1][0][i].y += chunkWorld[whichChunkRender - 1][3][1]
            chunkWorld[whichChunkRender - 1][3] = (chunkWorld[whichChunkRender - 1][3][0], 0)

def moveChunks(right = False, left = False, up = False, down = False):

    #Sets the values based on the right or left:
    if right:
        movementDirection = -1
    elif left:
        movementDirection = 1
    elif up:
        movementDirectionV = 1
        moveUpDown(movementDirectionV)
    elif down:
        movementDirectionV = -1
        moveUpDown(movementDirectionV)
    else:
        return 0
    if right or left:
        #loops through the chunks to apply the movement:
        for i in range(len(chunkWorld)):
            chunkWorld[i][1] += movementDirection #Works
            chunkWorld[i][3] = (chunkWorld[i][3][0] + movementDirection, chunkWorld[i][3][1])#Works

        if whichChunkRender != len(chunkWorld):
            #This is the problem
            if whichChunkRender > 0 and whichChunkRender != len(chunkWorld) - 1: #checks if the chunk is greater than zero and not the last chunk
                #Then change the x values:
                for i in range(len(chunkWorld[whichChunkRender][0])):
                    chunkWorld[whichChunkRender][0][i].x += chunkWorld[whichChunkRender][3][0]
                chunkWorld[whichChunkRender][3] = (0, chunkWorld[whichChunkRender][3][1])

                for i in range(len(chunkWorld[whichChunkRender - 1][0])):
                    chunkWorld[whichChunkRender - 1][0][i].x += chunkWorld[whichChunkRender - 1][3][0]
                chunkWorld[whichChunkRender - 1][3] = (0, chunkWorld[whichChunkRender - 1][3][1])

                for i in range(len(chunkWorld[whichChunkRender + 1][0])):
                    chunkWorld[whichChunkRender + 1][0][i].x += chunkWorld[whichChunkRender + 1][3][0]
                chunkWorld[whichChunkRender + 1][3] = (0, chunkWorld[whichChunkRender + 1][3][1])

            elif whichChunkRender == 0 and len(chunkWorld) > 1:
                #Then change the x values:
                for i in range(len(chunkWorld[whichChunkRender][0])):
                    chunkWorld[whichChunkRender][0][i].x += chunkWorld[whichChunkRender][3][0]
                chunkWorld[whichChunkRender][3] = (0, chunkWorld[whichChunkRender][3][1])
                for i in range(len(chunkWorld[whichChunkRender + 1][0])):
                    chunkWorld[whichChunkRender + 1][0][i].x += chunkWorld[whichChunkRender + 1][3][0]
                chunkWorld[whichChunkRender + 1][3] = (0, chunkWorld[whichChunkRender + 1][3][1])

            elif whichChunkRender == len(chunkWorld) - 1:
                #Then change the x values:
                for i in range(len(chunkWorld[whichChunkRender][0])):
                    chunkWorld[whichChunkRender][0][i].x += chunkWorld[whichChunkRender][3][0]
                chunkWorld[whichChunkRender][3] = (0, chunkWorld[whichChunkRender][3][1])

                for i in range(len(chunkWorld[whichChunkRender - 1][0])):
                    chunkWorld[whichChunkRender - 1][0][i].x += chunkWorld[whichChunkRender - 1][3][0]
                chunkWorld[whichChunkRender - 1][3] = (0, chunkWorld[whichChunkRender - 1][3][1])

def checkToMove():
    if image.y <= 550 and chunkWorld[whichChunkRender][0][0].y > 564:
        blockMover(False,False, True, False)

def changeBackground():
    if chunkWorld[whichChunkRender][0][0].y <= 0 and background.tag != 'Underground':
        background.tag = 'Underground'
        background.convertImage('Sprites/Underground.png')
    elif background.tag == 'Underground' and chunkWorld[whichChunkRender][0][0].y >= 0:
        background.tag = 'Background'
        background.convertImage('Sprites/Background.png')

def writeWorldFile():
    with open('world.pkl', 'wb') as output:
        pickle.dump(chunkWorld, output, pickle.HIGHEST_PROTOCOL)#saves world
def loadWorldFile():
    with open('world.pkl', 'rb') as input:
        world = pickle.load(input)
        return world

def doIt():
    for event in eventLog:
        if event.type == pygame.KEYDOWN: #ends program if conditions are true.
            if event.key == pygame.K_F4:
                writeWorldFile()
            if event.key == pygame.K_F5:
                return loadWorldFile()
    return chunkWorld


def calculateDeltatime(dt, previous_frame_time):
    dt = time.time() - previous_frame_time
    dt *= 60
    previous_frame_time = time.time()
    return previous_frame_time, dt
#Game:
#--> Window:
BLACK = (0, 0, 0)

#

dt = 0
previous_frame_time = 0
elapsed_time = 0
time_between_spawns = 100

#
screenW = 1280
screenH = 720
fps = 144
clock = pygame.time.Clock()
ds = pygame.display.set_mode((screenW, screenH))
pygame.display.set_caption("New Worlds")
#--> Other:
event = True
changeInxy = [0, 0]
chunkWorld = []
image = Player('Sprite', 'Sprites/test.png', 610, 501)
background = SpriteManager('Background', 'Sprites/Background.png', 0, 0)
blocksAvailable = [pygame.image.load('Sprites/Grass.png'), pygame.image.load('Sprites/Dirt.png'), pygame.image.load('Sprites/Bedrock.png')] #Contains all block names...
whichChunkRender = 0
#Large is 1500x50
#Medium is 750x50
#Small is 375x50
createChunkWorld((25000, 100)) #25000x100
#World lengths notes: 2000 by 50 good, 4000 by 50 good, 6000 by 50 good. 50,000 by 50 good! #Widths size does not affect peformentss 3000 by 50 godo
#Only deepness
dieCheck = False
if len(chunkWorld[whichChunkRender][0]) > 1:
    initialLowHeight = chunkWorld[whichChunkRender][0][-1].y

check = (whichChunkRender, True)
#Main game loop:
while event and not dieCheck:
    checkToMove()
    changeBackground()
    eventLog = pygame.event.get()#all logs
    event = events() #Checks events from the player.
    chunkWorld = doIt() #saves and loads world
    background.displayImage()

    previous_frame_time, dt = calculateDeltatime(dt, previous_frame_time)

    check = manageChunkWorld(check[1])
    whichChunkRender = check[0]
    right = check[2]
    left = check[3]
    image.controlPlayer(right, left)
    image.jumpAndGravity(check[1], 350, initialLowHeight)
    image.displayImage() #Draws image.
    
    mouseCheck(image) #Mouse Check.
    clock.tick(fps) #The rate at which the screen refreshes.
    pygame.display.update() #Updates the Screen.

pygame.quit()
quit()