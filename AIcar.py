import pygame
import math
import sys
import time
import random
import pdb



# Pygame Init
init_status = pygame.init()
if init_status[1] > 0:
    print("(!) Had {0} initialising errors, exiting... ".format(init_status[1]))
    sys.exit()
else:
    print("(+) Pygame initialised successfully ")

# Play Surface
size = width, height = 640, 640 
playSurface = pygame.display.set_mode(size)
pygame.display.set_caption("AIcar")

# Colors
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
brown = pygame.Color(165, 42, 42)
# FPS controller
fpsController = pygame.time.Clock()

# Game settings
carPos = [200, 200]
carDir = 0
V = 5 
circleR = 90
carTurn = 'FORWARD'
carRun = 'STOP'

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				carTurn = 'LEFT'
			if event.key == pygame.K_RIGHT:
				carTurn = 'RIGHT'
			if event.key == pygame.K_UP:
				carRun = 'RUN'
			if event.key == pygame.K_ESCAPE:
				pygame.event.post(pygame.event.Event(pygame.QUIT))

		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				carTurn = 'FORWARD'
			if event.key == pygame.K_UP:
				carRun = 'STOP'

	
	#pdb.set_trace()
	if carRun == 'STOP':
		V = 0
	else:
		V = 5
		Yspeed = V*math.sin(carDir)
		Xspeed = V*math.cos(carDir)
		if carTurn == 'FORWARD':
			carPos[0] += Xspeed
			carPos[1] += Yspeed
		else:
			therta = V/float(circleR)
			Xcar = circleR-circleR*math.cos(therta)
			Ycar = circleR*math.sin(therta)


			cosT = Yspeed/float(V) 
			sinT = Xspeed/float(V)

			carPos[0] = Xcar*cosT + Ycar*sinT + carPos[0]
			carPos[1] = Xcar*sinT + Ycar*cosT + carPos[1]

			if carTurn == 'RIGHT':
				carDir += therta	
			elif carTurn == 'LEFT':
				carDir -= therta

	playSurface.fill(white)
	pygame.draw.line(playSurface, black, carPos, [carPos[0]+int(V*math.cos(carDir)*5), carPos[1]+int(V*math.sin(carDir)*5)], 1)
	pygame.draw.circle(playSurface, black, [int(round(carPos[0])), int(round(carPos[1]))], 10, 1)
	pygame.display.flip()

	fpsController.tick(20)
