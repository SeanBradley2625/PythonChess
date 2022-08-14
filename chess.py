import copy

# This is where all the board data is stored. The program will directly manipulate this
# dictionary to make moves in the game. This is passed down the data stream in order
# to verify moves etc. It is also used to print the board. It is the core of the program.
board = {"8":{"a":" BR","b":"BKn","c":" BB","d":" BQ","e":" BK","f":" BB","g":"BKn","h":" BR"},
         "7":{"a":" BP","b":" BP","c":" BP","d":" BP","e":" BP","f":" BP","g":" BP","h":" BP"},
         "6":{"a":"   ","b":"   ","c":"   ","d":"   ","e":"   ","f":"   ","g":"   ","h":"   "},
         "5":{"a":"   ","b":"   ","c":"   ","d":"   ","e":"   ","f":"   ","g":"   ","h":"   "},
         "4":{"a":"   ","b":"   ","c":"   ","d":"   ","e":"   ","f":"   ","g":"   ","h":"   "},
         "3":{"a":"   ","b":"   ","c":"   ","d":"   ","e":"   ","f":"   ","g":"   ","h":"   "},
         "2":{"a":" WP","b":" WP","c":" WP","d":" WP","e":" WP","f":" WP","g":" WP","h":" WP"},
         "1":{"a":" WR","b":"WKn","c":" WB","d":" WQ","e":" WK","f":" WB","g":"WKn","h":" WR"}}

# These globals could be circumvented but that would require redesigning the whole program
# in order to allow aspects such as castleing and en pasants to be timed. 
epav = False
wRCastle = True
wLCastle = True
bRCastle = True
bLCastle = True

# This simple function checks the form of a positional value and returns a bool.
def formCheck(pos):
    if (pos[1:2] in "12345678") and (pos[:1] in "abcdefgh"):
        return True
    else:
        return False

# The makeMove function is the only function that can directly invoke changes to the
# board dictionary. This function is sometimes used for predicting what the board will
# look like after a given move so the function calling it can verify if it is valid.
def makeMove(moveIn, board, real):
    # setting values for upcoming code based on whether the piece being moved is
    # white or black.
    if board[moveIn[1]][moveIn[0]][1] == "W":
        col = "W"
        startY = "1"
        epPos = "5"
        pPos = "8"
    else:
        col = "B"
        startY = "8"
        epPos = "4"
        pPos = "1"
    # Removes the piece being attacked in an en pasant
    if board[moveIn[1]][moveIn[0]] == " " + col + "P" and moveIn[1] == epPos and moveIn[2] != moveIn[0]:
        board[moveIn[1]][moveIn[2]] = "   "
    # Handles the promotion of a pawn, Note the real variable used here to prevent
    # the input from being called when this function is being used in prediction mode.
    if board[moveIn[1]][moveIn[0]] == " " + col + "P" and moveIn[3] == pPos and real:
        while True:
            promotion = input("Select a piece to promote to (R, Kn, B, Q):")
            if promotion in ("R", "Kn", "B", "Q"):
                if promotion == "Kn":
                    board[moveIn[1]][moveIn[0]] = (col + promotion)
                else:
                    board[moveIn[1]][moveIn[0]] = (" " + col + promotion)
                break
            else:
                print("Invalid input")
    # Handles right and left side castleing
    if board[moveIn[1]][moveIn[0]] == (" " + col + "K") and moveIn[2] == "g" and moveIn[0:2] == "e" + startY:
        board[moveIn[1]]["h"] = "   "
        board[moveIn[1]]["f"] = " " + col + "R"
    elif board[moveIn[1]][moveIn[0]] == " " + col + "K" and moveIn[2] == "c" and moveIn[0:2] == "e" + startY:
        board[moveIn[1]]["a"] = "   "
        board[moveIn[1]]["d"] = " " + col + "R"
    # Applies the final move to the board
    board[moveIn[-1:]][moveIn[-2:-1]] = board[moveIn[1:2]][moveIn[:1]]
    board[moveIn[1:2]][moveIn[:1]] = "   "
    return board

# Renders the board. Note the use of the escape code \033c to clear the terminal
def printBoard(board):
    print(("\033c\n         Sean's terminal chess\n" + 
           "   ╔═══╤═══╤═══╤═══╤═══╤═══╤═══╤═══╗"))
    for y in ("87654321"):
        print(" " + y + " ║", end="")
        for x in ("abcdefgh"):
            print(board[y][x], end="")
            if x == "h":
                print("║")
                break
            print("│", end="")
        if y == "1":
            print("   ╚═══╧═══╧═══╧═══╧═══╧═══╧═══╧═══╝" + "\n     A   B   C   D   E   F   G   H\n")
            break
        print("   ╟───┼───┼───┼───┼───┼───┼───┼───╢")

