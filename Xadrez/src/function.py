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

# Verifica se o movimento coloca o rei em xeque
def possible_moves(coords_list, selected, board, wcastle, bcastle):
    res = list(filter(lambda x: not threat_move(selected, x, board)))
    piece = board[selected[1][selected[0]]]

    # Se o rei se mover, não pode mais fazer roque (castling) com a torre correspondente (se houver)

    if piece == wking and board[7][6] == 0 and board[7][5] == 0 and wcastle[1] and not threat_move(find_king('white', board), (5, 7), board): 
        res.append((7, 7))
    if piece == wking and board[7][1] == 0 and board[7][2] == 0 and board[7][3] == 0 and wcastle[0] and not threat_move(find_king('white', board), (3, 7), board):
        res.append((0, 7))
    if piece == bking and board[0][6] == 0 and board[0][5] == 0 and bcastle[1] and not threat_move(find_king('black', board), (5, 0), board):
        res.append((7, 0))
    if piece == bking and board[0][1] == 0 and board[0][2] == 0 and board[0][3] == 0 and bcastle[0] and not threat_move(find_king('black', board), (3, 0), board):
        res.append((0, 0))

    # Se o rei estiver em xeque, só pode se mover para fora do xeque
    checked = check(board)

    if (checkmated == 'white' or threat_move(find_king('white', board), (6, 7), board)) and piece == wking and True in wcastle and (7, 7) in res:
        res.remove((7, 7))
    if (checkmated == 'white' or threat_move(find_king('white', board), (2, 7), board)) and piece == wking and True in wcastle and (0, 7) in res:
        res.remove((0, 7))
    if (checkmated == 'black' or threat_move(find_king('black', board), (6, 0), board)) and piece == bking and True in bcastle and (7, 0) in res:
        res.remove((7, 0))
    if (checkmated == 'black' or threat_move(find_king('black', board), (2, 0), board)) and piece == bking and True in bcastle and (0, 0) in res:
        res.remove((0, 0))
    return res

###########################    RENDERIZAÇÃO DE IMAGEM    ###########################

# Desenha o tabuleiro
def draw_board(win, board, rotated):
    # Se o tabuleiro estiver rotacionado, inverte as linhas e colunas do tabuleiro
    if rotated: 
        board = [x[::-1] for x in board[::-1]]
    # Desenha as casas do tabuleiro
    for i in range (8):
        for j in range (8):
            if board[i][j] != 0:
                win.blit(board[i][j], (64 + 64 * j, 64 + 64 * i))

# Desenha movimentos possíveis e capturas
def draw_moves(win, coords_list, selected, board, rotated):

    if rotated:
        coords_list - [(7 - x, 7 - y) for (x, y) in coords_list]
    
    for coords in coords_list:
        if rotated:
            c = board[7 - coords[1]][7 - coords[0]]
        else:
            c = board[coords[1]][coords[0]]
        if c != 0:
            win.blit(target, (64 + 64 * coords[0], 64 + 64 * coords[1]))
        else:
            pygame.draw.circle(win, (20, 23, 25), (coords[0] * 64 + 96, coords[1] * 64 + 96), 7)

# Sorteio do peão promovido
def draw_pawn_promotion(win, coords):

    if board[coords[1]][coords[0]] == wpawn:
        for i in enumerate([wqueen, wrook, wbishop, wknight]):
            if rotated:
                win.blit(i[1], (576, 320 + 64 * i[0]))
            else:
                win.blit(i[1], (0, 64 + 64 * i[0]))

    if board[coords[1]][coords[0]] == bpawn:
        for i in enumerate([bqueen, brook, bbishop, bknight]):
            if rotated:
                win.blit(i[1], (0, 64 + 64 * i[0]))
            else:
                win.blit(i[1], (576, 320 + 64 * i[0]))

def draw_buttons(win):
    win.blit(cross, (80, 592))
    win.blit(rotate, (144, 592))
    win.blit(arrow_backwards, (208, 592))
    win.blit(arrow_forwards, (272, 592))
    win.blit(return_menu, (16, 16))

###########################    BOARD EVALUATION   ###########################

# Verifica se o rei está em xeque 
def check(board):
    (white, black) = (False, False)
    for (x, y) in [(x, y) for x in range(8) for y in range(8) if board[y][x] != 0]:
        possible_moves = res = list(filter(lambda z: not threat_move((x,y), z, board), moves((x,y),board)))
        if is_white(board[y][x]) and find_king('black', board) in possible_moves:
            black = True
        if is_black(board[y][x]) and find_king('white', board) in possible_moves:
            white = True
    return 'white' * white + 'black' * black

# Verifica se o rei está em xeque-mate ou se o jogo acabou por falta de peças
def checkmate(board, wcastle, bcastle):
    (white, black) = (True, True)
    for (x, y) in [(x, y) for x in range(8) for y in range(8) if board[y][x] != 0]:
        if possible_moves(moves((x,y), board), (x,y), board, wcastle, bcastle) != []:
            if is_white(board[y][x]): white = False
            if is_black(board[y][x]): black = False
    return 'white' * white + 'black' * black