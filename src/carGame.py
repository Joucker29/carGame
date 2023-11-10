import pygame, sys, random, math

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

def rotatedPoints(rect, angle):
    # deg to rad
    radAngle = angle*math.pi/180
    radAngle=-radAngle

    
    #radAngle=-radAngle
    #radAngle = radAngle-math.pi/2

    x=rect[0]
    y=rect[1]
    _width=rect[2]
    _height=rect[3]

    vertecies = [(0, 0),(0, 0),(0, 0),(0, 0)]
    origVertecies = [(0, 0),(0, 0),(0, 0),(0, 0)]


    pointLength = math.sqrt(((_width/2)**2)+((_height/2)**2))
    skewAngle = math.acos((_width/2)/(((_width/2)**2+(_height/2)**2)**0.5))

    origVertecies[0] = (x-_width/2, y-_height/2)

    #print(radAngle)
    #print(x,y)
    vertecies[0] = (x+math.cos(radAngle-skewAngle-math.pi)*pointLength, y+math.sin(radAngle-skewAngle-math.pi)*pointLength)#topLeft
    vertecies[1] = (x+math.cos(radAngle-skewAngle)*pointLength, y+math.sin(radAngle-skewAngle)*pointLength)#topRight
    vertecies[3] = (x+math.cos(radAngle+skewAngle+math.pi)*pointLength, y+math.sin(radAngle+skewAngle+math.pi)*pointLength)#bottomLeft
    vertecies[2] = (x+math.cos(radAngle+skewAngle)*pointLength, y+math.sin(radAngle+skewAngle)*pointLength)#bottomRight


    #pygame.draw.rect(window, (255,0,0), (vertecies[0][0], vertecies[0][1], 3, 3))
    for i in range(0,4):
        print("x, y "+str(i)+": ",vertecies[i][0], vertecies[i][1])
        pygame.draw.circle(window, (255,0,0), (vertecies[i][0], vertecies[i][1]), 3)

    
    


pygame.init()

TPS = 240
clock = pygame.time.Clock()


bgColor = (113, 121, 126)

windowWidth = int(1200)
windowHeight = int((windowWidth/16)*9)

window = pygame.display.set_mode((windowWidth, windowHeight))


width = 20
height = 40

carPos = [windowWidth/2 - width/2, windowHeight/2 - height/2, width, height]

carSprite = pygame.image.load("car.png").convert_alpha()
carSprite = pygame.transform.scale(carSprite, (width, height))
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
        rotatedPoints((carPos[0], carPos[1], width, height), angle)

        # Drawing particles
        for i in range(len(particlesPos)):
            #print(particlesPos[i])
            particlesPos[i][0] -= scroll[0]
            particlesPos[i][1] -= scroll[1]

            if colide((particlesPos[i][0], particlesPos[i][1], particleWidth, particleHeight), (carPos[0], carPos[1], width, height)):
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