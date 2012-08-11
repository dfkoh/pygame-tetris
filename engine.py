
from collections import defaultdict
from random import Random

# Some interfaces
class Color:
	CLEAR = "clear"
	RED = "red"
	BLUE = "blue"
	GREEN = "green"
	YELLOW = "yellow"
	MAGENTA = "magenta"
	CYAN = "cyan"
	ORANGE = "orange"

	@staticmethod
	def colors():
		return (Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, 
			    Color.MAGENTA, Color.CYAN, Color.ORANGE)

class ViewBase:
	def __init__(self):
		self.rows = []
		self.width = 0
		self.height = 0

	def set_size(self, columns, rows):
		self.width = columns
		self.height = rows
		self.clear()

	def clear(self):
		self.rows = [[Color.CLEAR] * self.width for i in range(self.height)]

	def render_tile(self, x, y, color):
		if (0 <= x < self.width and 0 <= y < self.height):
			self.rows[y][x] = color

class TextView(ViewBase):
	"""Renders a board as text."""

	COLOR_CHAR = {
		Color.CLEAR : '.',
		Color.RED : '*',
		Color.BLUE : '#',
		Color.GREEN : 'o',
		Color.YELLOW : 'O',
		Color.MAGENTA : '%',
		Color.CYAN : '&',
		Color.ORANGE : '$',
	}

	def __init__(self, surf=None):
		ViewBase.__init__(self)

	def show(self):
		str_ = self.get_str()
		print(str_)

	def get_str(self):
		str_ = "\n"
		for column in self.rows:
			for item in column:
				str_ += TextView.COLOR_CHAR[item]
			str_ += "\n"
		return str_

class Piece:
	L_SHAPE = {"tiles" : ((0,0), (0,1), (0,2), (1,2)),
			   "x_adj" : 1,
			   "y_adj" : 2,
			   "color" : Color.RED}
	R_SHAPE = {"tiles" : ((0,0), (1,0), (0,1), (0,2)),
			   "x_adj" : 1,
			   "y_adj" : 2,
			   "color" : Color.ORANGE}
	O_SHAPE = {"tiles" : ((0,0), (0,1), (1,0), (1,1)),
			   "x_adj" : 1,
			   "y_adj" : 1,
			   "color" : Color.CYAN}
	T_SHAPE = {"tiles" : ((0,0), (1,0), (1,1), (2,0)),
			   "x_adj" : 2,
			   "y_adj" : 1,
			   "color" : Color.MAGENTA}
	S_SHAPE = {"tiles" : ((0,0), (0,1), (1,1), (1,2)),
			   "x_adj" : 1,
			   "y_adj" : 2,
			   "color" : Color.BLUE}
	Z_SHAPE = {"tiles" : ((0,0), (1,0), (1,1), (2,1)),
			   "x_adj" : 2,
			   "y_adj" : 1,
			   "color" : Color.GREEN}
	I_SHAPE = {"tiles" : ((0,0), (1,0), (2,0), (3,0)),
			   "x_adj" : 3,
			   "y_adj" : 0,
			   "color" : Color.YELLOW}
	SHAPES = (L_SHAPE, R_SHAPE, O_SHAPE, T_SHAPE, S_SHAPE, Z_SHAPE, I_SHAPE)

	def __init__(self, x, y, shape, color, rot=0):
		self.x = x
		self.y = y
		self.shape = shape
		self.color = color
		self.rotation = rot

	def move(self, x, y):
		self.x += x
		self.y += y

	def __iter__(self):
		for x_offset, y_offset in self.shape["tiles"]:
			if self.rotation == 0:
				yield (self.x + x_offset, self.y + y_offset)
			elif self.rotation == 1:
				yield (self.x - y_offset + self.shape["y_adj"], 
					   self.y + x_offset)
			elif self.rotation == 2:
				yield (self.x - x_offset + self.shape["x_adj"],
					   self.y - y_offset + self.shape["y_adj"])
			elif self.rotation == 3:
				yield (self.x + y_offset,
					   self.y - x_offset + self.shape["x_adj"] )

	def render(self, v):
		for x, y in self:
			v.render_tile(x, y, self.color)

	def rotate(self, clockwise=True):
		if clockwise:
			self.rotation = (self.rotation + 1) % 4
		else:
			self.rotation = (self.rotation - 1) % 4

	def rotated(self, clockwise=True):
		p = Piece(self.x, self.y, self.shape, self.color, self.rotation)
		p.rotate(clockwise)
		return p


