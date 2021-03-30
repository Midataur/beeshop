from PIL import Image, ImageFilter, ImageDraw
from vision import image_to_binmap
from os import listdir, remove
from copy import copy
from time import sleep
import numpy as np
import imghdr
import chess
import chess.engine

def wait_for_new_photo(path_to_folder):
    baseline = set(listdir(path_to_folder))
    print('Waiting')
    while True:
        #waiting for new file
        current = set(listdir(path_to_folder))
        if current != baseline:
            if len(current) < len(baseline): #ie a file was deleted
                baseline = current
            else: #ie a new file was made
                new_file = path_to_folder+(current-baseline).pop()
                break

    print('Found!')
    return wait_for_write(new_file)

def wait_for_write(new_file):
    #we can actually detect the image before it has finished writing
    #to fix this we try loading it and see if it works
    #we keep doing this until we can, at which point we're good
    while imghdr.what(new_file) == None:
        pass
    sleep(1)
    img = Image.open(new_file)
    while True:
        try:
            img.load()
            remove(new_file)
        except OSError:
            pass
        else:
            break
    return img

def board_to_binmap(board):
    binmap = np.zeros(64)
    for x in board.mirror().piece_map().keys():
        binmap[x] = 1
    return binmap.reshape((8,8)).astype(int)

def find_move(board, img_binmap):
    #check all moves for their binmap
    for move in board.legal_moves:
        bclone = copy(board)
        bclone.push(move)
        new_binmap = board_to_binmap(bclone)
        if (new_binmap == img_binmap).all():
            return move
    return None

path_to_folder = '/run/user/1000/gvfs/mtp:host=SAMSUNG_SAMSUNG_Android_R58M95KY9TB/Card/DCIM/Camera/'
board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci('/usr/games/stockfish')

while True:
    #player move
    img = wait_for_new_photo(path_to_folder)
    img_binmap = image_to_binmap(img)
    move = find_move(board,img_binmap)
    if move:
        print('\nFound move:', board.san(move))
        board.push(move)
    else:
        print('\nNo valid move detected, please take another photo')
        continue

    print('Current board:')
    print(board)

    #check for game over
    if board.is_game_over():
        print(board.result())
        break

    #ai turn
    print('\nAi turn:')
    ai_move = engine.play(board, chess.engine.Limit(time=0.1)).move
    print('Ai move:', board.san(ai_move))
    board.push(ai_move)
    print('Current board:')
    print(board)

    #check for game over
    if board.is_game_over():
        print(board.result())
        break
    print('\nReady for photo')