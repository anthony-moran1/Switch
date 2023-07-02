import pygame
pygame.init()

from random import randint, uniform
def randExclude(x, r, lr, ur):
	num = None
	while num == x or num is None:
		num = r(lr, ur)
	return num

clock = pygame.time.Clock()
FPS = 30

screenWidth = 640
screenHeight = 480
screen = pygame.display.set_mode((screenWidth, screenHeight))

black = (0,0,0)
brightBlack = (50,50,50)
grey = (128,128,128)
white = (205,205,205)

red = (255,0,0)
orange = (255,128,0)
green = (0,255,0)
blue = (0,0,255)

font = pygame.font.Font("FreeSansBold.ttf", 18)
bigFont = pygame.font.Font("FreeSansBold.ttf", 22)
def text(msg, x, y, fnt=font):
	message = fnt.render(msg, True, Players[sp].colour)
	screen.blit(message, (x, y))

def boxText(msg, x, y, fnt=font):
	w, h = fnt.size(msg)
	rect = pygame.Rect(x, y, w+8, h+4)

	if msg not in Texts:
		Texts.append(rect)

class GUIButton:
	def __init__(self, x, y, name, tempmes):
		GUIButtons.append(self)

		self.name = name
		self.msg = ""

		self.x, self.y = x, y
		self.w, self.h = font.size(tempmes)
		self.rect = pygame.Rect(self.x, self.y, self.w+8, self.h+4)

		self.blit = True
		self.clickMax = self.clickCool = 1

	def Loop(self):
		global level
		if self.name == "Level":
			self.msg = "Level "+str(level)

		if self.name == "Colour":
			if Players[sp].colour == white:
				self.msg = "White"
			if Players[sp].colour == black:
				self.msg = "Black"

			self.rect.right = screenWidth-4
			self.rect.top = 4

			if len(Players) <= 1:
				self.blit = False
			if len(Players) > 1:
				self.blit = True

		if self.name == "Restart":
			self.msg = "Restart"

		mousex, mousey = pygame.mouse.get_pos()
		ml, mm, mr = pygame.mouse.get_pressed()
		alpha = 160

		if self.clickCool < self.clickMax:
			if ml == False:
				self.clickCool += 1
		if self.clickCool > self.clickMax:
			self.clickCool = self.clickMax

		if mousex > self.rect.left and mousex < self.rect.right:
			if mousey > self.rect.top and mousey < self.rect.bottom:
				alpha = 64

				if ml:
					if self.clickCool == self.clickMax:
						if self.name == "Colour":
							if len(Players) > 1:
								SwitchPlayer()

						if self.name == "Restart":
							Level(level)

						self.clickCool = 0

		self.w, self.h = font.size(self.msg)
		self.rect = pygame.Rect(self.rect.x, self.rect.y, self.w+8, self.h+4)

		if self.blit == True:
			s = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
			s.fill((Players[sp].colour[0], Players[sp].colour[1], Players[sp].colour[2], alpha))
			screen.blit(s, (self.rect.x, self.rect.y))
			pygame.draw.rect(screen, (Players[sp].colour[0], Players[sp].colour[1], Players[sp].colour[2], alpha), self.rect, 1)

			text(self.msg, self.rect.x+4, self.rect.y+2)

class TypeTextPoint:
	def __init__(self, msg, x, y, fnt=font):
		TypeTexts.append(self)

		self.msg = msg
		self.fnt = fnt

		self.currentMessage = ""
		self.count = 0

		self.x = x
		self.y = y

		self.colour = Players[sp].colour

	def Loop(self):
		if self.colour == Players[sp].colour:
			w, h = self.fnt.size(self.currentMessage)
			x, y = self.x-w/2, self.y

			self.rect = pygame.Rect(x, y, w, h)
			if self.rect.x < 0:
				self.rect.x = 0
			if self.rect.right > screenWidth:
				self.rect.right = screenWidth

			if self.currentMessage != self.msg:
				if self.count % 2 == 0:
					self.currentMessage += self.msg[len(self.currentMessage)]

				self.count += 1

			text(self.currentMessage, self.rect.x, self.rect.y, self.fnt)