# These two functions are used to convert between characters and integers for use
# in calculating the moves that pieces can make.
def intCon(val): # Str to Int
    yAxis = {"8" : 0, "7" : 1, "6" : 2, "5" : 3, "4" : 4, "3" : 5, "2" : 6, "1" : 7}
    xAxis = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h" : 7}
    if val in "87654321":
        return yAxis[val]
    elif val in "abcdefgh":
        return xAxis[val]

def strCon(val, axis): # Int to Str
    yAxis = ("8" ,"7" ,"6" ,"5" ,"4" ,"3" ,"2" ,"1")
    xAxis = ("a" ,"b" ,"c" ,"d" ,"e" ,"f" ,"g" ,"h")
    if axis == "y":
        return yAxis[val]
    elif axis == "x":
        return xAxis[val]

# Checks if a position on the board is a piece or not.
def validPiece(col, board, Y, X):
    for piece in ("K", "P", "B", "Q", "R"):
        if board[Y][X] == (" " + col + piece) or board[Y][X] == (col + "Kn"):
            return True

# The next four functions are used to determine the positions that pieces are attacking. This
# information will then be used to prevent the king from moving into an attacked position.

# Used for directional pieces (rook, bishop and queen)
def direcCheck(board, x, y, direction, col):
    atkPositions = []
    if direction == "h": 
        stateList = [{"y":1, "x":0}, {"y":-1, "x":0}, {"y":0, "x":-1}, {"y":0, "x":1}]
        mulList = range(1,8)
    elif direction == "d":
        stateList = [{"y":1, "x":1}, {"y":-1, "x":1}, {"y":-1, "x":-1}, {"y":1, "x":-1}]
        mulList = range(1,8)
    else: 
        return atkPositions
    for state in stateList:
        for mul in range(1, 8):
            yVal = intCon(y) + (mul * state["y"])
            xVal = intCon(x) + (mul * state["x"])
            if (yVal >= 8 or yVal <= -1) or (xVal >= 8 or xVal <= -1):
                break
            else:
                Y = (strCon(yVal, "y"))
                X = (strCon(xVal, "x"))
                if validPiece(col, board, Y, X):
                    break
                else:
                    atkPositions.append(Y+X)
                    if board[Y][X] != "   ":
                        break
    return atkPositions

def knightCheck(board, x, y, col):
    atkPositions = []
    for state in [{"y":1, "x":1}, {"y":-1, "x":1}, {"y":-1, "x":-1}, {"y":1, "x":-1}]:
        for mul in ((1, 2), (2, 1)):
            yVal = intCon(y) + (mul[0] * state["y"])
            xVal = intCon(x) + (mul[1] * state["x"])
            if not ((yVal >= 8 or yVal <= -1) or (xVal >= 8 or xVal <= -1)):
                Y = (strCon(yVal, "y"))
                X = (strCon(xVal, "x"))
                if validPiece(col, board, Y, X):
                    pass
                else:
                    atkPositions.append(Y+X)
    return atkPositions

def kingCheck(board, x, y, col):
    atkPositions = []
    for state in [{"y":1, "x":1}, {"y":-1, "x":1}, {"y":-1, "x":-1}, {"y":1, "x":-1}, 
                  {"y":1, "x":0}, {"y":-1, "x":0}, {"y": 0, "x":-1}, {"y":0, "x": 1}]:
        yVal = intCon(y) + state["y"]
        xVal = intCon(x) + state["x"]
        if not ((yVal >= 8 or yVal <= -1) or (xVal >= 8 or xVal <= -1)):
            Y = (strCon(yVal, "y"))
            X = (strCon(xVal, "x"))
            if validPiece(col, board, Y, X):
                pass
            else:
                atkPositions.append(Y+X)
    return atkPositions

def pawnCheck(board, x, y, col):
    atkPositions = []
    if col == "B":
        stateList = [{"y":1, "x":1}, {"y":1, "x":-1}]
        row = "4"
        oppCol = " WP"
    elif col == "W":
        stateList = [{"y":-1, "x":1}, {"y":-1, "x":-1}]
        row = "5"
        oppCol = " BP"
    else:
        return atkPositions
    for state in stateList:
       yVal = (intCon(y) + state["y"])
       xVal = (intCon(x) + state["x"])
       if not (intCon(x) + state["x"] >= 8 or intCon(x) + state["x"] <= -1):
            Y = (strCon(yVal, "y"))
            X = (strCon(xVal, "x"))
            atkPositions.append(Y+X)
    return atkPositions

