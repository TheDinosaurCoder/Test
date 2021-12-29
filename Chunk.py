import pygame

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

class Blocks(SpriteManager):

    def __init__(self, spriteName, imageID, x, y, damage = 0, derablity = 0):
        super().__init__(spriteName, imageID, x, y) #Send info to the class that manages sprites.
        self.damage = damage
        self.derablity = derablity #sets damage and deribity to the blocks

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

    currentChunkXPos = 0
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
            #Runs a loop through the horizontal length of the chunk 25 blocks.
            for h in range(25):
                #adds a block to the block list in the chunk list.
                chunkWorld[chunk][0].append(Blocks('Dirt', 'Sprites/Dirt.png',currentx, currenty))
                #if currentChunkXPos == -250 and currenty == 564:
                    #print(currentx)
                currentx += xDistance
            currenty += yDistance

    print(numberChunks)




def manageChunkWorld(player):
    chunkNum = 0
    for chunk in chunkWorld:
        if player[0] >= chunk[1] and player[0] <= chunk[1] + chunk[2]:
            return chunkNum
        else:
            print('NA!')
        chunkNum += 1
whichChunk = 0
chunkWorld = []
#other:
#1000 by 100 world may be the maxmium height may be max at !50! or 100 Max world is 3000x50
createChunkWorld((1010, 50))
print(chunkWorld[2][1])
whichChunk = manageChunkWorld((610.0, 501))
print(whichChunk)
blocksCreated = chunkWorld[whichChunk][0]
print(blocksCreated[0], blocksCreated[1])


#blocksAvailable = [pygame.image.load('Sprites/Grass.png'), pygame.image.load('Sprites/Dirt.png')] #Contains all block names...

#print(chunkWorld[0][1])
#print(chunkWorld[0][3])

#print(chunkWorld[1][1])
#print(chunkWorld[1][3])

#playerx = -50
#playery = 0
#counter = 0
#for i in chunkWorld[-1][0]:
 #   if counter == 25:
 #       break
 #       print(" ")
 #   print(i.x, i.y)
 #   counter += 1

##print(len(chunkWorld))

#print(' ')

#manageChunkWorld((playerx, playery))
#CHUNKS WORK!

#chunk 2 = 518 but it starts from 0 so it is acutal chunk 1

#still use radius to render

#do if (blocks in all chucks <= radius):
#draw!
