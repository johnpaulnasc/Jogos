import pygame

from config import *

#Para depuração do código
def print_board (board): 
    s = ["wpawn", "wknight", "wbishop", "wrook", "wqueen", "wking", "bpawn", "bknight", "bbishop", "brook", "bqueen", "bking", 0]
    p = [wpawn, wknight, wbishop, wrook, wqueen, wking, bpawn, bknight, bbishop, brook, bqueen, bking, 0]
    for line in board:
        print (list(map(lambda x: s[p.index(x)], line)))

#Copia o tabuleiro para uma nova variável
def copy_board (board): 
    new = [[0] * 8 for _ in range(8)]
    for (x,y) in [(x,y) for x in range(8) for y in range(8)]:
        new[y][x] = board[y][x]
    return new

# Verifica se o mouse está em um quadrado do tabuleiro
def inside_board (mouse):
    coords = (mouse[0]//64 - 1, mouse[1]//64 - 1)
    return (-1 not in coords and 8 not in coords)

# Retorna o quadrado do tabuleiro que o mouse clicou
def hitbox (mouse, rotated):
    if rotated: return (mouse[0]//64 - 1, mouse[1]//64 - 1)
    return (mouse[0]//64 - 1, mouse[1]//64 - 1)

# Verifica se a peça é branca
def is_white(piece):
    return piece in [wrook, wknight, wbishop, wqueen, wking, wpawn]

# Verifica se a peça é preta
def is_black(piece):
    return piece in [brook, bknight, bbishop, bqueen, bking, bpawn]

# Retorna a cor da peça
def find_side(piece): 
    return "white" * is_white(piece) + "black" * is_black(piece)

# Verifica de quem é a vez
def find_turn(white_moving):
    return white_moving * 'white' + 'black' * (not white_moving) 

# Retorna a posição do rei
def find_king(side, board): 
    for (x,y) in [(x,y) for x in range(8) for y in range(8)]:
        if side == "white" and board[y][x] == wking: return (x,y)
        if side == "black" and board[y][x] == bking: return (x,y)
    return(1,1)