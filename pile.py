"""A module for the Pile class and all of its subclasses."""
from card import Card
import pygame

class Pile():
	"""A class for a pile of cards."""
	
	def __init__(self, screen, x, y, cards=None):
		#cards is a list of card objects
		#cards[0] is the bottom of the pile
		if cards is not None:
			self.cards = cards
		else:
			self.cards = []
		self.x = x
		self.y = y
		self.screen = screen
		width = Card.card_width()
		height = Card.card_height()
		self.rect = pygame.Rect(x, y, width, height)
		pygame.draw.rect(self.screen, (255,255,255), self.rect)
 
		for card in self.cards:
			card.rect.x = x
			card.rect.y = y
	
	def remove_card(self):
		"""
		Removes the top card from the pile, if possible.
		Returns the removed card.
		"""
		if len(self.cards) > 0:
			x = self.cards.pop()
			self.draw()
			return x
		self.draw()
		return None
		
	def add_card(self, card):
		"""Adds a card to the top of the pile."""
		card.rect.x = self.x
		card.rect.y = self.y
		self.cards.append(card)
		card.blitme()
		
	def can_add(self, card):
		"""
		Returns True if card can be added to top of pile.
		Returns False otherwise.
		"""
		return True
	
	def top_card(self):
		if len(self.cards) > 0:
			return self.cards[len(self.cards) - 1]
		return None
	
	def highlight(self, card):
		"""Draws a red rectangle around the selected cards."""
		pos = card.rect.topleft
		width = card.rect.width
		height = self.top_card().rect.bottom - card.rect.top
		rectangle = pygame.Rect(pos, (width, height))
		pygame.draw.rect(self.screen, (255, 0, 0), rectangle, 3)
	
	def draw(self):
		"""Draws pile on screen."""
		if self.top_card() is None:
			pygame.draw.rect(self.screen, (255,255,255), self.rect)
		else:
			self.top_card().blitme()
		
class TableauPile(Pile):

	def __init__(self, screen, x, y, cards):
		super().__init__(screen, x, y, cards) 
		for num in range(len(cards)):
			card = self.cards[num]
			card.rect.y += num * Card.card_height() / 4
		
	def remove_cards(self, n):
		"""
		Removes the top n cards from the pile.
		Returns the removed cards as a list.
		"""
		removed_cards = []
		for number in range(n):
			card = self.remove_card()
			removed_cards.insert(0, card)
			
		#Makes sure the top card of the pile faces up
		if self.top_card() is not None and not self.top_card().face_up:
			self.top_card().flip
		self.draw()
		return removed_cards
	
	def add_card(self, card):
		"""Adds a card to the top of the pile."""
		card.rect.x = self.x
		if self.top_card() is not None:
			card.rect.y = self.top_card().rect.y + Card.card_height() / 4
		else:
			card.rect.y = self.rect.y
		self.cards.append(card)
		card.blitme()
		self.draw()
		
	def add_cards(self, cards):
		""" Adds cards from list cards to pile."""
		for card in cards:
			self.add_card(card)
		
	def remove_card(self):
		"""
		Removes the top card from the pile.
		Returns the removed card.
		Flips the top card if necessary.
		"""
		card = super(TableauPile, self).remove_card()
		if self.top_card() is not None and not self.top_card().face_up:
			self.top_card().flip()
		self.draw()
		return card
		
	def can_add(self, card):
		"""
		Returns true if card is of opposite color of top card
		and lower rank by one
		or deck is empty.
		Returns false otherwise.
		"""
		if self.top_card() == None:
			if card.rank == 13:
				return True
			return False
		if card.color() == self.top_card().color():
			return False
		if card.rank == self.top_card().rank - 1:
			return True
		return False
	
	def draw(self):
		rect = pygame.Rect(self.x, self.y, self.rect.width, self.screen.get_height())
		pygame.draw.rect(self.screen, (0, 100, 0), rect)
		if self.top_card() is None:
			pygame.draw.rect(self.screen, (255,255,255), self.rect)
		for card in self.cards:
			card.blitme()
		 
		
	
class FoundationPile(Pile):
	
	def __init__(self, screen, x, y, suit):
		super().__init__(screen, x, y)
		self.suit = suit
		self.image = pygame.image.load('images/' + suit + '.bmp')
	
	def can_add(self, card):
		"""
		Returns true if card's suit matches pile's suit 
		and card has rank one higher than top card. 
		Returns false otherwise.
		"""
		if card.suit != self.suit:
			return False
		if self.top_card() is None: 
			if card.rank == 1:
				return True
			return False
		if card.rank == self.top_card().rank + 1:
			return True
		return False
	
	def draw(self):
		super().draw()
		if self.top_card() is None:
			self.screen.blit(self.image, self.rect)

class StockPile(Pile):
	
	def __init__(self, screen, x, y, cards=[]):
		super().__init__(screen, x, y, cards)
	
	def draw(self):
		super().draw()
		if self.top_card() is None:
			image = pygame.image.load('images/reset.bmp')
			rectangle = image.get_rect()
			rectangle.center = self.rect.center
			self.screen.blit(image, rectangle)		