class Board:
	def __init__(self, n_columns, n_rows, board = None, autogen = True):
		self.height = n_rows
		self.columns = [self.height] * n_columns
		self.reset()
		self.rand = Random()
		self.color_index = 0
		self.autogen = autogen

	def reset(self):
		self.piece = None
		self.tiles = defaultdict(lambda:Color.CLEAR)

	def clear_tile(self, x, y):
		self.tiles[(x,y)] = Color.CLEAR

		# Move all the tiles above this row down one space
		for y_tile in range(y, self.columns[x] - 1, -1):
			self.tiles[(x, y_tile)] = self.tiles[(x, y_tile - 1)]

		# And reset the top of of the columns
		while (self.columns[x] < self.height and 
		       self.tiles[(x, self.columns[x])] == Color.CLEAR):
			self.columns[x] += 1

	def clear_row(self, row):
		for col in range(len(self.columns)):
			self.clear_tile(col, row)

	def row_full(self, row):
		for col in range(len(self.columns)):
			if self.tiles[(col,row)] == Color.CLEAR:
				return False
		return True

	def set_tile_color(self, x, y, color):
		assert color != Color.CLEAR
		self.tiles[(x,y)] = color
		if self.columns[x] > y:
			self.columns[x] = y

	def piece_can_move(self, x_move, y_move):
		"""Returns True if a piece can drop, False otherwise."""
		for base_x, base_y in self.piece:
			x = x_move + base_x
			y = y_move + base_y
			if not 0 <= x < len(self.columns) or y >= self.columns[x]:
				return False
		return True

	def drop_piece(self):
		"""Either drops a piece down one level, or finalizes it and creates another piece."""
		if self.piece is None:
			return
		if not self.piece_can_move(0, 1):
			self.finalize_piece()
			if self.autogen:
				self.generate_piece()
		else:
			self.piece.move(0, 1)

	def full_drop_piece(self):
		"""Either drops a piece down one level, or finalizes it and creates another piece."""
		if self.piece is None:
			return
		while self.piece_can_move(0, 1):
			self.piece.move(0, 1)
		self.finalize_piece()
		self.generate_piece()

	def move_piece(self, x_move, y_move):
		"""Move a piece some number of spaces in any direction"""
		if self.piece is None:
			return
		if self.piece_can_move(x_move, y_move):
			self.piece.move(x_move, y_move)

	def rotate_piece(self, clockwise=True):
		if self.piece is None:
			return
		if self.piece_can_rotate(clockwise):
			self.piece.rotate(clockwise)

	def piece_can_rotate(self, clockwise):
		"""Returns True if a piece can drop, False otherwise."""
		p = self.piece.rotated(clockwise)
		for x, y in p:
			if not 0 <= x < len(self.columns) or y >= self.columns[x]:
				return False
		return True

	def generate_piece(self):
		"""Creates a new piece at random and places it at the top of the board."""
		middle = len(self.columns) // 2
		shape = self.rand.choice(Piece.SHAPES)
		self.piece = Piece(middle - shape["x_adj"], 0, shape, shape["color"])
		self.color_index = (self.color_index + 1) % len(Color.colors())

	def finalize_piece(self):
		for x, y in self.piece:
			self.set_tile_color(x, y, self.piece.color)

		for y in range(0, self.height + 1):
			if self.row_full(y):
				self.clear_row(y)

		self.piece = None

	def render(self, v):
		v.clear()
		v.set_size(len(self.columns), self.height)
		for (x,y), color in self.tiles.items():
			v.render_tile(x, y, color)
		if self.piece is not None:
			self.piece.render(v)
