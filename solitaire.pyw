"""Run this file to play the game."""
from layout import Layout
import pygame
import sys

class Solitaire():
	
	def __init__(self):
		self.screen = pygame.display.set_mode((1000, 600))
		self.screen.fill((0,100,0)) 
		self.layout = Layout(self.screen)

	def check_events(self):
		"""Checks user inputs."""
		while True:
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				if event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					if self.layout.pile_clicked is None:
						self.layout.click(pos)
					else:
						self.layout.move_to(pos)
					if self.layout.game_over():
						self.end_game()
						
	def end_game(self):
		"""Displays a message telling the user they won."""
		
		string = 'YOU WON!'
		font = pygame.font.Font('freesansbold.ttf', 100)
		text = font.render(string, True, (255,0,0))
		width, height = font.size(string)
		x, y = self.screen.get_size()	
		x -= width
		x /= 2
		y -= height
		y /= 2
		self.screen.blit(text, (x, y))
		
		while True:
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

def main():
	pygame.init()
	solitaire = Solitaire()
	solitaire.check_events()

if __name__ == "__main__":
	main()
