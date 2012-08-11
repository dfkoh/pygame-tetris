import nose
from engine import *

class TestTextView:
	def setUp(self):
		self.tr = TextView()
		self.tr.set_size(5,5)

	def test_smoke(self):
		self.tr.show()
		assert self.tr.get_str() == EMPTY_BOARD

	def test_set_size(self):
		self.tr.set_size(10,3)
		self.tr.show()
		assert self.tr.get_str() == EMPTY_10x3_BOARD

	def test_colors(self):
		for i in range(4):
			self.tr.render_tile(i + 1, 0, Color.colors()[i])
		self.tr.show()
		assert self.tr.get_str() == COLOR_BOARD

class TestPiece:
	def setUp(self):
		self.tr = TextView()
		self.tr.set_size(4, 4)

	def test_pieces(self):
		for letter in ("L", "R", "O", "T", "S", "Z", "I"):
			self.tr.clear()
			p = Piece(0, 0, getattr(Piece, "{}_SHAPE".format(letter)), Color.RED)
			expected = globals()["{}_PIECE".format(letter)]
			p.render(self.tr)
			print("{}_SHAPE".format(letter))
			self.tr.show()
			assert self.tr.get_str() == expected

	def test_rot_pieces(self):
		for letter in ("L", "R", "O", "T", "S", "Z", "I"):
			p = Piece(0, 0, getattr(Piece, "{}_SHAPE".format(letter)), Color.RED)
			for i in range(5):
				self.tr.clear()
				expected = globals()["{}_ROT{}".format(letter, i % 4)]
				p.render(self.tr)
				print("{}_ROT{}".format(letter, i % 4))
				self.tr.show()
				assert self.tr.get_str() == expected
				p.rotate()

class TestBoard:
	def setUp(self):
		self.tr = TextView()
		self.b = Board(4,5, autogen=False)
		self.b.piece = Piece(0, 0, Piece.Z_SHAPE, Color.RED)

	def test_smoke(self):
		self.b.render(self.tr)
		self.tr.show()
		assert self.tr.get_str() == DROP_PIECE[0]

	def test_drop_piece(self):
		for i in range(4):
			self.b.render(self.tr)
			print("i: {}".format(i))
			self.tr.show()
			assert self.tr.get_str() == DROP_PIECE[i]
			assert self.b.piece != None
			self.b.drop_piece()
		self.b.render(self.tr)
		self.tr.show()
		assert self.tr.get_str() == DROP_PIECE[4]
		assert self.b.piece == None

	def test_drop_piece_stuff(self):
		self.b.set_tile_color(0, 3, Color.BLUE)
		self.b.set_tile_color(0, 4, Color.BLUE)
		for i in range(3):
			self.b.render(self.tr)
			print("i: {}".format(i))
			self.tr.show()
			assert self.tr.get_str() == DROP_PIECE_STUFF[i]
			assert self.b.piece != None
			self.b.drop_piece()
		self.b.render(self.tr)
		self.tr.show()
		assert self.tr.get_str() == DROP_PIECE_STUFF[3]
		assert self.b.piece == None

	def test_move_piece(self):
		MOVES = [(1,0), (1,0), (-1,0), (-1,0)]
		for i in range(len(MOVES)):
			self.b.render(self.tr)
			self.tr.show()
			assert self.tr.get_str() == SHUFFLE_PIECE[i]
			self.b.move_piece(*MOVES[i])
		self.b.render(self.tr)
		self.tr.show()
		assert self.tr.get_str() == SHUFFLE_PIECE[4]

	def test_clear_rows(self):
		self.b = Board(4,6)
		self.b.piece = Piece(0, 0, Piece.Z_SHAPE, Color.RED)

		self.b.set_tile_color(0, 5, Color.RED)
		self.b.set_tile_color(0, 4, Color.RED)
		self.b.set_tile_color(0, 3, Color.RED)
		self.b.set_tile_color(1, 5, Color.BLUE)
		self.b.set_tile_color(1, 4, Color.BLUE)
		self.b.set_tile_color(1, 3, Color.BLUE)
		self.b.set_tile_color(2, 5, Color.GREEN)
		self.b.set_tile_color(2, 4, Color.GREEN)
		self.b.set_tile_color(2, 3, Color.GREEN)
		self.b.set_tile_color(2, 2, Color.GREEN)
		self.b.set_tile_color(3, 3, Color.YELLOW)
		self.b.set_tile_color(3, 5, Color.YELLOW)

		self.b.render(self.tr)
		self.tr.show()
		assert self.tr.get_str() == CLEAR_ROW[0]
		print(self.b.columns)
		assert self.b.columns == [3,3,2,3]

		assert self.b.row_full(5)
		assert not self.b.row_full(4)
		assert self.b.row_full(3)
		self.b.clear_row(3)
		self.b.render(self.tr)
		self.tr.show()
		assert self.tr.get_str() == CLEAR_ROW[1]
		print(self.b.columns)
		assert self.b.columns == [4,4,3,5]