class TypeTextPlayer:
	def __init__(self, msg, who, fnt=font):
		TypeTexts.append(self)
		self.who = who

		self.currentMessage = ""
		self.maxMessage = msg

		self.count = 0
		self.colour = Players[sp].colour

	def Loop(self):
		if self.colour == Players[sp].colour:
			w, h = font.size(self.currentMessage)
			x, y = self.who.rect.centerx-w/2, self.who.rect.top-h-4

			self.rect = pygame.Rect(x, y, w, h)
			if self.rect.left < 0:
				self.rect.left = 0
			if self.rect.right > screenWidth:
				self.rect.right = screenWidth

			if self.rect.top < 0:
				self.rect.top = 0
			if self.rect.bottom > screenHeight:
				self.rect.bottom = screenHeight

			if self.currentMessage != self.maxMessage:
				if self.count % 2 == 0:
					self.currentMessage += self.maxMessage[len(self.currentMessage)]

				self.count += 1

			text(self.currentMessage, self.rect.x, self.rect.y)

def Outside(self):
	if self.rect.left < 0:
		self.rect.left = 0
	if self.rect.right > screenWidth:
		self.rect.right = screenWidth

	if self.rect.top < 0:
		self.rect.top = 0
	if self.rect.bottom > screenHeight:
		self.rect.bottom = screenHeight

class Player:
	def __init__(self, x, y, w, h, colour, alpha):
		Players.append(self)
		self.collide = True

		self.Shadows = []
		self.rect = pygame.Rect(x, y, w, h)

		self.opoColour = (255-colour[0], 255-colour[1], 255-colour[2])
		self.colour = colour
		self.alpha = alpha

		self.lp = self.rp = self.up = self.dp = 0
		self.mk = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
		self.pmk = [self.lp, self.rp, self.up, self.dp]

		self.hspd = 6
		self.vspd = 4

		self.facing = "Right"
		self.finish = False

	def Input(self):
		global sp
		if sp == Players.index(self):
			if e.type == pygame.KEYDOWN:
				for k in range(len(self.mk)):
					if e.key == self.mk[k]:
						self.pmk[k] = 1
						if k == 0:
							self.facing = "Left"
						if k == 1:
							self.facing = "Right"
						if k == 2:
							self.facing = "Up"
						if k == 3:
							self.facing = "Down"

			if e.type == pygame.KEYUP:
				for k in range(len(self.mk)):
					if e.key == self.mk[k]:
						self.pmk[k] = 0

	def Collide(self, e, i, x, y):
		if i.collide == True:
			xx = yy = 0

			if x < 0:
				xx = randint(1, 2)
			if x > 0:
				xx = randint(-2, -1)

			if y < 0:
				yy = randint(1, 2)
			if y > 0:
				yy = randint(-2, -1)

			Particles(self.colour, randint(self.rect.left, self.rect.right), randint(self.rect.top, self.rect.bottom), xx, yy)

		if e == Buttons:
			if i.colour == self.colour:
				if i.wall in Walls:
					Walls.remove(i.wall)

		if e == Blocks:
			if i.colour == self.colour:
				i.MoveSingleAxis(x/2, 0)
				i.MoveSingleAxis(0, y/2)

				if x < 0:
					self.rect.left = i.rect.right
				if x > 0:
					self.rect.right = i.rect.left

				if y < 0:
					self.rect.top = i.rect.bottom
				if y > 0:
					self.rect.bottom = i.rect.top

		if e == Targets:
			if i.colour == self.colour:
				self.finish = True

				global level
				if level == 6 and Players[1].finish == False:
					msg = "Press Spacebar"
					if len(TypeTexts) == 0:
						TypeTextPoint(msg, Targets[0].rect.centerx, Targets[0].rect.centery-64)

	def NotCollide(self, e, i):
		if e == Buttons:
			if i.colour == self.colour:
				if i.hold == True:
					if i.wall not in Walls:
						go = True
						for b in Blocks:
							if b.rect.colliderect(i):
								go = False
						if go:
							Walls.append(i.wall)

		if e == Targets:
			if i.colour == self.colour:
				self.finish = False

	def MoveSingleAxis(self, x, y):
		if x != 0:
			self.rect.x += x

			for e in Everythings:
				for i in e:
					if i == self:
						continue
					if i.colour != self.colour:
						continue

					if i.collide == False and e != Buttons and e != Targets:
						continue

					if self.rect.colliderect(i):
						if i.collide == True:
							if x < 0:
								self.rect.left = i.rect.right
							if x > 0:
								self.rect.right = i.rect.left

						self.Collide(e, i, x, y)

					else:
						self.NotCollide(e, i)

		if y != 0:
			self.rect.y += y

			for e in Everythings:
				for i in e:
					if i == self:
						continue
					if i.colour != self.colour:
						continue

					if i.collide == False and e != Buttons and e != Targets:
						continue

					if self.rect.colliderect(i):
						if i.collide == True:
							if y < 0:
								self.rect.top = i.rect.bottom
							if y > 0:
								self.rect.bottom = i.rect.top

						self.Collide(e, i, x, y)

					else:
						self.NotCollide(e, i)

	def Loop(self):
		Outside(self)
		if sp == Players.index(self):
			self.alpha = 255

			s = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
			s.fill((self.colour[0], self.colour[1], self.colour[2], self.alpha))

			screen.blit(s, (self.rect.x, self.rect.y))

			xchange = (self.pmk[1]-self.pmk[0])*self.hspd
			ychange = (self.pmk[3]-self.pmk[2])*self.vspd

			self.MoveSingleAxis(xchange, 0)
			self.MoveSingleAxis(0, ychange)

		if sp != Players.index(self):
			self.alpha = 64

		for s in self.Shadows:
			s.Loop()

