import pygame, sys, random, math

def addVector(v1, v2):
    return [x+y for x,y in zip(v1,v2)]

def subVector(v1,v2):
    return [x-y for x,y in zip(v1,v2)]

def dotProduct(vector1, vector2):
    return sum([i*j for (i, j) in zip(vector1, vector2)])



def sign(num):
    result = 1
    if num < 0:
        result = -1
    return result

def colide(rect1, rect2):
    # (x, y, width, height)
    colision = False
    if rect1[0] + rect1[2] > rect2[0] and rect1[1] + rect1[3] > rect2[1] and rect1[0] < rect2[0] + rect2[2] and rect1[1] < rect2[1] + rect2[3]:
        colision = True
    return colision

def getStaticVertecies(rect):
    return ((rect[0], rect[1]), (rect[0]+rect[2], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), (rect[0], rect[1]+rect[3]))


def getRotatedVertecies(rect, angle, skewAngle=0, hypotnuseLength=0):
    # deg to rad
    radAngle = angle*math.pi/180
    radAngle=-radAngle

    x=rect[0]
    y=rect[1]
    vertecies = [(0, 0),(0, 0),(0, 0),(0, 0)]

    if (skewAngle == 0):
        skewAngle = math.acos((rect[2]/2)/(((rect[2]/2)**2+(rect[3]/2)**2)**0.5))
    if (hypotnuseLength == 0):
        hypotnuseLength = math.sqrt(((rect[2]/2)**2)+((rect[3]/2)**2))


    vertecies[0] = (x+math.cos(radAngle-skewAngle-math.pi)*hypotnuseLength, y+math.sin(radAngle-skewAngle-math.pi)*hypotnuseLength)#topLeft
    vertecies[1] = (x+math.cos(radAngle-skewAngle)*hypotnuseLength, y+math.sin(radAngle-skewAngle)*hypotnuseLength)#topRight
    vertecies[3] = (x+math.cos(radAngle+skewAngle+math.pi)*hypotnuseLength, y+math.sin(radAngle+skewAngle+math.pi)*hypotnuseLength)#bottomLeft
    vertecies[2] = (x+math.cos(radAngle+skewAngle)*hypotnuseLength, y+math.sin(radAngle+skewAngle)*hypotnuseLength)#bottomRight

    # debuging
    #for i in range(0,4):
    #    #print("x, y "+str(i)+": ",vertecies[i][0], vertecies[i][1])
    #    pygame.draw.circle(window, (255,0,0), (vertecies[i][0], vertecies[i][1]), 3)
    # end debuging

    return vertecies

def polygonColide(verteciesA, verteciesB):
    for i in range(len(verteciesA)):
        vertexA = verteciesA[i]
        vertexB = verteciesA[(i+1) % len(verteciesA)]

        edge = subVector(vertexB,vertexA)
        axis = (-edge[1], edge[0]) # normal

        minA, maxA = projectVertecies(verteciesA, axis)
        minB, maxB = projectVertecies(verteciesB ,axis)

        if minA >= maxB or minB >= maxA:
            return False


    for i in range(len(verteciesB)):
        vertexA = verteciesB[i]
        vertexB = verteciesB[(i+1) % len(verteciesB)]

        edge = subVector(vertexB,vertexA)
        axis = (-edge[1], edge[0]) # normal

        minA, maxA = projectVertecies(verteciesA, axis)
        minB, maxB = projectVertecies(verteciesB ,axis)

        if minA >= maxB or minB >= maxA:
            return False
    
    return True
        

def projectVertecies(vertecies, axis):
    min = 1.7976931348623157e+308
    max = -1.7976931348623157e+308

    for i in range(len(vertecies)):

        vertex = vertecies[i]
        projection = dotProduct(vertex, axis)
        
        if projection < min:
            min = projection
        if projection > max:
            max = projection
    
    return min, max


pygame.init()

TPS = 240
clock = pygame.time.Clock()


bgColor = (113, 121, 126)

windowWidth = int(1200)
windowHeight = int((windowWidth/16)*9)

window = pygame.display.set_mode((windowWidth, windowHeight))


carWidth = 20
carHeight = 40

carPos = [windowWidth/2 - carWidth/2, windowHeight/2 - carHeight/2, carWidth, carHeight]

carSkewAngle = math.acos((carWidth/2)/(((carWidth/2)**2+(carHeight/2)**2)**0.5))
carHypotnuseLength = math.sqrt(((carWidth/2)**2)+((carHeight/2)**2))

carSprite = pygame.image.load("car.png").convert_alpha()
carSprite = pygame.transform.scale(carSprite, (carWidth, carHeight))
carSpriteMask = pygame.mask.from_surface(carSprite)

angle = 0
langle = 0

rotSpeed = 1
 
drag = 0.001
breakSpeed = 0.02
acceleration = 0.02
curSpeed = 0
maxSpeedForward = 1.5
maxSpeedBackwards = -0.5

# Scroll
scroll = [0, 0]
scrollLast = scroll

scrollWidthDisplacment = windowWidth/15
scrollHeightDisplacment = windowHeight/15

