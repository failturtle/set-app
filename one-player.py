import pygame
import random

width = 1200
height = 800
win = pygame.display.set_mode((width, height))

pygame.display.set_caption("Set")

img = pygame.image.load('img/cards.png')
currentCoordinates = []
curSelected = []

pygame.font.init()
myfont = pygame.font.SysFont('Arial', 30)

CARD_WIDTH = 165
CARD_HEIGHT = 94

class card:
	def __init__(self, num = 0):
		self.num = num
		self.isSelected = 0
	def toggle(self):
		if self.isSelected:
			curSelected.remove(self.num)
		else:
			curSelected.append(self.num)
			
		self.isSelected = 1 - self.isSelected
		if len(curSelected) == 3:
			blah = curSelected
			validSet = check(blah)
			if validSet:
				return blah
			return [-1]
		return []

cards = [card(x) for x in range(81)]
random.shuffle(cards)

def isSet(a):
	if len(a) != 3:
		return False
	c0 = num_to_coordinates(a[0])
	c1 = num_to_coordinates(a[1])
	c2 = num_to_coordinates(a[2])
	for i in range(4):
		s = set()
		s.add(c0[i])
		s.add(c1[i])
		s.add(c2[i])
		if len(s) == 2:
			return False
	return True

def check(a):
	if isSet(a):
		print("SET")
		return True
	print("NOT SET")
	return False

def getImageCoordinate(a):
	# magic numbers woo
	x = 45

	y = 20
	y += 285 * a[0]
	x += 508 * a[1]
	y += 95 * a[2]
	x += 170 * a[3]
	return (x, y, CARD_WIDTH, CARD_HEIGHT)

def num_to_coordinates(k):
	ret = []
	while len(ret) < 4:
		ret.append(k % 3)
		k //= 3
	return ret

def getScreenCoordinate(idx, num_cards):
	x = idx % 3
	y = idx // 3
	xx = 320
	yy = 150 - (num_cards-12)*20

	y_offset = 150
	if num_cards > 12:
		y_offset = 130
	if num_cards > 15:
		y_offset = 118
	return (xx + x * 200, yy + y * y_offset)

def reset(ar):
	for i in ar:
		i.isSelected = 0
	global curSelected
	curSelected = []

end = 0

def redrawWindow(cards, numCardsLeft):
	# win.fill((244,230,251))
	global currentCoordinates
	global end
	win.fill((255,255,255))

	text = myfont.render('Welcome to set!', False, (0, 0, 0))
	win.blit(text, (600 - text.get_rect().width/2, 20))
	l = len(cards)
	currentCoordinates = []
	for i in range(l):
		screenCoordinate = getScreenCoordinate(i, l)
		card = num_to_coordinates(cards[i].num)

		image_props = getImageCoordinate(card)
		# print(screenCoordinate, currentCoordinates)
		currentCoordinates.append(screenCoordinate)
		if cards[i].isSelected:
			pygame.draw.rect(win, (0, 100, 255), 
					(screenCoordinate[0]-5, screenCoordinate[1]-5, CARD_WIDTH+10, CARD_HEIGHT+10), 3)  # width = 3
		win.blit(img, screenCoordinate, image_props)

	if end:
		text = myfont.render('Game Over!', False, (0, 0, 0))
		win.blit(text, (600 - text.get_rect().width/2, 700))
	text = myfont.render('Cards left: '+str(numCardsLeft), False, (0, 0, 0))
	win.blit(text, (70, 40))

	pygame.display.update()


# print(cards)


def inRange(a, b, c):
	return a <= b and b <= c

def getNextCard():
	global cards
	if len(cards) == 0:
		return False
	ret = cards[0]
	cards = cards[1:]
	return ret

def isThereASet(cur):
	for i in cur:
		for j in cur:
			for k in cur:
				if i.num != j.num and j.num != k.num and i.num != k.num and isSet((i.num, j.num, k.num)):
					return True
	return False


def main():
	global cards
	global currentCoordinates
	global end
	run = True
	curCards = cards[:12]
	cards = cards[12:]
	while run:
		while not isThereASet(curCards):
			if len(cards) == 0:
				end = 1
				break
			curCards.append(getNextCard())
			curCards.append(getNextCard())
			curCards.append(getNextCard())
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONUP:
				pos = pygame.mouse.get_pos()
				mouseX = pos[0]
				mouseY = pos[1]
				# print(pos)
				# print(len(currentCoordinates))
				for i in range(len(currentCoordinates)):
					coord = currentCoordinates[i]
					x = coord[0]
					y = coord[1]
					# print(coord)
					if inRange(x, mouseX, x+CARD_WIDTH) and inRange(y, mouseY, y+CARD_HEIGHT):
						# print("ENTERED")
						cardsToBeReplaced = curCards[i].toggle()
						entered = 0
						for x in cardsToBeReplaced:
							entered = 1
							if x == -1:
								break
							f = getNextCard()
							if f and len(curCards) <= 12:
								for i in range(len(curCards)):
									if curCards[i].num == x:
										curCards[i] = f
										break
							else:
								for i in range(len(curCards)):
									if curCards[i].num == x:
										curCards.remove(curCards[i])
										break
						if entered:
							reset(curCards)

			if event.type == pygame.QUIT:
				run = False
				pygame.quit()


		redrawWindow(curCards, len(cards))
main()