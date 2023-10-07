import pygame, sys, random, math

pygame.init()


windowWidth = int(1200)
windowHeight = int((windowWidth/16)*9)

window = pygame.display.set_mode((windowWidth, windowHeight))

carPos = [windowWidth/2 + 100, windowHeight/2 - 60]
width = 5
height = 10

angle = 0
langle = 0

rotSpeed = 0.5

speed = 1 # const (DO NOT CHANGE IN CODE)
curSpeed = speed


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
        if keyPressed[pygame.K_SPACE]:
            curSpeed = speed/2
        else:
            curSpeed = speed
        
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
            carPos[0] += math.cos(radAngle)*curSpeed
            carPos[1] += math.sin(radAngle)*curSpeed
        if keyPressed[pygame.K_s]:
            carPos[0] -= math.cos(radAngle)*curSpeed
            carPos[1] -= math.sin(radAngle)*curSpeed

        if (angle != langle):
            print(angle)
        
        carRotated = pygame.transform.rotate(carSprite, angle)
        carFinal = carRotated.get_rect(center = (carPos[0], carPos[1]))



        window.blit(carRotated, carFinal)


        langle = angle
        pygame.display.update()
    

    lastPaused = keyPressed[pygame.K_p]