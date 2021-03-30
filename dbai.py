import chess
import requests
import random

url = 'https://explorer.lichess.ovh/master'

def find_move(board, outformat='san'):
    state = board.fen()
    turn = 'white' if board.turn else 'black'
    r = requests.get(url+f'?fen={state}')
    moves = r.json()['moves']
    moves.sort(key=lambda x: -x[turn])
    if moves:
        return moves[0][outformat]
    #state not found in database, return a random move
    move = random.choice(list(board.legal_moves))
    return board.san(move) if outformat == 'san' else board.uci(move)

if __name__ == '__main__':
    board = chess.Board()
    while True:
        print(board)
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