# This function is very important for determining if a king will put himself into check in the
# given move. It creates a map of all the positions being attacked by the provided colour. This
# will then be returned and can be indexed in the same way as the board.
def attackMap(board, col):
    atkMap = {"8":{"a":"","b":"","c":"","d":"","e":"","f":"","g":"","h":""},
              "7":{"a":"","b":"","c":"","d":"","e":"","f":"","g":"","h":""},
              "6":{"a":"","b":"","c":"","d":"","e":"","f":"","g":"","h":""},
              "5":{"a":"","b":"","c":"","d":"","e":"","f":"","g":"","h":""},
              "4":{"a":"","b":"","c":"","d":"","e":"","f":"","g":"","h":""},
              "3":{"a":"","b":"","c":"","d":"","e":"","f":"","g":"","h":""},
              "2":{"a":"","b":"","c":"","d":"","e":"","f":"","g":"","h":""},
              "1":{"a":"","b":"","c":"","d":"","e":"","f":"","g":"","h":""}}
    for y in ("87654321"):
        for x in ("abcdefgh"):
            if board[y][x][:2] == (" " + col) or board[y][x][:1] == col:
                piece = board[y][x]
                if piece == (col + "Kn"):
                    for i in knightCheck(board, x, y, col):
                        atkMap[i[0]][i[1]] = "x"
                elif piece == (" " + col + "R"):
                    for i in direcCheck(board, x, y, "h", col):
                        atkMap[i[0]][i[1]] = "x"
                elif piece == (" " + col + "B"):
                    for i in direcCheck(board, x, y, "d", col):
                        atkMap[i[0]][i[1]] = "x"
                elif piece == (" " + col + "Q"):
                    for i in (direcCheck(board, x, y, "d", col) + direcCheck(board, x, y, "h", col)):
                        atkMap[i[0]][i[1]] = "x"
                elif piece == (" " + col + "K"):
                    for i in kingCheck(board, x, y, col):
                        atkMap[i[0]][i[1]] = "x"
                elif piece == (" " + col + "P"):
                    for i in pawnCheck(board, x, y, col):
                        atkMap[i[0]][i[1]] = "x"
    return atkMap

# Returns the opposite colour to the one provided in the colour format used for pieces on the board.
def oppositeCol(col):
    if col == "white":
        return "B"
    elif col == "black":
        return "W"

# Returns the same colour to the one provided in the colour format used for pieces on the board.
def findCol(col):
    if col == "white":
        return "W"
    elif col == "black":
        return "B"

# These next three functions are required for kings and pawns because their attack positions are not
# the same as their move positions.

# This function is used to determin where a pawn can move, mainly special moves such as en pasants
# and double steps on their first move.
def pawnMoveCheck(board, x, y, col):
    movePos = []
    global epav
    if y == "2" or y == "7":
        jumpList = (1, 2)
    else:
        jumpList = (0,1)
    for i in jumpList:
        if col == "W":
            if y == "5" and board[y][strCon((intCon(x) + 1), "x")] == " BP" and epav:
                movePos.append(strCon((intCon(y) - 1), "y") + strCon((intCon(x) + 1), "x"))
            if y == "5" and board[y][strCon((intCon(x) - 1), "x")] == " BP" and epav:
                movePos.append(strCon((intCon(y) - 1), "y") + strCon((intCon(x) - 1), "x"))
            if board[strCon((intCon(y) - i), "y")][x] == "   ":
                movePos.append(strCon((intCon(y) - i), "y") + x)
        elif col == "B":
            if y == "4" and board[y][strCon((intCon(x) + 1), "x")] == " WP" and epav:
                movePos.append(strCon((intCon(y) + 1), "y") + strCon((intCon(x) + 1), "x"))
            if y == "4" and board[y][strCon((intCon(x) - 1), "x")] == " WP" and epav:
                movePos.append(strCon((intCon(y) + 1), "y") + strCon((intCon(x) - 1), "x"))
            if board[strCon((intCon(y) + i), "y")][x] == "   ":
                movePos.append(strCon((intCon(y) + i), "y") + x)
    return movePos

# Used to determine if the given move will endanger the king.
def kingSafetyCheck(board, col, oppCol, start, end):
    if board[start[1]][start[0]] == (" " + col + "K"):
        return attackMap(makeMove(start + end, copy.deepcopy(board), False), oppCol)[end[1]][end[0]]
    else:
        for y in ["8", "7", "6", "5", "4", "3", "2", "1"]:
            for x in ["a", "b", "c", "d", "e", "f", "g", "h"]:
                if board[y][x] == (" " + col + "K"):
                    return attackMap(makeMove(start + end, copy.deepcopy(board), False), oppCol)[y][x]