#########################
# Positions for Testing #
#########################

EMPTY_BOARD = """
.....
.....
.....
.....
.....
"""

EMPTY_10x3_BOARD = """
..........
..........
..........
"""

COLOR_BOARD = """
.*#oO
.....
.....
.....
.....
"""

L_PIECE = """
*...
*...
**..
....
"""
R_PIECE = """
**..
*...
*...
....
"""
O_PIECE = """
**..
**..
....
....
"""
T_PIECE = """
***.
.*..
....
....
"""
S_PIECE = """
*...
**..
.*..
....
"""
Z_PIECE = """
**..
.**.
....
....
"""
I_PIECE = """
****
....
....
....
"""

L_ROT0 = """
*...
*...
**..
....
"""
L_ROT1 = """
***.
*...
....
....
"""
L_ROT2 = """
**..
.*..
.*..
....
"""
L_ROT3 = """
..*.
***.
....
....
"""

R_ROT0 = """
**..
*...
*...
....
"""
R_ROT1 = """
***.
..*.
....
....
"""
R_ROT2 = """
.*..
.*..
**..
....
"""
R_ROT3 = """
*...
***.
....
....
"""

O_ROT0 = O_ROT1 = O_ROT2 = O_ROT3 = O_PIECE

T_ROT0 = """
***.
.*..
....
....
"""
T_ROT1 = """
.*..
**..
.*..
....
"""
T_ROT2 = """
.*..
***.
....
....
"""
T_ROT3 = """
*...
**..
*...
....
"""

S_ROT0 = S_ROT2 = """
*...
**..
.*..
....
"""
S_ROT1 = S_ROT3 = """
.**.
**..
....
....
"""

Z_ROT0 = Z_ROT2 = """
**..
.**.
....
....
"""
Z_ROT1 = Z_ROT3 = """
.*..
**..
*...
....
"""

I_ROT0 = I_ROT2 = """
****
....
....
....
"""
I_ROT1 = I_ROT3 = """
*...
*...
*...
*...
"""

DROP_PIECE = (
"""
**..
.**.
....
....
....
""",
"""
....
**..
.**.
....
....
""",
"""
....
....
**..
.**.
....
""",
"""
....
....
....
**..
.**.
""",
"""
....
....
....
**..
.**.
"""
)

DROP_PIECE_STUFF = (
"""
**..
.**.
....
#...
#...
""",
"""
....
**..
.**.
#...
#...
""",
"""
....
....
**..
#**.
#...
""",
"""
....
....
**..
#**.
#...
""")

SHUFFLE_PIECE = (
"""
**..
.**.
....
....
....
""",
"""
.**.
..**
....
....
....
""",
"""
.**.
..**
....
....
....
""",
"""
**..
.**.
....
....
....
""",
"""
**..
.**.
....
....
....
""")

CLEAR_ROW = (
"""
**..
.**.
..o.
*#oO
*#o.
*#oO
""",
"""
**..
.**.
....
..o.
*#o.
*#oO
"""
)

if __name__ == "__main__":
	nose.run()