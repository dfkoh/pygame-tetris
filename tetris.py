import sys
import os

import pygame
from pygame.locals import *

from engine import TextView, ViewBase, Board, Piece, Color

_print = False

class PygameView(ViewBase):
	"""Renders a board in pygame."""

	COLOR_MAP = {
		Color.CLEAR : pygame.Color(255, 255, 255),
		Color.RED : pygame.Color(255, 0, 0),
		Color.BLUE : pygame.Color(0, 255, 0),
		Color.GREEN : pygame.Color(0, 0, 255),
		Color.YELLOW : pygame.Color(255, 255, 0),
		Color.MAGENTA : pygame.Color(255, 0, 255),
		Color.CYAN : pygame.Color(0, 255, 255),
		Color.ORANGE : pygame.Color(255, 140, 0)
	}
		
	BOARD_BORDER_SIZE = 5
	BORDER_SIZE = 4
	BORDER_FADE = pygame.Color(50, 50, 50)

	def __init__(self, surf):
		ViewBase.__init__(self)
		self.surf = surf
		self.view_width = surf.get_width()
		self.view_height = surf.get_height()
		self.box_size = 10
		self.padding = (0, 0)

	def set_size(self, cols, rows):
		ViewBase.set_size(self, cols, rows)
		self.calc_dimensions()

	def calc_dimensions(self):
		horiz_size = (self.view_width - (self.BOARD_BORDER_SIZE * 2)) // self.width
		vert_size = (self.view_height - (self.BOARD_BORDER_SIZE * 2)) // self.height

		if vert_size > horiz_size:
			self.box_size = horiz_size
			self.padding = (0, (self.view_height 
								- self.BOARD_BORDER_SIZE
							    - (self.height * horiz_size)))
		else:
			self.box_size = vert_size
			self.padding = ((self.view_width 
							 - self.BOARD_BORDER_SIZE 
							 - (self.width * vert_size)), 0)

		global _print
		if not _print:
			print(self.width, self.height)
			print(self.view_width, self.view_height)
			print(horiz_size, vert_size)
			print(self.box_size)			
			print(self.padding)
			_print = True


	def show(self):
		self.draw_board()
		pygame.display.update()

	def draw_board(self):
		bg_color = self.COLOR_MAP[Color.CLEAR]
		self.surf.fill(bg_color - self.BORDER_FADE)

		X_START = self.BOARD_BORDER_SIZE + (self.padding[1] // 2)
		Y_START = self.BOARD_BORDER_SIZE + (self.padding[0] // 2)

		x = X_START
		y = Y_START
		board_rect = (y, x, self.width * self.box_size, self.height * self.box_size)
		pygame.draw.rect(self.surf, bg_color, board_rect)
		for col in self.rows:
			for item in col:
				self.draw_box(x, y, item)
				y += self.box_size
			x += self.box_size
			y = Y_START

	def draw_box(self, x, y, color):
		if color == Color.CLEAR:
			return

		pg_color = self.COLOR_MAP[color]
		bd_size = self.BORDER_SIZE
		bd_color = pg_color - self.BORDER_FADE

		outer_rect = (y, x, self.box_size, self.box_size)
		inner_rect = (y + bd_size, x + bd_size, 
					  self.box_size - bd_size*2, self.box_size - bd_size*2)

		pygame.draw.rect(self.surf, bd_color, outer_rect)
		pygame.draw.rect(self.surf, pg_color, inner_rect)


class Tetris:

	DROP_EVENT = USEREVENT + 1

	def __init__(self, view_type):
		self.board = Board(10, 20)
		self.board.generate_piece()
		self.view_type = view_type

		if view_type == TextView:
			def cls():
				os.system('cls')
			self.show_action = cls
			self.max_fps = 5
		else:
			self.show_action = None
			self.max_fps = 50

	def key_handler(self, key):
		if key == K_LEFT:
			self.board.move_piece(-1,0)
		elif key == K_RIGHT:
			self.board.move_piece(1, 0)
		elif key == K_UP:
			self.board.rotate_piece()
		elif key == K_DOWN:
			self.board.move_piece(0, 1)
		elif key == K_a:
			self.board.rotate_piece(clockwise=False)
		elif key == K_s:
			self.board.rotate_piece()
		elif key == K_SPACE:
			self.board.full_drop_piece()

	def init(self):
		pygame.init()
		surf = pygame.display.set_mode((600, 600))
		self.view = self.view_type(surf)

	def show_colors(self):
		self.init()
		self.view.set_size(5,5)
		for i in range(4):
			self.view.render_tile(i + 1, 0, Color.colors()[i])
		self.view.show()

		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()

	def main(self):
		self.init()
		self.clock = pygame.time.Clock()
		pygame.time.set_timer(self.DROP_EVENT, 500)

		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == KEYDOWN:
					self.key_handler(event.key)
				elif event.type == self.DROP_EVENT:
					self.board.drop_piece()

			self.board.render(self.view)
			if self.show_action is not None:
				self.show_action()
			self.view.show()

			self.clock.tick(self.max_fps)


if __name__ == "__main__":
	t = Tetris(PygameView)
	t.main()
	#t.show_colors()