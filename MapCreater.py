import json
import pygame
import sys
import math

init_status = pygame.init()
if init_status[1] > 0:
    print("(!) Had {0} initialising errors, exiting... ".format(init_status[1]))
    sys.exit()

size = width, height = 1000, 1000 
playSurface = pygame.display.set_mode(size)
pygame.display.set_caption("AIcar")

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

fpsController = pygame.time.Clock()

state = 'IDLE'
walls = []
ps = [0,0]
pe = [0,0]

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			f = open("Map.json", "w+")
			f.write(json.dumps(walls))
			f.close()
			pygame.quit()
			sys.exit()

		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				if state == 'IDLE':
					state = 'DRAWING'
					ps = event.pos
				elif state == 'DRAWING':
					pe = event.pos
					walls.append((ps, pe))
					ps = pe
			elif event.button == 3:
				state = 'IDLE'

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.event.post(pygame.event.Event(pygame.QUIT))

	playSurface.fill(white)
	for sp, ep in walls:
		pygame.draw.line(playSurface, black, sp, ep, 1)
	pygame.display.flip()

	fpsController.tick(60)

#Map = [([10, 20], [20, 30]), ([40, 20], [60, 21])]
#f = open("Map.json", "w+")
#f.write(json.dumps(Map))
#f.close()
#f = open("Map.json", "r")
#Mapread = f.readline()
#Map = json.loads(Mapread)
#ps, pe = Map[0]
#print ps[1]
#f.close()