# Checks if a castle is a viable move. Note the use of different global variables for W and B as well
# as left and right castles.
def castleCheck(col, oppCol, start, end, board):
    global wLCastle
    global wRCastle
    global bLCastle
    global bRCastle
    if end != "c1" and end != "g1" and end != "c8" and end != "g8":
        return False
    if col == "W" and (wRCastle or wLCastle):
        trueStart = "e1"
    elif col == "B" and (bRCastle or bLCastle):
        trueStart = "e8"
    else:
        return False
    if end[0] == "c" and board[trueStart[1]]["a"] == (" " + col + "R"):
        if (wLCastle and col == "W") or (bLCastle and col == "B"):
            aCheckList = ["b", "c", "d"]
            bCheckList = ["c", "d", "e"]
        else:
            return False
    elif end[0] == "g" and board[trueStart[1]]["h"] == (" " + col + "R"):
        if (wRCastle and col == "W") or (bRCastle and col == "B"):
            aCheckList = ["f", "g"]
            bCheckList = ["e", "f", "g"]
        else:
            return False
    if board[trueStart[1]][trueStart[0]] == (" " + col + "K"):
        for x in aCheckList:
            if board[trueStart[1]][x] != "   ":
                return False
        for x in bCheckList:
            if attackMap(board, oppCol)[trueStart[1]][x] == "x":
                return False
        return True

# This is a key function that checks whether the given move is within the bounds of the rules.
def posCheck(start, end, trnCol, board):
    col = findCol(trnCol)
    oppCol = oppositeCol(trnCol)
    s0 = start[0]
    s1 = start[1]
    endr = end[1] + end[0]
    global epav
    global wLCastle
    global wRCastle
    global bLCastle
    global bRCastle
    # If the move or the current position endangers the king the move is invalid. 
    if kingSafetyCheck(board, col, oppCol, start, end) == "x":
        return False
    elif board[s1][s0][:2] == (" " + col) or board[s1][s0][:1] == col:
        piece = board[s1][s0]
        # Note how the following checks reuse the functions used to determine where these pieces could attack.
        # Knight
        if piece == (col + "Kn"):
            if endr in knightCheck(board, s0, s1, col):
                epav = False
                return True
        # Rook
        elif piece == (" " + col + "R"):
            if endr in direcCheck(board, s0, s1, "h", col):
                if col == "W":
                    if s0 == "a":
                        wLCastle = False
                    elif s0 == "h":
                        wRCastle = False
                elif col == "B":
                    if s0 == "a":
                        bLCastle = False
                    elif s0 == "h":
                        bRCastle = False
                epav = False
                return True
        # Bishop
        elif piece == (" " + col + "B"):
            if endr in direcCheck(board, s0, s1, "d", col):
                epav = False
                return True
        # Queen
        elif piece == (" " + col + "Q"):
            if endr in (direcCheck(board, s0, s1, "d", col) + direcCheck(board, s0, s1, "h", col)):
                epav = False
                return True
        # King
        elif piece == (" " + col + "K"):
            if ((endr in kingCheck(board, s0, s1, col) and attackMap(board, oppCol)[end[1]][end[0]] != "x") 
            or castleCheck(col, oppCol, start, end, board)):
                if col == "W":
                    wLCastle = False
                    wRCastle = False
                elif col == "B":
                    bLCastle = False
                    bRCastle = False
                epav = False
                return True
        # Pawn
        elif piece == (" " + col + "P"):
            if (endr in pawnMoveCheck(board, s0, s1, col) 
            or (endr in pawnCheck(board, s0, s1, col) and board[end[1]][end[0]] != "   ")):
                epav = False
                if end[1] == "4" and col == "W" and s1 == "2":
                    epav = True
                elif end[1] == "5" and col == "B" and s1 == "7":
                    epav = True
                return True

# This function takes the raw user input and determines if its a valid move, command or nothing.
def moveCheck(moveIn, trnCol, board):
    if moveIn in ("quit", "Quit", "exit", "Exit", "q", "Q", "leave", "Leave"):
        print("Exiting now...")
        quit()
    if moveIn in ("help", "Help", "h", "H", "info", "Info", "i", "I"):
        print("\nMoveing:\n\t[Starting position][Ending position]\n\tExample: d2d4" +
              "\nExiting:\n\tPosible exit commands: quit, exit, leave, q" +
              "\nInformation:\n\tPosible info commands: help, info, h, i\n")
        return "i" 
    start = moveIn[:2]
    end = moveIn[-2:]
    if start != end and formCheck(start) and formCheck(end) and posCheck(start, end, trnCol, board):
         return (start + end)
    return False

# Main program loop
while True:
    for turnColour in ("white", "black"):
        printBoard(board)
        while True:
            moveIn = moveCheck(input(turnColour + "'s move: "), turnColour, board)
            if moveIn == "i":
                pass
            elif moveIn == False:
                 print("Invalid move")
            else:
                board = makeMove(moveIn, board, True)
                break
