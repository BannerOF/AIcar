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
size = width, height = 1000, 1000 
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

# Game data
carPos = [200, 200]
carDir = 0
V = 0 
VMAX = 5
Vdown = 0
Vup = 0
circleR = 90
carTurn = 'FORWARD'

walls = [([30, 70],[300, 200]), ([560, 700],[890, 800])]

def distancePtSeg(pt, p, q):
	pqx = q[0] - p[0]
	pqy = q[1] - p[1]
	dx = pt[0] - p[0]
	dy = pt[1] - p[1]
	d = pqx*pqx + pqy*pqy
	t = pqx*dx + pqy*dy
	if(d > 0):
		t /= d
	if(t < 0):
		t = 0
	elif(t > 1):
		t = 1	
	dx = p[0] + t*pqx - pt[0]
	dy = p[1] + t*pqy - pt[1]
	return math.sqrt(dx*dx+dy*dy)

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
				Vup = 0.05
			if event.key == pygame.K_DOWN:
				Vdown = 0.05
			if event.key == pygame.K_ESCAPE:
				pygame.event.post(pygame.event.Event(pygame.QUIT))

		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				carTurn = 'FORWARD'
			if event.key == pygame.K_UP:
				Vup = 0
			if event.key == pygame.K_DOWN:
				Vdown = 0

	
	#pdb.set_trace()
	V += Vup - Vdown - 0.01

	if V < 0:
		V = 0
	elif V > VMAX:
		V = VMAX
	
	circleR = 2 + V * 60

	if V > 0:
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

	for sp, ep in walls:
		if distancePtSeg(carPos, sp, ep) < 10:
			pygame.quit()	
			sys.exit()


	playSurface.fill(white)
	pygame.draw.line(playSurface, black, carPos, [carPos[0]+int(V*math.cos(carDir)*5), carPos[1]+int(V*math.sin(carDir)*5)], 1)
	pygame.draw.circle(playSurface, black, [int(round(carPos[0])), int(round(carPos[1]))], 10, 2)
	for sp, ep in walls:
		pygame.draw.line(playSurface, black, sp, ep, 1)
	pygame.display.flip()

	fpsController.tick(60)
