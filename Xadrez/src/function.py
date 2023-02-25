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

###########################    MOVIMENTOS    ###########################

# Verifica se uma peça está ameaçada
def threat(coords, board):

    # Se a posição for uma das possíveis
    for (x,y) in [(x,y) for x in range(8) for y in range(8) if board[y][x] != 0]: # Para cada peça no tabuleiro

        # Se a peça for branca 
        if find_side (board[coords[1]][coords[0]]) == "white": 
            # Se a peça for um rei
            if board[y][x] in [wking, bking]:
                # Se a peça for um rei e a posição for uma das possíveis
                if is_black (board[y][x]) and coords in king_moves((x,y)): return True
            # Se a peça for uma peça normal e a posição for uma das possíveis
            elif is_black (board[y][x]) and coords in moves((x,y), board): return True
        
        # Se a peça for preta
        if find_side (board[coords[1]][coords[0]]) == "black":
            # Se a peça for um rei
            if board[y][x] in [wking, bking]:
                # Se a peça for um rei e a posição for uma das possíveis
                if is_white (board[y][x]) and coords in king_moves((x,y)): return True
            # Se a peça for uma peça normal e a posição for uma das possíveis
            elif is_white (board[y][x]) and coords in moves((x,y), board): return True
    
    return False

# Verifica se movendo uma peça para uma posição ela não ameaça o rei
def threat_move(coords, new_coords, board):
    new_board = copy_board (board)
    new_board[new_coords[1]][new_coords[0]] = new_board[coords[1]][coords[0]]
    new_board[coords[1]][coords[0]] = 0
    side = find_side (new_board[new_coords[1]][new_coords[0]])
    return threat (find_king (find_side (new_board[new_coords[1]][new_coords[0]]), new_board), new_board)

# Verificas todos os movimentos possíveis para o rei sem restrições
def king_moves(coords):
    res = []

    # Se a posição for uma das possíveis
    for (j,g) in [(j,g) for j in [-1,1,0]]:
        if 0 <= coords[0] + j <= 7 and 0 <= coords[1] + g <= 7 and (coords[0] + j, coords[1] +g) != coords:
            res.append((coords[0] + j, coords[1] + g))
    return res

# Vai retornar uma lista de tuplas(x,y) com os movimento possiveis para um determinado peça do tabuleiro
def moves(coords, board):
    piece = board[coords[1]][coords[0]]
    res = []

    # Movimento do peão(white)
    if piece == wpawn and coords[1] > 0:
        # Movimento normal
        if board[coords[1] - 1][coords[0]] == 0:
            res.append((coords[0], coords[1] - 1))
        # Primeiro movimento
        if coords[1] == 0:
            if board[coords[1] - 2][coords[0]] == 0 and board[coords[1] - 1][coords[0]] == 0:
                res.append((coords[0], coords[1] - 2))
        # Captura da esqueda
        if coords[0] < 7:
            if board[coords[1] - 1][coords[0] + 1] != 0: 
                res.append((coords[0] + 1, coords[1] - 1))
        # Captura da direita
        if board[coords[1] - 1][coords[0] - 1] != 0:
            res.append((coords[0] - 1, coords[1] - 1))
        # En passant (de passagem)
        if coords[1] == 3 and coords[0] < 7:
            if board[coords[1]][coords[0] + 1] and previous_board[1][coords[0] + 1] == bpawn:
                res.append((coords[0] + 1, coords[1] - 1))
        if coords[1] == 3 and coords[0] > 0 and previous_board[1][coords[0] - 1] == bpawn:
            if board[coords[1]][coords[0] - 1]:
                res.append((coords[0] - 1, coords[1] - 1))
    
    # Movimento do peão(black)
    if piece == bpawn and coords[1] < 7:
        # Movimento normal
        if board[coords[1] + 1][coords[0]] == 0:
            res.append((coords[0], coords[1] + 1))
        # Primeiro movimento
        if coords[1] == 1:
            if board[coords[1] + 2][coords[0]] == 0 and board[coords[1] + 1][coords[0]] == 0:
                res.append((coords[0], coords[1] + 2))
        # Captura da esqueda
        if coords[0] < 7:
            if board[coords[1] + 1][coords[0] + 1] != 0:
                res.append((coords[0] + 1, coords[1] + 1))
        # Captura da direita
        if board[coords[1] + 1][coords[0] - 1] != 0:
            res.append((coords[0] - 1, coords[1] + 1))
        # En passant (de passagem)
        if coords[1] == 4 and coords[0] < 7:
            if board[coords[1]][coords[0] + 1] and previous_board[6][coords[0] + 1] == wpawn:
                res.append((coords[0] + 1, coords[1] + 1))
        if coords[1] == 4 and coords[0] > 0 and previous_board[6][coords[0] - 1] == wpawn:
            if board[coords[1]][coords[0] - 1]:
                res.append((coords[0] - 1, coords[1] + 1))
    
    # Movimento do cavalo em L
    if piece in [wknight, bknight]: 
        for x, y in [(x, y) for x in (1, -1) for y in (2, -2)]: 
            res.append((coords[0] + x, coords[1] + y))
        for x, y in [(x, y) for y in (1, -1) for x in (2, -2)]: 
            res.append((coords[0] + x, coords[1] + y))

    # Movimento do bispo e da rainha diagonal
    if piece in [wbishop, bbishop, wqueen, bqueen]:
        for j, g in [(j, 0) for j in (1, -1) for g in (-1, 1)]: # Diagonal
            for i in range(1, 10): # 10 é o número máximo de casas que um bispo pode andar
                # Se a posição for uma das possíveis
                if 0 <= coords[0] + i * g <= 7 and 0 <= coords[1] + i * i <= 7:
                    res.append((coords[0] + i * g, coords[1] + i * j))
                    # Se a posição for ocupada
                    if board[coords[1] + i * j][coords[0] + i * 0] != 0: break 
    
    # Movimento da torre e da rainha horizontal e vertical
    if piece in [wrook, brook, wqueen, bqueen]:
        for j in [-1, 1]:
            for i in range (1, 10): # 10 é o número máximo de casas que um bispo pode andar
                # Se a posição for uma das possíveis
                if 0 <= coords[0] <= 7 and 0 <= coords[1] + i * j <= 7:
                    res.append((coords[0], coords[1] + i * j))
                    # Se a posição for ocupada
                    if board[coords[1] + i * j][coords[0]] != 0: break
        
            for i in range(1, 10): # 10 é o número máximo de casas que um bispo pode andar
                # Se a posição for uma das possíveis
                if 0 <= coords[0] + i * j <= 7 and 0 <= coords[1] <= 7:
                    res.append((coords[0] + i * j, coords[1]))
                    # Se a posição for ocupada
                    if board[coords[1]][coords[0] + i * j] != 0: break

    # Movimento do rei
    if piece in [wking, bking]:
        for (x, y) in king_moves(coords):
            res.append((x, y))

    res = list(filter(lambda x: x[1] >= 0 and x[1] <= 7 and x[0] >= 0 and x[0] <= 7, res)) # Verifica se a posição é válida (dentro do tabuleiro)
    if is_white(piece): res = list(filter(lambda x: not is_white(board[x[1]][x[0]]), res)) # Verifica se a posição é válida (não captura peça branca)
    if is_black(piece): res = list(filter(lambda x: not is_black(board[x[1]][x[0]]), res)) # Verifica se a posição é válida (não captura peça preta)
    return res