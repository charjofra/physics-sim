import pygame
import pymunk
import pymunk.pygame_util
import math
import random

pygame.init()

#setting the values for the width and height of the window, these are constant.
WIDTH = 1300
HEIGHT = 800

#setting the window dimensions and title
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Physics Simulator")

gamePause = False

#setting the values for the text colour (white) along with the font, size of the text, and the scale
TEXTCOLOUR = (255,255,255)
defaultTextSize = 100
smallTextSize = 70
largeTextSize = 130
defaultFont = pygame.font.SysFont("Arial Rounded MT Bold", defaultTextSize)
smallFont = pygame.font.SysFont("Arial Rounded MT Bold", smallTextSize)
largeFont = pygame.font.SysFont("Arial Rounded MT Bold", largeTextSize)

fontChoice = defaultFont

scale = 1
textHeight = 0
TextWidth = 0

colours = ((255,210,43, 100), (254,178,4, 100), (255,133,3, 100), (213,54,0, 100), (112,14,1, 100), (146,221,200, 100), (129,182,157, 100), (90,161,127, 100), (19,122,99, 100), (10,58,42, 100))
planetColour = (200,200,150)

fps = 60
dt = 1/fps

#This function exists so I can call back to the main menu from anywhere in the program
def mainLoop(fontChoice, scale, textHeight, TextWidth, fps, dt):

    #creating the function to draw text on the main menu screen
    def writeText(text, font, textColour, x, y):
        img = font.render(text, True, textColour)
        window.blit(img, (x, y))

    #creating the function to draw any image I would like to add to the screen
    def addImage(image, x, y):
        drawnImage = pygame.image.load(image).convert()
        window.blit(drawnImage, (x, y))

    #creating the function to draw rectancles for the background of the buttons on the main menu    
    def drawRectangle(x, y, width, height, radius, colour):
        rectangle = pygame.Rect(x, y, width, height)
        pygame.draw.rect(window, colour, rectangle, border_radius = radius)

    def guideLine():
        drawRectangle(650, 0, 1, 800, 4, (0,0,0))
        drawRectangle(0, 400, 1300, 1, 4, (0,0,0))
    
    #creating the function to change the scale when the text size is changed, keeping the scale of everything constant with the text size
    def changeScale(scale, fontChoice, textHeight, TextWidth):
        if fontChoice == smallFont:
            scale = 0.7
            textHeight = 10
            TextWidth = +30
            settings(fontChoice, scale, textHeight, TextWidth)
        if fontChoice == defaultFont:
            scale = 1
            textHeight = 0
            TextWidth = 0
            settings(fontChoice, scale, textHeight, TextWidth)
        if fontChoice == largeFont:
            scale = 1.3
            textHeight = -10
            TextWidth = -30
            settings(fontChoice, scale, textHeight, TextWidth)
        
    #creating the function for the settings tab, this is executed when the settings button is pressed
    def settings(fontChoice, scale, textHeight, TextWidth):
        settingsRun = True
        while settingsRun:
            
            window.fill((255,180,130))
            
            drawRectangle(15, 10, 180*scale, 85*scale, 4, (255, 150, 100)) #back button
            drawRectangle(880, 220, 90, 65, 4, (255, 150, 100)) #small font button
            drawRectangle(990, 210, 120, 85, 4, (255, 150, 100)) #default font button
            drawRectangle(1130, 200, 130, 105, 4, (255, 150, 100)) #large font button
            
            writeText("Settings", fontChoice, TEXTCOLOUR, 510+TextWidth, 50+textHeight)
            writeText("Back", fontChoice, TEXTCOLOUR, 20, 20)
            writeText("Text Size", fontChoice, TEXTCOLOUR, 505+TextWidth, 215+textHeight)
            writeText("Aa", smallFont, TEXTCOLOUR, 890, 230)
            writeText("Aa", defaultFont, TEXTCOLOUR, 1005, 220)
            writeText("Aa", largeFont, TEXTCOLOUR, 1140, 210)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    settingsRun = False
                    break
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mousePos[0] >15 and mousePos[1] >10 and mousePos[0] < 15 + 180*scale and mousePos[1] < 10 + 85*scale:
                        mainLoop(fontChoice, scale, textHeight, TextWidth, fps, dt)
                        
                    if mousePos[0] >850 and mousePos[1] >200 and mousePos[0] < 980 and mousePos[1] < 285:
                        fontChoice = smallFont
                        changeScale(scale, fontChoice, textHeight, TextWidth)
                    if mousePos[0] >990 and mousePos[1] >200 and mousePos[0] < 1120 and mousePos[1] < 285:
                        fontChoice = defaultFont
                        changeScale(scale, fontChoice, textHeight, TextWidth)
                    if mousePos[0] >1130 and mousePos[1] >200 and mousePos[0] < 1260 and mousePos[1] < 285:
                        fontChoice = largeFont
                        changeScale(scale, fontChoice, textHeight, TextWidth)
            
            mousePos = pygame.mouse.get_pos()
        
            pygame.display.update()
            
        pygame.quit()
    
    #creating the function for the simulation, this will execute when the start button is pressed
    def start(gravity, friction, elasticity, planetColour, fps, dt):
        
        shapes = []
        
        def draw(space, window, drawOptions, line, fpsCount, controlVisibility, slingCheck, squareCheck, circleCheck, triangleCheck, rectangleCheck, squareX, squareY, rectX, rectY):
            window.fill(planetColour)
            space.debug_draw(drawOptions)
            
            if line:
                pygame.draw.line(window, "black", line[0], line[1], 3)
                
            if slingCheck:
                pygame.draw.circle(window, TEXTCOLOUR, pygame.mouse.get_pos(), 30, 2)
                
            if squareCheck:
                pygame.draw.rect(window, TEXTCOLOUR, pygame.Rect(squareX, squareY, 50, 50),  2)
            
            if circleCheck:
                pygame.draw.circle(window, TEXTCOLOUR, pygame.mouse.get_pos(), 25, 2)
                
            if triangleCheck:
                pygame.draw.polygon(window, TEXTCOLOUR, [[pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]-25], [pygame.mouse.get_pos()[0]-25, pygame.mouse.get_pos()[1]+25], [pygame.mouse.get_pos()[0]+25, pygame.mouse.get_pos()[1]+25]], 2)
                
            if rectangleCheck:
                pygame.draw.rect(window, TEXTCOLOUR, pygame.Rect(rectX, rectY, 200, 50),  2)
            
            if controlVisibility:
                writeText("slingshot [1]", pygame.font.SysFont("Arial Rounded MT Bold", 25), TEXTCOLOUR, 22, 22)
                writeText("square [2]", pygame.font.SysFont("Arial Rounded MT Bold", 25), TEXTCOLOUR, 22, 42)
                writeText("circle [3]", pygame.font.SysFont("Arial Rounded MT Bold", 25), TEXTCOLOUR, 22, 62)
                writeText("triangle [4]", pygame.font.SysFont("Arial Rounded MT Bold", 25), TEXTCOLOUR, 22, 82)
                writeText("rectangle [5]", pygame.font.SysFont("Arial Rounded MT Bold", 25), TEXTCOLOUR, 22, 102)
                writeText("delete previous [backspace]", pygame.font.SysFont("Arial Rounded MT Bold", 25), TEXTCOLOUR, 22, 122)
                
                writeText("pause/unpause [p]", pygame.font.SysFont("Arial Rounded MT Bold", 25), TEXTCOLOUR, 22, 142)
                writeText("reset [r]", pygame.font.SysFont("Arial Rounded MT Bold", 25), TEXTCOLOUR, 22, 162)
                writeText("main menu [escape]", pygame.font.SysFont("Arial Rounded MT Bold", 25), TEXTCOLOUR, 22, 182)
            
                writeText("show/hide controls [shift]", pygame.font.SysFont("Arial Rounded MT Bold", 25), TEXTCOLOUR, 22, 202)
                
                writeText("0.5x speed [LEFT]", pygame.font.SysFont("Arial Rounded MT Bold", 25), TEXTCOLOUR, 22, 722)
                writeText("1x speed [UP]", pygame.font.SysFont("Arial Rounded MT Bold", 25), TEXTCOLOUR, 22, 742)
                writeText("2x speed [RIGHT]", pygame.font.SysFont("Arial Rounded MT Bold", 25), TEXTCOLOUR, 22, 762)
            
            writeText(fpsCount, pygame.font.SysFont("Arial Rounded MT Bold", 30), TEXTCOLOUR, 1276, 2)
                
            pygame.display.update()
        
        def createUserBall(space, radius, mass, pos, elasticity, friction):
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = pos
            shape = pymunk.Circle(body, radius)
            shape.mass = mass
            shape.elasticity = elasticity
            shape.friction = friction
            shape.color = random.choice(colours)
            space.add(body, shape)
            return shape
            
        def createBall(space, radius, mass, pos, elasticity, friction):
            body = pymunk.Body()
            body.position = pos
            shape = pymunk.Circle(body, radius)
            shape.mass = mass
            shape.elasticity = elasticity
            shape.friction = friction
            shape.color = random.choice(colours)
            space.add(body, shape)
            return shape
        
        def createRectangle(space, length, width, mass, pos, elasticity, friction):
            shape = pymunk.Poly.create_box(None, size=(length, width))
            moment = pymunk.moment_for_poly(mass, shape.get_vertices())
            body = pymunk.Body(mass, moment)
            shape.body = body
            body.position = pos
            shape.elasticity = elasticity
            shape.friction = friction
            shape.color = random.choice(colours)
            space.add(body, shape)
            return shape
        
        def createTriangle(space, base, height, mass, pos, elasticity, friction):
            shape = pymunk.Poly(None, ((base/2, -height), (0, 0), (base, 0)))
            moment = pymunk.moment_for_poly(mass, shape.get_vertices())
            body = pymunk.Body(mass, moment)
            body.position = pos
            shape.body = body
            shape.elasticity = elasticity
            shape.friction = friction
            shape.color = random.choice(colours)
            space.add(body, shape)
            return shape
        
        def createBoundary(space, width, height, friction, elasticity):
            rects = [
                [(width/2, height - 10), (width, 20)],
                [(width/2, 10), (width, 20)],
                [(10, height/2), (20, height)],
                [(width - 10, height/2), (20, height)]
            ]
            
            for pos, size in rects:
                body = pymunk.Body(body_type=pymunk.Body.STATIC)
                body.position = pos
                shape = pymunk.Poly.create_box(body, size)
                shape.friction = friction
                shape.elasticity = elasticity
                space.add(body, shape)
                
            return shape
        
        def calculateDistance(p1, p2):
            return math.sqrt((p1[1] - p2[1])**2 + (p2[0] - p1[0])**2)

        def calculateAngle(p1, p2):
            return math.atan2(p2[1] - p1[1], p2[0] - p1[0])
        
        def pause():
            paused = True
            while paused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        paused = False
                
                writeText("PAUSED", pygame.font.SysFont("Arial Rounded MT Bold", 50), TEXTCOLOUR, 550, 350)
                
        def run(window, width, height, fps, dt):
            simRun = True
            clock = pygame.time.Clock()
            
            slingCheck = True
            squareCheck = False
            circleCheck = False
            triangleCheck = False
            rectangleCheck = False
            
            controlVisibility = True
            
            space = pymunk.Space()
            space.gravity = (0, gravity)
                
            createBoundary(space, width, height, friction, elasticity)
            
            drawOptions = pymunk.pygame_util.DrawOptions(window)
            
            pressedPos = None
            ball = None
            
            while simRun:
                line = None
                if ball and pressedPos:
                    line = [pressedPos, pygame.mouse.get_pos()]
                    
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        simRun = False
                        break         
                    
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                        squareCheck = False
                        circleCheck = False
                        triangleCheck = False
                        slingCheck = True
                        rectangleCheck = False
                        
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                        squareCheck = True
                        circleCheck = False
                        triangleCheck = False
                        slingCheck = False
                        rectangleCheck = False
                        
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                        circleCheck = True
                        triangleCheck = False
                        squareCheck = False
                        slingCheck = False
                        rectangleCheck = False
                        
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                        triangleCheck = True
                        squareCheck = False
                        circleCheck = False
                        slingCheck = False
                        rectangleCheck = False
                    
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_5:
                        triangleCheck = False
                        squareCheck = False
                        circleCheck = False
                        slingCheck = False
                        rectangleCheck = True
                        
                    
                    if event.type == pygame.MOUSEBUTTONDOWN and squareCheck == True:
                        shapes.append(createRectangle(space, 50, 50, 10, pygame.mouse.get_pos(), 0.5, 0.5))
                            
                    if event.type == pygame.MOUSEBUTTONDOWN and circleCheck == True:
                        shapes.append(createBall(space, 25, 10, pygame.mouse.get_pos(), 0.5, 0.5))
                            
                    if event.type == pygame.MOUSEBUTTONDOWN and triangleCheck == True:
                        trianglePos = tuple(map(lambda i, j: i + j, pygame.mouse.get_pos(), [-25, 25]))
                        shapes.append(createTriangle(space, 50, 50, 10, trianglePos, 0.5, 0.5))
                    
                    if event.type == pygame.MOUSEBUTTONDOWN and rectangleCheck == True:
                        shapes.append(createRectangle(space, 200, 50, 10, pygame.mouse.get_pos(), 0.5, 0.5))
                        
                    if event.type == pygame.MOUSEBUTTONDOWN and slingCheck == True:
                        
                        if not ball:
                            pressedPos = pygame.mouse.get_pos()
                            ball = createUserBall(space, 30, 10, pressedPos, 0.8, 0.5)
                        elif pressedPos:
                            ball.body.body_type = pymunk.Body.DYNAMIC
                            angle = calculateAngle(*line)
                            force = calculateDistance(*line) * 80
                            ball.body.apply_impulse_at_local_point((math.cos(angle) * -force, math.sin(angle) * -force), (0, 0))
                            pressedPos = None
                        else:
                            space.remove(ball, ball.body)
                            ball = None
                    
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                        if len(shapes) > 0:
                            space.remove(shapes[-1], shapes[-1].body)
                            shapes.pop(-1)            
                            
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        start(981, 0.5, 0.8, planetColour, fps, dt)
                    
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        pause()
                        
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                        dt = 0.5/fps
                        
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                        dt = 1/fps
                        
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                        dt = 2/fps
                        
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        mainLoop(fontChoice, scale, textHeight, TextWidth, fps, dt)
                        
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
                        controlVisibility = not controlVisibility
                    
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_RSHIFT:
                        controlVisibility = not controlVisibility
                
                fpsCount = str(math.floor(clock.get_fps()))
                
                squareX = pygame.mouse.get_pos()[0]-25
                squareY = pygame.mouse.get_pos()[1]-25
                
                rectX = pygame.mouse.get_pos()[0]-100
                rectY = pygame.mouse.get_pos()[1]-25
                
                draw(space, window, drawOptions, line, fpsCount, controlVisibility, slingCheck, squareCheck, circleCheck, triangleCheck, rectangleCheck, squareX, squareY, rectX, rectY)
                space.step(dt)
                clock.tick(fps)
            
            pygame.quit()

        run(window, WIDTH, HEIGHT, fps, dt)
            
    #creating the mainloop for the game, this is where everything will be called and executed
    run = True
    while run:
        #filling the window with the colour corresponding to the rgb values below
        window.fill((255,180,130))
        
        #executing the functions to draw all of the text, shapes, and images
        if gamePause == True:
            pass
        else:
            drawRectangle(40, 190, 310*scale, 85*scale, 4, (255, 150, 100)) #settings button
            drawRectangle(40, 340, 180*scale, 85*scale, 4, (255, 150, 100)) #start button
            drawRectangle(40, 670, 155*scale, 85*scale, 4, (255, 150, 100)) #exit button
            
            writeText("2D Physics Simulator", fontChoice, TEXTCOLOUR, 50, 50+textHeight)
            writeText("Settings", fontChoice, TEXTCOLOUR, 45, 200)
            writeText("Start", fontChoice, TEXTCOLOUR, 45, 350)
            writeText("Planet:", fontChoice, TEXTCOLOUR, 675+TextWidth, 200+textHeight)
            writeText("Exit", fontChoice, (234, 77, 61), 45, 680)
            
            addImage("planet1.png", 600, 275)
            addImage("leftArrow.jpg", 400, 375)
            addImage("rightArrow.jpg", 1000, 375)
            addImage("rocket.jpg", 1050, 50)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            #giving the buttons their functionality
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mousePos[0] >40 and mousePos[1] >670 and mousePos[0] < 40 + 155*scale and mousePos[1] < 670 + 85*scale:
                    pygame.quit()
                
                if mousePos[0] >40 and mousePos[1] >190 and mousePos[0] < 40 +310*scale and mousePos[1] < 190 + 85*scale:
                    settings(fontChoice, scale, textHeight, TextWidth)

                if mousePos[0] >40 and mousePos[1] >340 and mousePos[0] < 40+ 180*scale and mousePos[1] < 340 + 85*scale:
                    start(981, 0.5, 0.5, planetColour, fps, dt)
        
        #gets the coordinates of the mouse
        mousePos = pygame.mouse.get_pos()
        
        pygame.display.update()

    #quits the program when broken out of the while loop above, will only happen when the x button in the top right is pressed
    pygame.quit()

mainLoop(fontChoice, scale, textHeight, TextWidth, fps, dt)