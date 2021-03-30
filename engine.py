from dbai import find_move
import requests
import chess
#lichess compatible uci interface

board = chess.Board()

#main command loop
while True:
    command = input()
    if command == 'isready':
        print('readyok')
    elif command == 'uci':
        print('id name MidaBot')
        print('id author Max Petschack')
        print("""option name Debug Log File type string default 
option name Contempt type spin default 24 min -100 max 100
option name Analysis Contempt type combo default Both var Off var White var Black var Both
option name Threads type spin default 1 min 1 max 512
option name Hash type spin default 16 min 1 max 131072
option name Clear Hash type button
option name Ponder type check default false
option name MultiPV type spin default 1 min 1 max 500
option name Skill Level type spin default 20 min 0 max 20
option name Move Overhead type spin default 30 min 0 max 5000
option name Minimum Thinking Time type spin default 20 min 0 max 5000
option name Slow Mover type spin default 84 min 10 max 1000
option name nodestime type spin default 0 min 0 max 10000
option name UCI_Chess960 type check default false
option name UCI_AnalyseMode type check default false
option name UCI_LimitStrength type check default false
option name UCI_Elo type spin default 1350 min 1350 max 2850
option name SyzygyPath type string default <empty>
option name SyzygyProbeDepth type spin default 1 min 1 max 100
option name Syzygy50MoveRule type check default true
option name SyzygyProbeLimit type spin default 7 min 0 max 7""")
        print('uciok')
    elif 'position' in command:
        #set the board position
        moves = command.split()[3:]
        board.reset()
        for move in moves:
            board.push_uci(move)
    elif command[:2] == 'go':
        print('bestmove',find_move(board,outformat='uci'))
    elif command =='quit':
        break