import pygame, sys, random, math

def sign(num):
    result = 1
    if num < 0:
        result = -1
    return result


pygame.init()

TPS = 240
clock = pygame.time.Clock()

windowWidth = int(1200)
windowHeight = int((windowWidth/16)*9)

window = pygame.display.set_mode((windowWidth, windowHeight))

carPos = [windowWidth/2 + 100, windowHeight/2 - 60]
width = 5
height = 10

angle = 0
langle = 0

rotSpeed = 1


drag = 0.001
acceleration = 0.02
curSpeed = 0
maxSpeedForward = 1.5
maxSpeedBackwards = -0.5

carSprite = pygame.image.load("car.png")
carSprite = pygame.transform.scale(carSprite, (width, height))


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
        window.fill((0,0,0)) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                run = False
        
        keyPressed = pygame.key.get_pressed()
        if keyPressed[pygame.K_ESCAPE]:
            game = False

        # hand Break
        if keyPressed[pygame.K_SPACE]:
            curSpeed = 0
        
        if keyPressed[pygame.K_a]:
            angle += rotSpeed
        if keyPressed[pygame.K_d]:
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

        if keyPressed[pygame.K_s]:
            curSpeed -= acceleration

            # check max speed
            if curSpeed <= maxSpeedBackwards:
                curSpeed = maxSpeedBackwards

        #drag
        curSpeed += sign(curSpeed)*drag*-1

        # move car
        carPos[0] += math.cos(radAngle)*curSpeed
        carPos[1] += math.sin(radAngle)*curSpeed

        # Debug print
        # if (angle != langle):
        #     print(angle)
        # if curSpeed > 1.499:
        #     print(curSpeed)
        
        carRotated = pygame.transform.rotate(carSprite, angle)
        carFinal = carRotated.get_rect(center = (carPos[0], carPos[1]))

        window.blit(carRotated, carFinal)


        langle = angle
        pygame.display.update()
        clock.tick(TPS)
    

    lastPaused = keyPressed[pygame.K_p]
    clock.tick(TPS)