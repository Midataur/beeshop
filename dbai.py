import chess
import requests
import random
from functools import lru_cache

master_url = 'https://explorer.lichess.ovh/master'
endgame_url = 'http://tablebase.lichess.ovh/standard'

piece_values = {
    1: 1, #pawn
    2: 3, #knight
    3: 3, #bishop
    4: 5, #rook
    5: 9, #queen
    6: 999999 #king
}

@lru_cache()
def master_lookup(fen):
    board = chess.Board(fen)
    turn = 'white' if board.turn else 'black'
    r = requests.get(master_url+f'?fen={fen}')
    moves = r.json()['moves']
    moves.sort(key=lambda x: -x[turn])
    if moves:
        return chess.Move.from_uci(moves[0]['uci'])

@lru_cache()
def endgame_lookup(fen):
    r = requests.get(endgame_url+f'?fen={fen}')
    moves = r.json()['moves']
    if moves:
        return chess.Move.from_uci(moves[0]['uci'])

def find_move(board, outformat='san'):
    #try looking up state
    move = master_lookup(board.fen())
    if not move:
        #print("TOTO, WE'RE NOT IN KANSAS ANYMORE")
        #state not found in database, return a random move
        move = tree_search(board.fen(), depth=3)[0]
    return board.san(move) if outformat == 'san' else board.uci(move)

def evaluate_board(board):
    score = 0
    for piece in board.piece_map().values():
        value = piece_values[piece.piece_type]
        value *= 1 if piece.color else -1 #add for white, sub for black
        score += value
    return score

@lru_cache()
def tree_search(fen, depth=0):
    #we use fen so we can cache results and to avoid side effects
    board = chess.Board(fen)
    #if at leaf node
    if board.is_game_over() or board.can_claim_draw():
        if board.result() == '1-0': #white winsS
            board_score = 999999
        elif board.result == '0-1': #black winsS
            board_score = -999999 
        else:
            board_score = 0
        return (None, board_score)
    elif depth == 0:
        return (None,evaluate_board(board))
    
    #go down one more layer
    scores = []
    for move in board.legal_moves:
        board.push(move)
        result = tree_search(board.fen(), depth=depth-1)[1]
        scores.append((move,result))
        board.pop()
    
    #actually min max
    minormax = max if board.turn else min
    return minormax(scores, key=lambda x: x[1])

if __name__ == '__main__':
    board = chess.Board()
    while True:
        print(board)
        print('Score:',evaluate_board(board))
        print('Legal moves:',[board.san(x) for x in board.legal_moves])
        board.push_san(input('What is your move? '))

        if board.is_game_over():
            print(board.result())
            break

        #ai move
        move = find_move(board)
        board.push_san(move)
        print('Bot move:', move)

        if board.is_game_over():
            print(board.result())
            break

        print()