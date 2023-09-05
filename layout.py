from pile import *
from card import Card
import random

SUITS = ['h', 'd', 'c', 's']

class Layout():
	"""A class for keeping track of the game's piles."""
	
	def __init__(self, screen):
		self.screen = screen
		
		self.init_foundation()	
		self.init_deck()		
		self.init_tableau()
		
		#creates stock pile with remaining cards in deck
		self.stock = StockPile(self.screen, 900, 490, self.deck)
		#creates empty waste pile
		self.waste = Pile(self.screen, 800, 490)
		
		self.init_piles()
		
		#indicates pile and bottom-most card that are selected
		self.pile_clicked = None
		self.card_clicked = None
	
	def init_foundation(self):
		"""Creates the foundation."""
		self.foundation = []
		for num in range(len(SUITS)):
			suit = SUITS[num]
			pile = FoundationPile(self.screen, 10, 110 * num + 160, suit)
			self.foundation.append(pile)
	
	def init_deck(self):
		"""Creates a list of all possible cards."""		
		self.deck = []
		for suit in SUITS:
			for rank in range(1, 14):
				card = Card(self.screen, suit, rank)
				self.deck.append(card)
				
	def init_tableau(self):
		"""Creates the tableau."""
		self.tableau = []
		for pile_number in range(1, 8):
			cards = []
			for card_number in range(pile_number):
				card = random.choice(self.deck)
				self.deck.remove(card)
				cards.append(card)
			pile = TableauPile(self.screen, 100 * pile_number, 10, cards)
			pile.top_card().flip()
			self.tableau.append(pile)

	def init_piles(self):		
		"""Creates list of piles & draws all piles.""" 
		self.piles = []
		self.piles.append(self.stock)
		self.piles.append(self.waste)
		for pile in self.foundation:
			self.piles.append(pile)
		for pile in self.tableau:
			self.piles.append(pile)
		for pile in self.piles:
			pile.draw()
		
	def move_card(self, pile1, pile2):
		"""Moves top card from pile1 to pile2, if possible."""
		if (pile1 is not self.stock) and (pile2 is self.waste):
			return
		if pile2 is self.stock:
			return
		card = pile1.top_card()
		if (card is not None) and pile2.can_add(card):
			pile1.remove_card()
			pile2.add_card(card)
		if pile2 is self.waste:
			pile2.top_card().flip()
			
	def move_cards(self, tpile1, tpile2, n):
		"""Moves top n cards from tpile1 to tpile2, if possible."""
		critical_card = tpile1.cards[len(tpile1.cards) - n]
		if tpile2.can_add(critical_card):
			cards = tpile1.remove_cards(n)
			tpile2.add_cards(cards)
	
	def reset_stock(self):
		"""Moves all cards from waste to stock."""
		while self.waste.top_card() is not None:
			card = self.waste.remove_card()
			card.flip()
			self.stock.add_card(card)
		self.waste.draw()
	
	def click(self, point):
		"""selects the pile & cards that were clicked."""
		for pile in self.piles:
			if (pile in self.tableau) and (pile.top_card() is not None):
				for index in range(len(pile.cards)):
					card = pile.cards[len(pile.cards) - 1 - index]
					if card.rect.collidepoint(point) and card.face_up:
						self.pile_clicked = pile
						self.card_clicked = card
						pile.highlight(card)
						break
			elif pile is self.stock and pile.rect.collidepoint(point):
				if pile.top_card() is None:
					self.reset_stock()
				else:
					self.move_card(self.stock, self.waste)
			elif pile.rect.collidepoint(point) and pile.top_card() is not None:
				self.pile_clicked = pile
				self.card_clicked = pile.top_card()
				pile.highlight(self.card_clicked)
			
	def move_to(self, point):
		"""Moves selected cards to the pile at point."""
		for pile in self.piles:
			if pile in self.tableau and pile.top_card() is not None:
				rect = pygame.Rect(pile.x, pile.y, pile.rect.width, pile.top_card().rect.bottom - pile.y)
			else:
				rect = pile.rect
			if rect.collidepoint(point):
				 if self.pile_clicked in self.tableau and self.card_clicked is not self.pile_clicked.top_card():
						if pile in self.tableau:
							cards = self.pile_clicked.cards
							num_cards = len(cards) - cards.index(self.card_clicked)
							self.move_cards(self.pile_clicked, pile, num_cards)
							break
				 self.move_card(self.pile_clicked, pile)
				 break
				 
		self.pile_clicked.draw()
		self.pile_clicked = None
		self.card_clicked = None
	
	def game_over(self):
		"""Returns true if all cards are in the foundation."""
		for pile in self.foundation:
			if pile.top_card() is None or pile.top_card().rank != 13:
				return False		
		return True		
