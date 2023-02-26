from config import *
from functions import *
from random import choice

"""
A forma como o bot funciona é avaliando o tabuleiro para cada movimento e
gerando um valor numérico. O valor é maior se a posição concede vantagem 
ao lado que joga. Cada peça tem um valor relativo dependendo da posição e do
qual peça é. Os valores são de acordo com as posições que foram tomados de 
Simplified Evaluation Function e ligeiramente alterada.
"""

pawn = [[0, 0, 0, 0, 0, 0, 0, 0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 15, 15, 20, 10, 10],
        [5, 5, 10, 20, 20, 10, 5, 5],
        [0, 0, 0, 25, 30, 0, 0, 0],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]]

knight = [[-50, -40, -30, -30, -30, -30, -40, -50],
          [-40, -20, 0, 0, 0, 0, -20, -40],
          [-30, 0, 10, 15, 15, 10, 0, -30],
          [-30, 5, 15, 20, 20, 15, 5, -30],
          [-30, 0, 15, 20, 20, 15, 0, -30],
          [-30, 5, 10, 15, 15, 10, 5, -30],
          [-40, -20, 0, 5, 5, 0, -20, -40],
          [-50, -40, -30, -30, -30, -30, -40, -50]]

bishop = [[-20, -10, -10, -10, -10, -10, -10, -20],
          [-10, 0, 0, 0, 0, 0, 0, -10],
          [-10, 0, 5, 10, 10, 5, 0, -10],
          [-10, 5, 5, 10, 10, 5, 5, -10],
          [-10, 0, 10, 10, 10, 10, 0, -10],
          [-10, 10, 10, 10, 10, 10, 10, -10],
          [-10, 5, 0, 0, 0, 0, 5, -10],
          [-20, -10, -10, -10, -10, -10, -10, -20]]

rook = [[0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [-5, 0, 0, 0, 0, 0, 0, -5], 
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [0, 0, 0, 5, 5, 0, 0, 0]]

queen = [[-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]]

king = [[-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [20, 20, 0, 0, 0, 0, 20, 20],
        [20, 30, 10, 0, 0, 10, 30, 20]]

# Valores das peças
piece_values = {**dict.fromkeys([wpawn, bpawn], 10), 
                **dict.fromkeys([wknight, bknight], 30)
                **dict.fromkeys([wbishop, bbishop], 30),
                **dict.fromkeys([wrook, brook], 50),
                **dict.fromkeys([wqueen, bqueen], 90),
                **dict.fromkeys([wking, bking], 99999)}

# Valores das peças de acordo com a posição
piece_pos_values = {**dict.fromkeys([wpawn, bpawn], pawn),
                    **dict.fromkeys([wknight, bknight], knight),
                    **dict.fromkeys([wbishop, bbishop], bishop),
                    **dict.fromkeys([wrook, brook], rook),
                    **dict.fromkeys([wqueen, bqueen], queen),
                    **dict.fromkeys([wking, bking], king)}

class bot(object):

    # Retorna uma lista de coordenadas com todas as peças móveis
    def get_piece (self, board, white_moving, wcastle, bcastle):
        res = []
        for (x, y) in [(x, y) for x in range(8) for y in range(8) if board[x][y] != 0]:
            if white_moving and is_white(board[y][x]):
                res.append((x, y))
            if not white_moving and is_black(board[y][x]):
                res.append((x, y))
        return list(filter(lambda x: possible_moves(moves(x, board), x, board, wcastle, bcastle) != [], res))