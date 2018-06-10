import pygame
import json
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

f = open("Map.json", "r")
Mapread = f.readline()
walls = json.loads(Mapread)
f.close()

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

def IsRectCross(p1, p2, q1, q2):
	return min(p1[0], p2[0]) <= max(q1[0], q2[0]) and \
		min(q1[0], q2[0]) <= max(p1[0], p2[0]) and \
		min(p1[1], p2[1]) <= max(q1[1], q2[1]) and \
		min(q1[1], q2[1]) <= max(p1[1], p2[1])

def IsLineSegmentCross(p1, p2, q1, q2):
	return (((q1[0]-p1[0])*(q1[1]-q2[1])-(q1[1]-p1[1])*(q1[0]-q2[0]))*((q1[0]-p2[0])*(q1[1]-q2[1])-(q1[1]-p2[1])*(q1[0]-q2[0]))<0 and \
		((p1[0]-q1[0])*(p1[1]-p2[1])-(p1[1]-q1[1])*(p1[0]-p2[0]))*((p1[0]-q2[0])*(p1[1]-p2[1])-(p1[1]-q2[1])*(p1[0]-p2[0]))<0)

def GetCrossPoint(p1, p2, q1, q2):
	ret = [1, 0, 0]
	if IsRectCross(p1, p2, q1, q2):
		if IsLineSegmentCross(p1, p2, q1, q2):
			tmpLeft = (q2[0]-q1[0]) * (p1[1]-p2[1]) - (p2[0]-p1[0]) * (q1[1]-q2[1])
			tmpRight = (p1[1]-q1[1]) * (p2[0]-p1[0]) * (q2[0]-q1[0]) + q1[0] * (q2[1]-q1[1]) *(p2[0]-p1[0]) - p1[0] * (p2[1]-p1[1]) * (q2[0]-q1[0])
			ret[1] = int(float(tmpRight)/float(tmpLeft))

			tmpLeft = (p1[0]-p2[0]) * (q2[1]-q1[1]) - (p2[1]-p1[1]) * (q1[0]-q2[0])
			tmpRight = p2[1] * (p1[0]-p2[0]) * (q2[1]-q1[1]) + (q2[0]-p2[0]) * (q2[1]-q1[1]) * (p1[1]-p2[1]) - q2[1] * (q1[0]-q2[0]) * (p2[1]-p1[1])
			ret[2] = int(float(tmpRight)/float(tmpLeft))

			ret[0] = 1
			return ret
	ret[0] = 0
	return ret
	

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
	
	circleR = 2 + V * 50

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
	
	P1 = [int(round(carPos[0])), int(round(carPos[1]))]
	PF = [P1[0]+int(400*math.cos(carDir)), P1[1]+int(400*math.sin(carDir))]
	PFR = [P1[0]+int(400*math.cos(carDir+math.pi/4)), P1[1]+int(400*math.sin(carDir+math.pi/4))]
	PR = [P1[0]+int(400*math.cos(carDir+math.pi/2)), P1[1]+int(400*math.sin(carDir+math.pi/2))]
	PFL = [P1[0]+int(400*math.cos(carDir-math.pi/4)), P1[1]+int(400*math.sin(carDir-math.pi/4))]
	PL = [P1[0]+int(400*math.cos(carDir-math.pi/2)), P1[1]+int(400*math.sin(carDir-math.pi/2))]
	for sp, ep in walls:
		if distancePtSeg(carPos, sp, ep) < 10:
			pygame.quit()	
			sys.exit()
		Ret = GetCrossPoint(P1, PF, sp, ep)
		if Ret[0] == 1:
			PF[0] = Ret[1]
			PF[1] = Ret[2]
		Ret = GetCrossPoint(P1, PFR, sp, ep)
		if Ret[0] == 1:
			PFR[0] = Ret[1]
			PFR[1] = Ret[2]
		Ret = GetCrossPoint(P1, PR, sp, ep)
		if Ret[0] == 1:
			PR[0] = Ret[1]
			PR[1] = Ret[2]
		Ret = GetCrossPoint(P1, PFL, sp, ep)
		if Ret[0] == 1:
			PFL[0] = Ret[1]
			PFL[1] = Ret[2]
		Ret = GetCrossPoint(P1, PL, sp, ep)
		if Ret[0] == 1:
			PL[0] = Ret[1]
			PL[1] = Ret[2]


	playSurface.fill(white)
	pygame.draw.line(playSurface, red, carPos, PF, 1)
	pygame.draw.circle(playSurface, red, PF, 3, 3)
	pygame.draw.circle(playSurface, red, PFR, 3, 3)
	pygame.draw.circle(playSurface, red, PR, 3, 3)
	pygame.draw.circle(playSurface, red, PFL, 3, 3)
	pygame.draw.circle(playSurface, red, PL, 3, 3)
	pygame.draw.circle(playSurface, black, P1, 10, 2)
	for sp, ep in walls:
		pygame.draw.line(playSurface, black, sp, ep, 1)
	pygame.display.flip()

	fpsController.tick(60)
