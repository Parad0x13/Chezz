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
        self.game_alive = True

    def render(self):
        # Really should make an iterator or something for this... Or maybe a for x, y if I can
        for y in range(len(self.board)):
                for x in range(len(self.board[y])):
                    print(self.board[y][x], end = " ")
                print()

    def setup_board(self):
        if self.board_type == BOARD_TYPE_LINEAR:
            board = [[None] * 8 for i in range(8)]    # Maybe use numpy for this instead

            setup = "rnbqkbnrppppppppeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeePPPPPPPPRNBQKBNR"    # Might have to change the N and K for knight and king at some point

            # I really don't like how this is done, consider doing it more elegantly eventually. Just getting it working for now
            for y in range(len(board)):
                for x in range(len(board[y])):
                    piece = setup[0]
                    setup = setup[1:]
                    board[y][x] = piece

            self.board = board

    # Probably not efficient to do this every single turn...
    def rotate(self):
        tuples = zip(*self.board[::-1])
        self.board = [list(elm) for elm in tuples]

    # This function is going to need a LOT of refining and optimization in the future...
    # [TODO] I feel like this function is getting called far too often...
    def legal_moves(self, a, b, nA, nB):
        retVal = []
        if self.turn == WHITE or self.turn == BLACK:
            allowable = []

            # PAWN, needs drastic improvements and optimization
            searching = "P"
            if self.turn == BLACK: searching = "p"

            if self.board[b][a] == searching:
                opponent = WHITE
                if self.turn == WHITE: opponent = BLACK

                rules = [
                    [a + 0, b - 1, "e"],    # Move forward
                    # Account for double first move here
                    [a - 1, b - 1, opponent],    # Attack up left
                    [a + 1, b - 1, opponent],    # Attack up right
                ]

                for rule in rules:
                    try:    # Try does a good job of dynamically handling out of bounds issues
                        piece = self.board[nB][nA]
                        if nA == rule[0] and nB == rule[1] and piece in rule[2]:
                            retVal.append(rule)

                        #    Now we handle promotion, really this needs to be fully fleshed out to any piece. Default Queen
                        #if nB == 0: self.board[nB][nA] = "Q"    # This doesn't work as it happens to all the backrow... figure it out

                    except: pass    # Movement is out of bounds

            if len(retVal) == 0: return None
            return retVal

    def possible_moves(self, color, x, y):
        legals = []
        for nY in range(len(self.board)):
            for nX in range(len(self.board[nY])):
                legal = self.legal_moves(x, y, nX, nY)
                if legal != None: legals.append([x, y, nX, nY])

        return legals

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

    def iterate(self):
        legals = []
        for y in range(len(self.board)):
                for x in range(len(self.board[y])):
                    if self.board[y][x] in self.turn:
                        moves = self.possible_moves(self.turn, x, y)
                        if len(moves) > 0: legals.append(moves)

        if len(legals) == 0:
            print("No more moves available!")
            self.game_alive = False
            return

        # Actually play the move
        best_move = self.best_move(legals, RATING_IDIOT)
        #print("Best move is {}".format(best_move))
        print()
        self.board[best_move[3]][best_move[2]] = self.board[best_move[1]][best_move[0]]
        self.board[best_move[1]][best_move[0]] = "e"

    def play(self):
        if self.game_alive == False: exit()

        self.iterate()

        if self.turn == WHITE: self.turn = BLACK
        else: self.turn = WHITE

        for i in range(2): self.rotate()

        self.iterate()

        if self.turn == WHITE: self.turn = BLACK
        else: self.turn = WHITE

        for i in range(2): self.rotate()

        self.turn_count += 1

board = Board()

for n in range(1):
#while True:
    board.render()
    board.play()
    board.render()
    print()
