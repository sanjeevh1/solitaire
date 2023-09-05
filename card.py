import pygame
from pygame.sprite import Sprite

class Card(Sprite):
	"""A class for objects representing playing cards."""
	
	def __init__(self, screen, suit, rank, x=0, y=0):
		super().__init__()
		self.screen = screen
		self.image = pygame.image.load('images/face_down.bmp')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		
		'''
		String representations of suits:
			's' = spades
			'c' = clubs
			'h' = hearts
			'd' = diamonds
		'''
		self.suit = suit
		self.rank = rank
		self.face_up = False
	
	def card_width():
		image = pygame.image.load('images/face_down.bmp')
		return image.get_width()
	
	def card_height():
		image = pygame.image.load('images/face_down.bmp')
		return image.get_height()
	
	def color(self):
		"""Returns the color of the card's suit."""
		if (self.suit == 's') or (self.suit == 'c'):
			return 'black'
		return 'red'
	
	def flip(self):
		"""Changes the value of self.face_up ('flips' the card)."""
		self.face_up = not self.face_up
		if self.face_up:
			image_name = 'images/' + self.suit + str(self.rank) + '.bmp'
			self.image = pygame.image.load(image_name)
		else:
			self.image = pygame.image.load('images/face_down.bmp')
		self.blitme()
	
	def blitme(self):
		"""Draws the card at its current location."""
		self.screen.blit(self.image, self.rect) 