def SwitchPlayer():
	global sp

	pastPlayer = Players[sp]
	if sp < len(Players)-1:
		sp += 1
	else:
		sp = 0

	for a in Everythings:
		for b in a:
			if b == Players[sp]:
				continue
			if b.colour != Players[sp].colour:
				continue

			if Players[sp].rect.colliderect(b):
				if b.collide == True:
					if sp == 0:
						sp = len(Players)-1
					else:
						sp -= 1

					break

	for k in range(len(Players[sp].pmk)):
		Players[sp].pmk[k] = pastPlayer.pmk[k]

class Shadow:
	def __init__(self, owner):
		owner.Shadows.append(self)
		self.collide = False

		self.owner = owner
		self.rect = pygame.Rect(owner.rect)

		self.colour = owner.colour
		self.alpha = owner.alpha/2

	def Loop(self):
		if Players[sp].colour == self.colour:
			s = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
			s.fill((self.colour[0], self.colour[1], self.colour[2], self.alpha))

			screen.blit(s, (self.rect.x, self.rect.y))

		self.alpha -= 2

		if self.alpha <= 0:
			self.owner.Shadows.remove(self)

class Wall:
	def __init__(self, x, y, w, h, colour, alpha):
		Walls.append(self)

		self.rect = pygame.Rect(x, y, w, h)
		self.collide = True

		self.colour = colour
		self.alpha = alpha

	def Loop(self):
		if Players[sp].colour == self.colour:
			s = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
			s.fill((self.colour[0], self.colour[1], self.colour[2], self.alpha))

			screen.blit(s, (self.rect.x, self.rect.y))

class Button:
	def __init__(self, x, y, w, h, colour, alpha, wall, hold=False):
		Buttons.append(self)
		self.rect = pygame.Rect(x, y, w, h)

		self.colour = colour
		self.opoColour = (255-colour[0], 255-colour[1], 255-colour[2])
		self.alpha = alpha

		self.wall = wall
		self.hold = hold

		self.collide = False

	def Loop(self):
		if Players[sp].colour == self.colour:
			if self.hold == False:
				fill = 0
			if self.hold == True:
				if self.wall in Walls:
					fill = 1
				if self.wall not in Walls:
					fill = 0

			pygame.draw.circle(screen, self.colour, (self.rect.centerx, self.rect.centery), int(self.rect.w/2), fill)

class Block:
	def __init__(self, x, y, w, h, colour, alpha):
		Blocks.append(self)
		self.rect = pygame.Rect(x, y, w, h)

		self.colour = colour
		self.alpha = alpha

		self.collide = True

	def Collide(self, e, i):
		if e == Buttons:
			if i.colour == self.colour:
				if i.wall in Walls:
					Walls.remove(i.wall)

	def NotCollide(self, e, i):
		if e == Buttons:
			if i.colour == self.colour:
				if i.hold == True:
					if i.wall not in Walls:
						Walls.append(i.wall)

	def MoveSingleAxis(self, x, y):
		if x != 0:
			self.rect.x += x

			for e in Everythings:
				for i in e:
					if i == self or e == Players:
						continue
					if i.colour != self.colour:
						continue

					if self.rect.colliderect(i):
						if i.collide == True:
							if x < 0:
								self.rect.left = i.rect.right
							if x > 0:
								self.rect.right = i.rect.left

						self.Collide(e, i)

					else:
						self.NotCollide(e, i)

		if y != 0:
			self.rect.y += y

			for e in Everythings:
				for i in e:
					if i == self or e == Players:
						continue
					if i.colour != self.colour:
						continue

					if self.rect.colliderect(i):
						if i.collide == True:
							if y < 0:
								self.rect.top = i.rect.bottom
							if y > 0:
								self.rect.bottom = i.rect.top

						self.Collide(e, i)

					else:
						self.NotCollide(e, i)

	def Loop(self):
		Outside(self)
		if Players[sp].colour == self.colour:
			s = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
			s.fill((self.colour[0], self.colour[1], self.colour[2], self.alpha))

			screen.blit(s, (self.rect.x, self.rect.y))

		for e in Everythings:
			for i in e:
				if self.rect.colliderect(i):
					self.Collide(e, i)

