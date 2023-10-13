import pygame, sys, random, math

def sign(num):
    result = 1
    if num < 0:
        result = -1
    return result


pygame.init()

TPS = 240
clock = pygame.time.Clock()


bgColor = (113, 121, 126)

windowWidth = int(1200)
windowHeight = int((windowWidth/16)*9)

window = pygame.display.set_mode((windowWidth, windowHeight))


width = 5
height = 10

carPos = [windowWidth/2 - width/2, windowHeight/2 - height/2]

angle = 0
langle = 0

rotSpeed = 1


drag = 0.001
breakSpeed = 0.02
acceleration = 0.02
curSpeed = 0
maxSpeedForward = 1.5
maxSpeedBackwards = -0.5

carSprite = pygame.image.load("car.png")
carSprite = pygame.transform.scale(carSprite, (width, height))

# Scroll
scroll = [0, 0]
scrollLast = scroll

scrollWidthDisplacment = windowWidth/15
scrollHeightDisplacment = windowHeight/15

# Particles:
particlesPos = []
particleAmount = 50
particleRadius = 2
particleColor = (255, 255, 255)

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
            if keyPressed[pygame.K_d]:
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

        # Drawing particles
        for i in range(len(particlesPos)):
            particlesPos[i][0] -= scroll[0]
            particlesPos[i][1] -= scroll[1]

            pygame.draw.circle(window, particleColor, particlesPos[i], particleRadius, 0)

        langle = angle
        pygame.display.update()
        clock.tick(TPS)

    lastPaused = keyPressed[pygame.K_p]
    clock.tick(TPS)