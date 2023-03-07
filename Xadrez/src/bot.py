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
pieces_value = {**dict.fromkeys([wpawn, bpawn], 10), 
                **dict.fromkeys([wknight, bknight], 30)
                **dict.fromkeys([wbishop, bbishop], 30),
                **dict.fromkeys([wrook, brook], 50),
                **dict.fromkeys([wqueen, bqueen], 90),
                **dict.fromkeys([wking, bking], 99999)}

# Valores das peças de acordo com a posição
pieces_pos_value = {**dict.fromkeys([wpawn, bpawn], pawn),
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
    
    # Pesquisa o valor da peça de acordo com a posição no tabuleiro
    def get_pos_value(self, piece, pos):
        if is_white(piece):
            return pieces_pos_value[piece][pos[1]][pos[0]]

        return [x[::-1] for x in pieces_pos_value[piece]][::-1][pos[1]][pos[0]]
    
    # Soma o valor total no quadrado
    def get_board_value(self, board, white_moving):
        value = 0
        for (x, y) in [(x, y) for x in range(8) for y in range(8) if board[y][x] != 0]:
            if white_moving:
                if is_white(board[y][x]): 
                    value += self.get_pos_value(board[y][x], (x,y))
                else: 
                    value -= self.get_pos_value(board[y][x], (x,y))
            else:
                if is_white(board[y][x]): 
                    value -= self.get_pos_value(board[y][x], (x,y))
                else: 
                    value += self.get_pos_value(board[y][x], (x,y))
        
        return value
    
    # Prcura a melhor jogada para o bot
    def get_best_move(self, board, pieces, white_moving, wcastle, bcastle):
        max_value = -99999

        for piece in pieces:
            for x,y in possible_moves(moves(piece, board), piece, board, wcastle, bcastle):
                current_value = 0
                hold = board[y][x]
                board[y][x] = board[piece[1]][piece[0]]
                board[piece[1]][piece[0]] = 0
                if hold != 0: current_value += pieces_value[hold] # Captura
                current_value += self.get_board_value(board, white_moving)
                if current_value == max_value: # Não joga da mesma forma duas vezes
                    switch = choice([False, True])
                    if switch:
                        best_piece = piece
                        best_move = (x,y)
                if current_value > max_value:
                    max_value = current_value
                    best_piece = piece
                    best_move = (x,y)
                board[piece[1]][piece[0]] = board[y][x]
                board[y][x] = hold
        return (best_piece, best_move)
    
    # Retorna o movimento como (best_piece, best_move)
    def play(self, board, white_moving, wcastle, bcastle):
        pieces = self.get_pieces(board, white_moving, wcastle, bcastle)
        if pieces == []: 
            return False
        prev_board = copy_board(board)
        res = self.get_best_move(prev_board, pieces, white_moving, wcastle, bcastle)

        return (res[0], res[1])