class Target:
	def __init__(self, x, y, w, h, colour, alpha):
		Targets.append(self)

		self.rect = pygame.Rect(x, y, w, h)
		self.collide = False

		self.colour = colour
		self.opoColour = (255-self.colour[0], 255-self.colour[1], 255-self.colour[2])
		self.alpha = alpha

	def Loop(self):
		if Players[sp].colour == self.colour:
			pygame.draw.rect(screen, self.colour, self.rect, 1)

class Particle:
	def __init__(self, x, y, s, xchange, ychange, colour, lt):
		parties.append(self)
		self.rect = pygame.Rect(x-s/2, y-s/2, s, s)

		self.xchange = xchange
		self.ychange = ychange

		self.colour = colour

		self.lifeTime = FPS*lt
		self.currentLifeTime = 0

		self.collide = False

	def Loop(self):
		pygame.draw.rect(screen, self.colour, self.rect)

		self.rect.x += self.xchange
		self.rect.y += self.ychange

		if self.currentLifeTime < self.lifeTime:
			self.currentLifeTime += 1
		else:
			parties.remove(self)

def Particles(col, x, y, xchange, ychange):
	for i in range(1):
		Particle(x, y, randint(4, 8), xchange, ychange, col, uniform(.3, .6))

parties = []

sp = 0
Players = []
Targets = []

Levels = []
GUIButtons = []

Walls = []
Buttons = []
Blocks = []

Everythings = [Players, Targets, Walls, Buttons, Blocks, parties]

Texts = []
TypeTexts = []
Writings = [Texts, TypeTexts]