# Particles:
particlesPos = []
particleAmount = 2
particleRadius = 2
particleWidth = 50
particleHeight = particleWidth
particleColor = (255, 255, 255)
particleCollideColor = (255, 0, 0)

for i in range(particleAmount):
    particlesPos.append([random.randint(0, windowWidth), random.randint(0, windowHeight)])


# Game states
run = True
game = True

paused = False
lastPaused = False
while run:
    keyPressed = pygame.key.get_pressed()

    if lastPaused == False and keyPressed[pygame.K_p] == True:
        paused = not paused

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if keyPressed[pygame.K_ESCAPE]:
             run = False
        
    while game:
        window.fill(bgColor) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                run = False
        
        keyPressed = pygame.key.get_pressed()
        if keyPressed[pygame.K_ESCAPE]:
            game = False

        
        # Controls
        if keyPressed[pygame.K_a]:
            angle += rotSpeed
        else:
            if keyPressed[pygame.K_LEFT]:
                angle += rotSpeed
                
        if keyPressed[pygame.K_d]:
            angle -= rotSpeed
        else:
            if keyPressed[pygame.K_RIGHT]:
                angle -= rotSpeed


        if angle > 180:
            angle = angle*-1 + rotSpeed
        if angle < -180:
            angle = angle*-1 - rotSpeed

        radAngle = (-1*angle-90)*math.pi/180
        if keyPressed[pygame.K_w]:
            curSpeed += acceleration
            
            # check max speed
            if curSpeed >= maxSpeedForward:
                curSpeed = maxSpeedForward
        else:
            if keyPressed[pygame.K_UP]:
                curSpeed += acceleration
                
                # check max speed
                if curSpeed >= maxSpeedForward:
                    curSpeed = maxSpeedForward

        if keyPressed[pygame.K_s]:
            curSpeed -= acceleration

            # check max speed
            if curSpeed <= maxSpeedBackwards:
                curSpeed = maxSpeedBackwards
        else:
            if keyPressed[pygame.K_DOWN]:
                curSpeed -= acceleration

                # check max speed
                if curSpeed <= maxSpeedBackwards:
                    curSpeed = maxSpeedBackwards

        # drag
        curSpeed += sign(curSpeed)*drag*-1


        # hand Break
        direction = [math.cos(radAngle)*curSpeed, math.sin(radAngle)*curSpeed]
        if keyPressed[pygame.K_SPACE]:
            curSpeed -= breakSpeed

            if curSpeed <=0:
                curSpeed = 0
            
            if keyPressed[pygame.K_a]:
                direction[0] -= math.cos(radAngle-math.pi/2)*curSpeed
                direction[1] -= math.sin(radAngle-math.pi/2)*curSpeed
            else:
                if keyPressed[pygame.K_LEFT]:
                    direction[0] -= math.cos(radAngle-math.pi/2)*curSpeed
                    direction[1] -= math.sin(radAngle-math.pi/2)*curSpeed
                
            if keyPressed[pygame.K_d]:
                direction[0] += math.cos(radAngle-math.pi/2)*curSpeed
                direction[1] += math.sin(radAngle-math.pi/2)*curSpeed
            else:
                if keyPressed[pygame.K_RIGHT]:
                    direction[0] += math.cos(radAngle-math.pi/2)*curSpeed
                    direction[1] += math.sin(radAngle-math.pi/2)*curSpeed

        # # move car
        # carPos[0] += math.cos(radAngle)*curSpeed
        # carPos[1] += math.sin(radAngle)*curSpeed
        # Scroll
        scroll[0] = direction[0]
        scroll[1] = direction[1]


            

        carRotated = pygame.transform.rotate(carSprite, angle)
        carFinal = carRotated.get_rect(center = (carPos[0], carPos[1]))

        # Drawing car
        window.blit(carRotated, carFinal)
        getRotatedVertecies((carPos[0], carPos[1], carWidth, carHeight), angle, carSkewAngle, carHypotnuseLength)

        # Drawing particles
        for i in range(len(particlesPos)):
            #print(particlesPos[i])
            particlesPos[i][0] -= scroll[0]
            particlesPos[i][1] -= scroll[1]

            #if colide((particlesPos[i][0], particlesPos[i][1], particleWidth, particleHeight), (carPos[0], carPos[1], carWidth, carHeight)):
            if polygonColide(getRotatedVertecies((carPos[0], carPos[1], carWidth, carHeight), angle, carSkewAngle, carHypotnuseLength), getStaticVertecies((particlesPos[i][0], particlesPos[i][1], particleWidth, particleHeight))):
                #particlesPos.remove(particlesPos[i])
                pygame.draw.rect(window, particleCollideColor, (particlesPos[i][0], particlesPos[i][1], particleWidth, particleHeight))
            else:
                pygame.draw.rect(window, particleColor, (particlesPos[i][0], particlesPos[i][1], particleWidth, particleHeight))

        langle = angle
        pygame.display.update()
        clock.tick(TPS)

    lastPaused = keyPressed[pygame.K_p]
    clock.tick(TPS)
exit()