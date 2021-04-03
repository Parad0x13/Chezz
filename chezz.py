# Inspired by https://www.youtube.com/watch?v=DpXy041BIlA, 30 wierd chess algorithms

BOARD_TYPE_LINEAR = 0

WHITE = "PRNBQK"
BLACK = "prnbqk"

RATING_IDIOT = 0

# I'd like to account for several ways to account for board position just in case I want to change it later
class Board:
    def __init__(self, board_type = BOARD_TYPE_LINEAR):
        self.board_type = board_type
        self.board = None

        self.setup_board()    # Might have to optimize this later to account directly for all board types and not an array
        self.turn = WHITE
        self.turn_count = 0

    def render(self):
        # Really should make an iterator or something for this... Or maybe a for x, y if I can
        for y in range(len(self.board)):
                for x in range(len(self.board[y])):
                    print(self.board[y][x], end = " ")
                print()

    def setup_board(self):
        if self.board_type == BOARD_TYPE_LINEAR:
            board = [[None] * 8 for i in range(8)]    # Maybe use numpy for this instead

            #setup = "rnbqkbnrppppppppeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeePPPPPPPPRNBQKBNR"    # Might have to change the N and K for knight and king at some point
            setup = "rnbqkbnrppppppppeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeePeeeeeeeeeeeeeee"    # Might have to change the N and K for knight and king at some point

            # I really don't like how this is done, consider doing it more elegantly eventually. Just getting it working for now
            for y in range(len(board)):
                for x in range(len(board[y])):
                    piece = setup[0]
                    setup = setup[1:]
                    board[y][x] = piece

            self.board = board

    # This function is going to need a LOT of refining and optimization in the future...
    def legal_moves(self, a, b, nA, nB):
        verbose = False

        retVal = []
        if self.turn == WHITE:
            allowable = []

            # PAWN, needs drastic improvements and optimization
            if self.board[b][a] == "P":
                opponent = WHITE
                if self.turn == WHITE: opponent = BLACK

                # Check directly in front
                forward_count = 1
                if self.turn == 0: forward_count = 2
                enemy = self.board[nB][nA]
                if enemy in opponent:
                    if(verbose): print("Pawns may not attack forward into an enemy. {} {} -> {} {}".format(a, b, nA, nB))
                elif nA < 0 or nA > 7 or nB < 0 or nB > 7:
                    if(verbose): print("Pawns may not go out of bounds. {} {} -> {} {}".format(a, b, nA, nB))
                elif self.turn in enemy:
                    if(verbose): print("Pawns may not move forward into an ally. {} {} -> {} {}".format(a, b, nA, nB))
                elif nB > b:
                    if(verbose):  print("Pawns may not move backwards. {} {} -> {} {}".format(a, b, nA, nB))
                elif nB == b:
                    if(verbose): print("Pawns may not move onto themselves. {} {} -> {} {}".format(a, b, nA, nB))
                elif b - nB > forward_count:
                    if(verbose): print("Pawns may not move forward more than once unless on their first move. {} {} -> {} {}".format(a, b, nA, nB))
                elif nA > 0:
                    if(verbose): print("Pawns may not move left or right unless attacking. {} {} -> {} {}".format(a, b, nA, nB))
                else: retVal.append([a + 0, b - 1])

            if len(retVal) == 0: return None
            return retVal

    def possible_moves(self, color, x, y):
        legals = []
        for nY in range(len(self.board)):
            for nX in range(len(self.board[nY])):
                legal = self.legal_moves(x, y, nX, nY)
                if legal != None: legals.append([x, y, nX, nY])
                #if legal != None and legal not in legals: legals.append([x, y, nX, nY])

        print(legals)
        return legals
        #print(set(legals))

    # Just return the first legal move
    def rating_idiot(self, moves):
        for piece in moves:
            for move in piece:
                return move

    def best_move(self, moves, rating_method):
        move = None

        if rating_method == RATING_IDIOT:
            move = self.rating_idiot(moves)

        return move

    def play(self):
        legals = []
        for y in range(len(self.board)):
                for x in range(len(self.board[y])):
                    if self.board[y][x] in WHITE:
                        moves = self.possible_moves(WHITE, x, y)
                        if len(moves) > 0: legals.append(moves)

        if len(legals) > 0:
            pass    # For now only let white play
            #if self.turn == WHITE: self.turn = BLACK
            #else: self.turn = WHITE
        else:    # Put win/loss conditions here
            print("No more moves available!")
            return

        # Actually play the move
        best_move = self.best_move(legals, RATING_IDIOT)
        print("Best move is {}".format(best_move))
        self.board[best_move[3]][best_move[2]] = self.board[best_move[1]][best_move[0]]
        self.board[best_move[1]][best_move[0]] = "e"

        self.turn_count += 1

board = Board()

for n in range(5):
    board.render()
    board.play()
    board.render()
    print()