def Level(level):
	if level not in Levels:
		Levels.append(level)

	for e in Everythings:
		for i in range(len(e)):
			del e[0]

	for w in Writings:
		for i in range(len(w)):
			del w[0]

	if level > 0:
		P1 = Player(0, 0, 32, 32, white, 128)
		P1.rect.centerx = screenWidth/2
		P1.rect.centery = screenHeight/2

		if level > 5:
			P2 = Player(0, 0, 32, 32, black, 128)
			P2.rect.centerx = screenWidth/2
			P2.rect.centery = screenHeight/2

		global sp
		sp = 0

	if level == 1:
		P1.rect.left = screenWidth*.25
		P1.rect.centery = screenHeight/2

		t = Target(0, 0, 32, 32, white, 160)
		t.rect.right = screenWidth*.75
		t.rect.centery = screenHeight/2

	if level == 2:
		P1.rect.right = screenWidth*.75
		P1.rect.centery = screenHeight/2

		t = Target(0, 0, 32, 32, white, 160)
		t.rect.left = screenWidth*.25
		t.rect.centery = screenHeight/2

		w = Wall(0, 0, 2, screenHeight-P1.rect.h*2, white, 160)
		w.rect.centerx = screenWidth/2
		w.rect.centery = screenHeight/2

	if level == 3:
		P1.rect.left = screenWidth*.25
		P1.rect.centery = screenHeight/2

		t = Target(0, 0, 32, 32, white, 160)
		t.rect.centerx = screenWidth/2
		t.rect.bottom = screenHeight*.75

		w = Wall(0, 0, screenWidth, 2, white, 160)
		w.rect.left = 0
		w.rect.top = P1.rect.bottom+P1.rect.h

		b = Button(0, 0, 32, 32, white, 160, w, False)
		b.rect.centerx = screenWidth/2
		b.rect.bottom = b.wall.rect.top-b.rect.h

	if level == 4:
		P1.rect.centerx = screenWidth/2
		P1.rect.bottom = screenHeight*.75

		t = Target(0, 0, 32, 32, white, 160)
		t.rect.centerx = screenWidth/2
		t.rect.top = screenHeight*.25

		w = Wall(0, 0, screenWidth-P1.rect.w*2, 2, white, 160)
		w.rect.centerx = screenWidth/2
		w.rect.centery = screenHeight/2

		b = Button(0, 0, 32, 32, white, 160, w, True)
		b.rect.centerx = screenWidth/2
		b.rect.top = w.rect.bottom+b.rect.h*1.5

	if level == 5:
		P1.rect.centerx = screenWidth/2
		P1.rect.top = screenHeight*.25

		t = Target(0, 0, 32, 32, white, 160)
		t.rect.centerx = screenWidth/2
		t.rect.bottom = screenHeight*.75

		w = Wall(0, 0, screenWidth, 2, white, 160)
		w.rect.left = 0
		w.rect.centery = screenHeight/2

		b = Button(0, 0, 32, 32, white, 160, w, True)
		b.rect.centerx = screenWidth/2
		b.rect.bottom = w.rect.top-b.rect.h*1.5

		bb = Block(0, 0, 32, 32, white, 160)
		bb.rect.left = b.rect.right+bb.rect.w*2
		bb.rect.centery = b.rect.centery

	if level == 6:
		P1.rect.centerx = P2.rect.centerx = screenWidth/2
		P1.rect.bottom = P2.rect.bottom = screenHeight*.75

		t = Target(0, 0, 32, 32, white, 160)
		t2 = Target(0, 0, 32, 32, black, 160)

		t.rect.centerx = t2.rect.centerx = screenWidth*.75
		t.rect.centery = t2.rect.centery = screenHeight*.25

	if level == 7:
		P1.rect.centerx = P2.rect.centerx = screenWidth*.75
		P1.rect.centery = P2.rect.centery = screenHeight*.25

		t = Target(0, 0, 32, 32, white, 160)
		t2 = Target(0, 0, 32, 32, black, 160)

		t.rect.centerx = t2.rect.centerx = screenWidth*.75
		t.rect.centery = t2.rect.centery = screenHeight*.75

		w = Wall(0, 0, 2, screenHeight/2, white, 160)
		ww = Wall(0, 0, screenWidth/2, 2, white, 160)
		ww2 = Wall(0, 0, screenWidth/2, 2, black, 160)

		w.rect.left = ww.rect.left = ww2.rect.left = screenWidth/2
		w.rect.top = 0
		ww.rect.bottom = ww2.rect.bottom = w.rect.bottom

		b2 = Button(0, 0, 32, 32, black, 160, ww, True)
		b2.rect.centerx = b2.wall.rect.centerx
		b2.rect.top = b2.wall.rect.bottom+b2.rect.h*1.5

	if level == 8:
		P1.rect.centerx = P2.rect.centerx = screenWidth/2
		P1.rect.centery = P2.rect.centery = screenHeight/2

		Target(0, screenHeight/2-16, 32, 32, white, 255)
		Target(0, screenHeight/2-16, 32, 32, black, 255)

		w = Wall(screenWidth*.75-2, 0, 4, screenHeight, white, 160)
		ww = Wall(screenWidth*.25-2, 0, 4, screenHeight, white, 160)

		ww2 = Wall(screenWidth*.25-2, 0, 4, screenHeight, black, 160)

		b = Button(0, 0, 32, 32, black, w.alpha, w, True)
		b.rect.right = w.rect.left-b.rect.w
		b.rect.centery = w.rect.centery

		bb = Button(576, screenHeight/2-16, 32, 32, white, 160, ww, True)
		bb2 = Button(32, screenHeight/2-64, 32, 32, white, 160, ww2, True)

		bl = Block(P1.rect.left-P1.rect.w*1.5, screenHeight/2-16, 32, 32, white, 128)

level = 1
Level(level)

LevelButton = GUIButton(4, 4, "Level", "Level 1")
RestartButton = GUIButton(4, LevelButton.rect.bottom+4, "Restart", "Restart")
ColourButton = GUIButton(4, 0, "Colour", "White")

stop = False
pause = False

gameloop = True
while gameloop:
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			gameloop = False
			pygame.quit()
			stop = True

		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_SPACE:
				SwitchPlayer()

			if e.key == pygame.K_l:
				level += 1
				Level(level)
			if e.key == pygame.K_k:
				if level > 1:
					level -= 1
					Level(level)

		for p in Players:
			p.Input()

	if stop:
		break

	fill = grey
	screen.fill(fill)

	for e in Everythings:
		for i in e:
			i.Loop()

	for w in Writings:
		for i in w:
			try:
				i.Loop()
			except:
				pass

	for g in GUIButtons:
		g.Loop()

	if level <= 5:
		if Players[0].finish == True:
			level += 1
			Level(level)

	if level > 5:
		if Players[0].finish == True and Players[1].finish == True:
			level += 1
			Level(level)

	clock.tick(FPS)
	pygame.display.update()